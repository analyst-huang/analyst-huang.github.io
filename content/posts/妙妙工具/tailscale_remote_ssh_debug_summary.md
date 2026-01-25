---
title: "Tailscale + VS Code Remote-SSH 故障排查复盘"
date: 2026-01-23
draft: false
---


# 从原理到实战：Tailscale 在校园网环境下的连接机制与排障记录

## 1. 背景与问题陈述

我希望用 Tailscale 让两台处于不同网络环境（不同 NAT/不同局域网）的机器互相访问。实际使用/调试中遇到典型问题：

- `tailscale netcheck` 有时显示 IPv6 可用、有时不可用；
- 关闭路由器 UPnP 后，`PortMapping` 变为空，但依旧无法 `ping` 对端；
- 路由器后台显示 WAN 口拿到了公网 IPv6，但内网主机 `ipconfig` 只有 `fe80::`（link-local）而没有公网 IPv6；
- 最终定位：**校园网策略限制**导致“路由器能拿到 IPv6，但无法向 LAN 下发前缀（Prefix Delegation/RA）”，从而使内网终端 IPv6 不可用；Tailscale 在纯 IPv4 + 多级 NAT 环境下直连成功率显著下降，表现为 ping 不通或频繁退化到 DERP 中继。

---

## 2. Tailscale 是什么：控制面与数据面

一句话概括：

> Tailscale = **WireGuard 数据面** + **云端控制面（身份/公钥/节点发现/路由下发）** 的自动化 Overlay Network。

### 2.1 控制面（Control Plane）做什么

控制面通过 HTTPS 与每个节点通信，负责：

- 身份认证（SSO/OAuth 等）与设备注册
- 节点公钥分发（谁是谁的 peer）
- 节点地址发现与“可达性信息”交换（NAT 映射、候选 endpoint）
- ACL/路由策略下发（谁可以访问谁）

控制面**不承载你的业务数据**（除非走 DERP 时需要中继服务，见下文）。

### 2.2 数据面（Data Plane）做什么

数据面是 WireGuard：

- 每个节点有一对公私钥
- 节点之间用 UDP 传输加密后的 WireGuard 数据包
- 理想状态：**P2P 直连**
- 直连失败：**走 DERP Relay（中继）**，仍保持端到端加密

---

## 3. “网卡”到底是什么意思：TUN 虚拟网卡与路由表

Tailscale 启动后会创建一个虚拟网卡（Windows 上表现为 “未知适配器 Tailscale”；Linux 常见为 `tailscale0`）。

### 3.1 OS 视角：网卡 = net_device 抽象

在操作系统里，“网卡”是一个统一抽象：能收发 IP 包的接口对象。可以是：

- 物理网卡：以太网/Wi‑Fi
- 回环接口：`lo`
- 虚拟网卡：VPN/TUN/TAP/容器 veth

### 3.2 ping 一个 IP 时发生了什么

准确表述是：

> **不是“IP 属于某张网卡”，而是“路由表决定目标 IP 的出接口（网卡）”。**

内核流程（概念化）：

1. 用户态 `ping` 通过系统调用把 ICMP 包交给内核
2. 内核查路由表（FIB lookup）：
   - 目标 IP 落在哪个前缀？
   - 匹配到哪条路由规则？
3. 得出出接口 `dev`
4. 把 packet 交给该接口的发送路径  
   - 若是物理网卡：最终 DMA/驱动发出
   - 若是 TUN（Tailscale 虚拟网卡）：写入 TUN 设备缓冲，由 Tailscale 进程读取、加密、再通过 UDP 发出

---

## 4. 连接建立的关键：NAT、打洞、DERP、IPv6

Tailscale 连接“能不能直连”，通常取决于：

1. **IPv6 是否可用**（极大提升直连概率）
2. **NAT 类型是否友好**（对称 NAT 很难打洞）
3. 是否允许 UDP、是否有复杂防火墙/RA guard 等策略

### 4.1 netcheck 里几个字段的含义（排障高频）

`tailscale netcheck` 输出里，最有诊断价值的字段包括：

- `UDP: true/false`：是否能发 UDP（WireGuard 基础需求）
- `IPv4: yes, <公网IP:端口>`：STUN 探测到的 IPv4 出口映射
- `IPv6: yes/no`：是否能用 IPv6 做 STUN/连通（不是“系统是否支持”，而是“是否真的可用”）
- `MappingVariesByDestIP: true/false`：NAT 映射是否随目标变化  
  - **true**：通常更“可打洞”（cone/EIM 类）
  - **false**：更像对称 NAT（对打洞不友好）
- `PortMapping: UPnP, NAT-PMP`：路由器是否在做自动端口映射
- `Nearest DERP`：最近的 DERP 中继站点（直连失败时可能走它）

---

## 5. 调试实录：从“有时能连”到“稳定不可用”的定位

### 5.1 两次 netcheck 的关键差异（简化摘录）

**能连时**（节选）：

- `IPv6: yes, [2408:...]:55694`
- `MappingVariesByDestIP: true`
- `PortMapping:`（空）

**不行时**（节选）：

- `IPv6: no, but OS has support`
- `MappingVariesByDestIP: false`
- `PortMapping: UPnP, NAT-PMP`

第一轮推断：网络环境在变化（出口 IP/端口、IPv6 可用性、NAT 行为），尤其 `PortMapping` 的出现提示路由器自动映射可能导致不稳定。

### 5.2 操作：关闭 UPnP/NAT-PMP

关闭后再次 netcheck（节选）：

- `MappingVariesByDestIP: true`
- `PortMapping:`（空）
- `IPv6: no, but OS has support`
- `IPv4: yes, 115.27.214.90:58693`

结论：  
关闭 UPnP 的确让 NAT 行为更“健康”（`MappingVariesByDestIP: true`，`PortMapping` 为空），但 **连通性仍未恢复**，说明根因不在 UPnP，而在 **IPv6 不可用 + IPv4 环境多级 NAT/策略限制**。

---

## 6. 关键证据：路由器 WAN 有 IPv6，但 LAN 无公网 IPv6

### 6.1 路由器 IPv6 状态页（核心证据）

路由器显示（节选）：

- `IPv6 WAN口地址: 240c:c001:.../64`（公网 IPv6）
- `IPv6 默认网关: fe80::...`（上游网关，link-local 是正常现象）

这说明：**上游（校园网）确实提供 IPv6，且路由器 WAN 口能拿到公网 IPv6。**

### 6.2 终端 `ipconfig`（第二个核心证据）

Windows `ipconfig` 显示：

- 以太网接口：只有 `fe80::...`（link-local IPv6），没有 `240c:...` 这类 global IPv6
- IPv4：`192.168.0.111`，网关 `192.168.0.1`

这说明：**路由器并没有向 LAN 广播/下发 IPv6 前缀**，终端无法形成可用的 IPv6 出口（因此 Tailscale netcheck 的 `IPv6: no` 是必然的）。

> 注意：Tailscale 适配器上出现的 `fd7a:...` 属于 Tailscale 自己的 ULA（私有 IPv6），不等价于公网 IPv6 可用。

---

## 7. 为什么校园网会导致“路由器拿到 IPv6，但 LAN 拿不到”

在校园网里，常见策略是：

- 允许“**直连终端**”通过 SLAAC/DHCPv6 获取 IPv6
- **禁止二级路由器**进行 Prefix Delegation（DHCPv6-PD）
- 启用 RA Guard / DHCP Guard，防止你在下游广播 RA、扩展子网、绕过审计

因此出现典型拓扑：

```
校园网（提供 IPv6）
   │
   ├── 你的电脑（直连） → 能拿到 IPv6 → Tailscale 直连概率极高
   │
   └── 你的路由器（WAN 有 IPv6） → 但无法获得前缀委派给 LAN → LAN 终端只有 fe80::
```

在这种模式下，“路由器 IPv6 开着”并不代表“LAN 终端有 IPv6”。

---

## 8. IPv6 对 Tailscale 的影响为什么是数量级的

这不是“快一点”的差别，而是“**连接机制不同**”：

### 8.1 有 IPv6：几乎等价于公网直连

- 全局可路由地址
- 无 NAT
- 无打洞
- WireGuard UDP 直接建立 peer 通道

直连成功率通常非常高，抖动和失败模式很少。

### 8.2 没 IPv6：进入 IPv4 NAT 打洞的概率世界

- 需要 STUN 探测
- 需要双方 NAT 行为都足够友好
- 需要状态保持与路径迁移
- 失败就会退化到 DERP（延迟/带宽受限）

在 **校园网 + 多级 NAT/防火墙策略** 下，直连成功率会显著下降，这也是 “ping 不通/不稳定” 的根本原因。

---

## 9. 实用排障与验证步骤（命令行优先）

以下以 Windows PowerShell 为例，并对参数做简要解释。

### 9.1 查看 Tailscale 的网络能力摘要

```powershell
tailscale netcheck
```

- `netcheck`：对当前网络环境做 STUN/连通性探测，输出 NAT/IPv6/DERP 等诊断信息。

重点观察：`IPv6`、`MappingVariesByDestIP`、`PortMapping`。

### 9.2 查看是否直连或走 DERP

```powershell
tailscale status
```

- `status`：列出 tailnet 中各节点及其在线/路径信息。

以及：

```powershell
tailscale ping <peer>
```

- `ping`：在 Tailscale 网络层做探测，常会显示 `via DERP(...)` 或直连信息。

### 9.3 查看本机是否获得公网 IPv6（关键）

```powershell
ipconfig
```

- 关注以太网/Wi‑Fi 接口是否存在形如 `240c:`/`2408:` 的 global IPv6 地址；
- 若只有 `fe80::`，代表仅有 link-local，无法直接上 IPv6 Internet。

可再验证 IPv6 连通：

```powershell
ping -6 ipv6.google.com
```

- `-6`：强制使用 IPv6。

### 9.4 验证“直连校园网 vs 经过路由器”的差异（强烈推荐）

- 电脑直插校园网（不经过你的路由器）→ 重复 `ipconfig` 与 `tailscale netcheck`
- 电脑接你的路由器 LAN → 重复同样命令

如果直连时出现 global IPv6，而经路由器时消失，则可以定性为：校园网策略限制二级路由的 IPv6 前缀委派/RA。

---

## 10. 可行解决方案（按可操作性排序）

### 方案 A：每台设备直接接校园网（最稳定）

- 终端自己拿 IPv6
- Tailscale P2P 直连概率显著提升

### 方案 B：接受 DERP（对 SSH/管理足够）

- 不追求低延迟大带宽时可接受
- 适合远程管理、轻量同步

### 方案 C：自建中继（追求稳定/可控路径）

- 在公网 VPS 部署 DERP 或其他中继方案
- 让关键流量稳定走可控的中继点

### 方案 D：向校园网网管申请支持（通常较难）

- 申请 DHCPv6-PD / Prefix Delegation
- 或申请允许下游 RA/路由（很少会批）

### 方案 E：改成桥接/旁路（视校园网认证方式而定）

如果校园网要求 802.1X/Web Portal 等认证，二级路由可能天然不兼容；桥接/旁路方案可降低二级 NAT 的不确定性，但是否可行取决于校园网具体策略。

---

## 11. 总结：本次排障的“结构性结论”

1. **UPnP 不是根因**：关闭后 NAT 更健康，但连通性未恢复。  
2. **IPv6 是关键变量**：有 IPv6 时，Tailscale 更接近“纯 WireGuard 直连”；无 IPv6 时，进入“IPv4 NAT 打洞”概率世界。  
3. **校园网是治理型网络**：常禁止二级路由的 IPv6 前缀委派/RA 广播，导致“路由器 WAN 有 IPv6，但 LAN 无公网 IPv6”。  
4. **工程决策优先**：与其继续微调本地路由器，不如选择“直连校园网 / 接受 DERP / 自建中继”这类结构性解法。

---

## 附录：本次关键输出摘录（供对照）

### A. `tailscale netcheck`（关闭 UPnP 后）

- `UDP: true`
- `IPv4: yes, 115.27.214.90:58693`
- `IPv6: no, but OS has support`
- `MappingVariesByDestIP: true`
- `PortMapping:`（空）

### B. Windows `ipconfig`（LAN 接路由器）

- 以太网：只有 `fe80::...`，无 global IPv6
- IPv4：`192.168.0.111`，网关 `192.168.0.1`

---

*本文为排障记录性质的技术博客，重点在于“机制解释 + 证据链 + 工程结论”。如需进一步深入，可扩展：NAT 类型判别方法、对称 NAT 的不可打洞性、DERP 的路径选择与性能影响等。*

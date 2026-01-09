---
title: "Socket"
date: 2026-01-09
draft: false
---

# 进程、内核与 Socket：通信机制要点

## 一、每个进程都有哪些是“独立的”？

每个进程有独立的：

* 虚拟地址空间
* 寄存器上下文

内核用**时间片轮转**在同一颗物理 CPU 上切换它们。

但有一件事是**不虚拟的**：

> 所有进程共享同一个操作系统内核。

而 **socket 属于**：

* 内核对象（kernel object）

当你在用户态调用：

```text
sock.send(...)
```

实际上发生的是：

1. 触发系统调用（syscall）
2. CPU 切到内核态
3. 内核代表你这个进程去执行真正的发送逻辑

所以通信的“公共场所”不是 CPU，而是：

> 内核里的网络协议栈 + 内核缓冲区

---

## 二、Socket 在内核里到底是什么？

从内核视角看，一个 socket 大致包含：

* socket 结构体
* 接收缓冲区（recv buffer）
* 发送缓冲区（send buffer）
* 协议状态机（TCP 状态、序列号等）

每个进程持有的其实只是：

> 一个文件描述符 `fd` → 指向内核里的 socket 对象

所以：

* 两个进程可以分别持有：

  * 指向**同一个 socket 对象**的 fd（例如通过 `fork` 继承）
  * 或一对**互相关联的 socket**（TCP 连接两端）

# Socket 与 TCP 出现之前的通信历史（极简时间线）

## 一、最早期：只有物理通信（无协议）

- 串口、并口、专用总线
- 直接发送电信号
- 特点：
  - 无地址
  - 无连接
  - 无可靠性
- 本质：硬件层通信，没有操作系统抽象

---

## 二、分组交换网络：只有“包”，没有“连接”

- ARPANET / 早期 IP 思想
- 通信模型：
  - send(packet)
  - 网络尽力投递
- 特点：
  - 无连接
  - 可能丢包 / 乱序 / 重复
- 接近今天的：IP / UDP 语义

---

## 三、应用自己实现可靠性（应用层协议时代）

- FTP / Telnet 等早期协议
- 每个应用自己实现：
  - 序号
  - ACK
  - 重传
  - 流控
- 问题：
  - 重复造轮子
  - 质量不可控
  - 网络整体容易拥塞

---

## 四、TCP 的出现：把“可靠流”下沉到内核

- TCP 抽象：
  - 可靠
  - 有序
  - 字节流
- 协议状态必须长期维护：
  - 状态机
  - 缓冲区
  - 拥塞控制
- 结果：
  - 状态进入操作系统内核
  - 通信关系成为内核对象

---

## 五、Socket 的诞生：进程访问内核协议栈的统一接口

- BSD Unix 引入 socket API
- 设计目标：
  - 用 fd 表示通信端点
  - 统一 TCP / UDP / 本地域通信
- 本质：
  - socket = 协议状态 + 缓冲区 + 控制逻辑 的内核对象

---

## 一句话总结

- TCP 之前：  
  → 要么无连接无可靠性（只发包）  
  → 要么可靠性由应用自己实现  

- TCP 之后：  
  → 可靠通信成为操作系统职责  
  → 必须有内核级端点对象  
  → socket 因此诞生

# Python Socket API（要点总结：1–5）

一、Python 的 socket 对应内核里的什么？

-   socket.socket() 调用内核的 socket() 系统调用创建内核 socket 对象
-   内核返回文件描述符（fd），Python 将其封装成 socket 对象
-   真实的数据缓冲区、协议状态机全部在内核中
-   send/recv 实际路径：Python → libc → syscall → 内核协议栈

------------------------------------------------------------------------

二、socket.socket(…) 参数含义

标准构造：

    socket.socket(family, type, proto=0)

常见组合：

-   TCP：

        socket.socket(AF_INET, SOCK_STREAM)

    -   IPv4 + 字节流 + 面向连接 → TCP

-   UDP：

        socket.socket(AF_INET, SOCK_DGRAM)

    -   IPv4 + 数据报 + 无连接 → UDP

-   本机通信：

        socket.socket(AF_UNIX, SOCK_STREAM)

    -   仅在内核中拷贝，不走网络协议栈

------------------------------------------------------------------------

三、TCP 服务端完整流程（内核视角）

1.  创建 socket

        s = socket.socket()

    -   内核创建 socket 对象

2.  bind

        s.bind((ip, port))

    -   绑定本地地址与端口

3.  listen

        s.listen(backlog)

    -   socket 进入 LISTEN 状态
    -   建立连接等待队列
    -   不能用于数据传输

4.  accept

        conn, addr = s.accept()

    -   内核创建新的 socket（ESTABLISHED）
    -   返回新的 fd 用于真实通信
    -   原 socket 仍用于继续监听

5.  send / recv

        conn.send(...)
        conn.recv(...)

    -   TCP 提供可靠有序字节流
    -   不保证消息边界，需自定义协议分帧

------------------------------------------------------------------------

四、TCP 客户端流程

    s = socket.socket()
    s.connect((server_ip, port))

-   触发三次握手
-   socket 进入 ESTABLISHED 状态
-   之后 send/recv 与服务端对等通信

------------------------------------------------------------------------

五、UDP API 的本质区别

-   无连接、无状态机、无重传保证

发送：

    s.sendto(data, addr)

接收：

    data, addr = s.recvfrom(4096)

特点：

-   无 listen / accept
-   每个数据报独立处理
-   可调用 connect() 仅用于固定默认目标地址（不建立真实连接）

------------------------------------------------------------------------

一句话对比

-   TCP socket：内核维护连接状态与缓冲区，提供可靠字节流
-   UDP socket：仅提供数据报投递接口，不提供可靠性与顺序保证
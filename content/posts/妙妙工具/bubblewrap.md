---
title: "bubblewrap"
date: 2025-12-24
draft: false
---

# Bubblewrap 的功能与 GPU 隔离用法

## Bubblewrap 是做什么的

**Bubblewrap（bwrap）** 是一个基于 Linux namespaces 的**进程级 sandbox 工具**，核心功能只有一件事：

> **在系统层面为“单个进程”构造一个最小可见、白名单式的运行环境。**

从工程角度看，它提供的能力非常集中：

- 创建独立的 **mount namespace**
- 默认使用 **空的根文件系统（tmpfs）**
- 仅通过 `--bind / --dev-bind` 暴露**显式允许的路径与设备**
- 精确控制 `/dev` 下可见的设备节点
- **进程退出即销毁**，无任何残留状态

它**不负责**：

- 镜像构建
- 服务部署
- 长期运行
- 资源调度

---

## Bubblewrap 能解决什么 GPU 问题

在 Isaac Lab / Omniverse 场景中：

- `CUDA_VISIBLE_DEVICES` 只影响 **CUDA**
- Vulkan / RTX / NVML 仍可能枚举**宿主机全部 GPU**
- 根因是：**系统设备节点未被隔离**

Bubblewrap 的作用是：

> **从 `/dev` 与文件系统层面，让“不该存在的 GPU 真的不存在”。**

---

## 最小示例：用 Bubblewrap 屏蔽 GPU

下面示例中，**进程只能看到 GPU 0**，其余 GPU 在系统层面不可见。

```bash
bwrap \
  --bind / / \
  --dev /dev \
  --dev-bind /dev/nvidia6 /dev/nvidia6 \
  --dev-bind /dev/nvidiactl /dev/nvidiactl \
  --dev-bind /dev/nvidia-uvm /dev/nvidia-uvm \
  -- bash
```
### 效果

- `/dev` 中只存在 **GPU 6** 相关节点  
- 其他 GPU 对该进程而言 **不存在**

## 一句话总结

- **Container**：解决「如何长期运行一个软件」
- **Bubblewrap**：解决「是否允许这段代码看到这些资源」

---
title: "zmq"
date: 2026-01-11
draft: false
---
最近在做机器人遥操，所以需要在多进程之间交换数据。直接用socket来写就太底层了，所以就研究了一下封装库zmq怎么用。结果出了一个延迟的bug，特此记录zmq的用法。

ZeroMQ PUB-SUB 总结（代码导向）

一、角色职责（Role Semantics）

Publisher（PUB）

职责：只负责发送消息（广播），不接收任何数据。

    import zmq

    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://*:5555")

    while True:
        pub.send(b"state robot_pose=...")

特点： - 只能 send()，不能 recv() - 不知道是否有订阅者 -
不关心订阅者订了什么

Subscriber（SUB）

职责：只负责接收并按 topic 过滤消息，不发送任何数据。

    import zmq

    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://localhost:5555")

    # 订阅前缀为 b"state" 的消息
    sub.setsockopt(zmq.SUBSCRIBE, b"state")

    while True:
        msg = sub.recv()
        print(msg)

特点： - 只能 recv()，不能 send() - 必须显式设置订阅规则 -
只能收到匹配前缀的消息

二、连接方式（Connection Pattern）

语义与 bind / connect 无关，只是部署方式不同。

常见方式：

方式 A：PUB bind，SUB connect（经典服务器广播）

    # PUB
    pub.bind("tcp://*:5555")

    # SUB
    sub.connect("tcp://server_ip:5555")

方式 B：SUB bind，PUB connect（受防火墙限制时使用）

    # SUB
    sub.bind("tcp://*:5555")

    # PUB
    pub.connect("tcp://client_ip:5555")


ZMQ 在底层维护连接拓扑，应用层不感知对端数量。

六、可靠性语义（Delivery Guarantees）

PUB-SUB 是 best-effort（尽力而为）广播模型，没有可靠投递保证。

会丢消息的情况

-   SUB 尚未完成连接 → 早期消息全部丢弃
-   SUB 处理不过来 → 队列满后丢消息
-   新订阅者加入 → 只能收到之后的消息

也就是说：

  没有 ACK，没有重传，没有历史缓存。

队列与背压（HWM）

每个 socket 内部有发送/接收队列：

-   High Water Mark (HWM)
-   队列满时：
    -   PUB：直接丢消息
    -   SUB：丢旧或新（取决于配置）

示例：

    pub.setsockopt(zmq.SNDHWM, 1000)
    sub.setsockopt(zmq.RCVHWM, 1000)

但即使设置了 HWM： - 仍然不能保证不丢 - 只是在高负载时控制内存使用

**在teleop的场景中，实时性是很重要的，如果pub发送的hz高，而sub接收的频率低，那么就会导致sub的队列积压消息，并且丢弃消息，最合适的方法是，将sub的队列设置为1，即始终只接受最新的信息！！！**

适合与不适合的场景

适合： - 传感器数据流 - 机器人状态广播 - Telemetry / 监控流 -
视觉帧流（允许掉帧）

不适合： - 任务分发 - 事务处理 - RPC - 任何“必须处理每一条消息”的系统

如果需要可靠性： - 使用 PUSH/PULL（任务队列语义） - 或 DEALER/ROUTER +
应用层 ACK

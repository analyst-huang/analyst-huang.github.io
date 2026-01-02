---
title: "ELBO：证据、隐变量与变分下界的统一视角"
date: 2026-01-02
draft: false
math: true
---

# ELBO：证据、隐变量与变分下界的统一视角

本文给出一个可重复推导、可迁移到多种 AI 场景（VAE、世界模型、序列潜变量模型、变分推断等）的 ELBO（Evidence Lower Bound）理解框架。核心主线是：

1. 训练目标始终是最大化 **证据**（边缘似然）。
2. 隐变量不是深度学习才有的“工程拆解”，而是统计建模与推断的长期核心工具；ELBO 则是经典“下界化 + 可优化”范式的现代实现。
3. ELBO 中显式出现的先验 KL 与“逼近真实后验”的 KL 并不矛盾：前者是目标函数的结构项，后者是 ELBO 与证据之间的缺口（gap）。

---

## 1. “证据”到底是什么

给定观测数据 $x$ 与生成模型参数 $\theta$，所谓 **证据（evidence）**是数据在模型下出现的概率：
$p_\theta(x)$


它也常被称为 **边缘似然（marginal likelihood）**、**模型证据（model evidence）**。当模型含潜变量 $z$ 时，证据是对潜变量积分（或求和）后的量：

{{< math >}}
$p_\theta(x)=\int p_\theta(x,z)\,dz$
{{< /math >}}

如果进一步将联合分布写成“先验 + 条件似然”的形式：

{{< math >}}
$p_\theta(x,z)=p_\theta(x\mid z)\,p(z)$
{{< /math >}}

则证据变为：

{{< math >}}
$p_\theta(x)=\int p_\theta(x\mid z)\,p(z)\,dz$
{{< /math >}}

这句话的统计含义非常直接：**模型整体（在不知道真实潜变量的情况下）生成 $x$ 的能力**。在贝叶斯公式中，它是后验归一化因子：

{{< math >}}
$p_\theta(z\mid x)=\frac{p_\theta(x\mid z)p(z)}{p_\theta(x)}$
{{< /math >}}

因此，“证据”并不是某个特定解释 $z^\*$ 的质量，而是**所有可能解释对 $x$ 的总体支持度**。

---

## 2. 隐变量在统计中的地位：不是工程权宜，而是核心范式

隐变量（latent variables）在统计中长期处于中心位置，原因主要有两类：

### 2.1 结构建模：世界里确实有不可观测的量

典型例子包括：

- **混合模型**：数据来自多个未观测群体（类别标签不可见）。
- **因子分析**：观测维度相关来自共享的少数潜因子。
- **状态空间模型 / HMM**：系统有不可见状态，观测只是状态的噪声投影。
- **随机效应 / 分层模型**：个体差异（或组间差异）作为潜变量进入模型。

这些模型并不是为了“让概率可拆解”，而是为了让模型表达能力与科学解释更贴近现实机制。

### 2.2 计算装置：data augmentation 与 complete-data trick

即便隐变量不具备强语义，它也常被当作“计算装置”：直接处理边缘似然 $p_\theta(x)$ 很难，但“假装看到了完整数据 $(x,z)$”后，联合似然 $p_\theta(x,z)$ 往往更易处理。EM 算法正是这一思想的经典实例；而 ELBO 与 EM 在数学上存在直接对应（见第 6 节）。

---

## 3. 为什么需要 ELBO：证据难算、难优化

最大似然学习的目标并没有因为引入潜变量而改变。对单样本（或数据集求和）而言，目标仍是最大化对数证据：

{{< math >}}
$\max_\theta \log p_\theta(x)$
{{< /math >}}

困难在于：

{{< math >}}
$\log p_\theta(x)=\log\int p_\theta(x,z)\,dz$
{{< /math >}}

高维连续潜空间下该积分通常不可解析；即便使用蒙特卡洛，梯度估计方差也会很高。ELBO 的作用是把这个不可直接优化的目标，变成一个可计算、可微、可用随机梯度优化的下界目标。

---

## 4. ELBO 的推导：从证据到下界

引入任意分布 $q_\phi(z\mid x)$（变分分布或推断网络），做一个恒等变形：

{{< math >}}
$\log p_\theta(x)
=
\log \int q_\phi(z\mid x)\frac{p_\theta(x,z)}{q_\phi(z\mid x)}\,dz$
{{< /math >}}

由于对数函数凹，使用 Jensen 不等式得到下界：

{{< math >}}
$\log p_\theta(x)
\ge
\mathbb E_{q_\phi(z\mid x)}
\left[
\log p_\theta(x,z)-\log q_\phi(z\mid x)
\right]$
{{< /math >}}

定义右侧为 ELBO：

{{< math >}}
$\mathcal L(\theta,\phi)
=
\mathbb E_{q_\phi(z\mid x)}
\left[
\log p_\theta(x,z)-\log q_\phi(z\mid x)
\right]$
{{< /math >}}

展开联合分布 $\log p_\theta(x,z)=\log p_\theta(x\mid z)+\log p(z)$ 后得到最常用形式：

{{< math >}}
$\mathcal L(\theta,\phi)
=
\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
-
\mathrm{KL}\bigl(q_\phi(z\mid x)\,\|\,p(z)\bigr)$
{{< /math >}}

---

## 5. 两个 KL：一个在 ELBO 里，一个是 ELBO 与证据的缺口

一个常见困惑是：ELBO 里为何出现的是

{{< math >}}
$-\mathrm{KL}\bigl(q_\phi(z\mid x)\,\|\,p(z)\bigr)$
{{< /math >}}

而不是

{{< math >}}
$-\mathrm{KL}\bigl(q_\phi(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$
{{< /math >}}

关键在于：后者确实与 ELBO 紧密相关，但它不作为“显式项”出现，而是作为 **缺口（gap）**精确地刻画 ELBO 的松紧：

{{< math >}}
$\log p_\theta(x)
=
\mathcal L(\theta,\phi)
+
\mathrm{KL}\bigl(q_\phi(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$
{{< /math >}}

因此：
- ELBO 永远是下界，因为 KL 非负。
- 下界变紧当且仅当 $q_\phi(z\mid x)=p_\theta(z\mid x)$。

更重要的是，当 $\theta$ 固定时，$\log p_\theta(x)$ 与 $\phi$ 无关，因此最大化 ELBO 等价于最小化该缺口：

{{< math >}}
$\arg\max_\phi \mathcal L(\theta,\phi)
=
\arg\min_\phi \mathrm{KL}\bigl(q_\phi(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$
{{< /math >}}

---

---

## 附录：引入变分分布是否只是技术手段？

在 ELBO 的推导中，变分分布 $q_\phi(z\mid x)$ 往往以如下方式出现：  
为了处理难以计算的边缘似然
{{< math >}}
$\log p_\theta(x)=\log\int p_\theta(x,z)\,dz$
{{< /math >}}
人为引入一个分布并利用 Jensen 不等式构造下界。从形式上看，这一步确实带有明显的“技术性”色彩。

但如果仅将其理解为数学技巧，就会遗漏变分推断在统计学中更根本的含义。

---

### 一、计算动机：它解决了“边缘化不可计算”的问题

在含隐变量模型中，直接优化 $\log p_\theta(x)$ 通常不可行。引入 $q(z\mid x)$ 后，可以将对数积分改写为期望形式，并得到 ELBO：

{{< math >}}
$\mathcal L(\theta,q)
=
\mathbb E_{q(z\mid x)}[\log p_\theta(x,z)-\log q(z\mid x)]$
{{< /math >}}

在这一层面上，$q$ 的确是一个**为可计算性服务的辅助对象**。但这并不能解释：  
为什么 $q$ 被视为“后验近似”，而不是任意权重函数。

---

### 二、统计解释：$q(z\mid x)$ 是一个近似后验，而非随意分布

关键事实在于，ELBO 与证据之间存在如下**精确恒等分解**：

{{< math >}}
$\log p_\theta(x)
=
\mathcal L(\theta,q)
+
\mathrm{KL}\bigl(q(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$
{{< /math >}}

这一定义并非事后附会，而是直接来自概率恒等式。其含义是：

- ELBO 与真实目标（证据）的差距，**完全由 $q$ 与真实后验的 KL 决定**；
- 当 $\theta$ 固定时，最大化 ELBO 等价于最小化
  {{< math >}}
  $\mathrm{KL}\bigl(q(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$
  {{< /math >}}

因此，在统计意义上，引入 $q(z\mid x)$ 并不是随意的：

> 它是在你允许的分布族中，选择一个**最接近真实后验的、可计算的近似**。

这正是变分推断（variational inference）作为推断方法的核心定义。

---

### 三、为什么 ELBO 中出现的是 $\mathrm{KL}(q\|p(z))$？

在 ELBO 的常见展开形式中，显式出现的是：

{{< math >}}
$\mathbb E_{q(z\mid x)}[\log p_\theta(x\mid z)]
-
\mathrm{KL}\bigl(q(z\mid x)\,\|\,p(z)\bigr)$
{{< /math >}}

而不是直接出现 $\mathrm{KL}\bigl(q(z\mid x)\,\|\,p_\theta(z\mid x)\bigr)$。这是因为：

- 后者已经被“吸收”进证据与 ELBO 的差额之中；
- 前者将后验近似与先验结构绑定，从而保证：
  - 潜变量表示可采样；
  - 学到的表示在整体生成模型下是自洽的。

这并不是改变目标，而是将“逼近真实后验”和“保证生成一致性”这两件事分解为显式项与隐含项。

---

### 小结

引入变分分布 $q(z\mid x)$ 的确始于计算需求，但其合理性并不止于技巧层面：

- 它在统计上对应一个明确的后验近似问题；
- ELBO 精确刻画了该近似与真实后验之间的差距；
- 在现代 AI 中，$q$ 被进一步参数化并摊销，从而成为可扩展的推断机制。

因此，更准确的说法是：
> **变分分布不是“为了 ELBO 而引入的技巧”，    
> 而是 ELBO 所对应的近似推断立场本身。    
> 是我们在认识论上允许自己用什么结构来认识分布。**


---

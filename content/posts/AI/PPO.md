---

title: "PPO：策略梯度、重要性采样与 Clip"
date: 2025-12-31
draft: false
math: true
----------

# PPO 中的策略梯度、重要性采样与概率密度比

> 从策略梯度定理出发，经由重要性采样与“对梯度的不定积分”，理解 PPO 的 surrogate objective 与 Clip 机制。

---

## 1. 策略梯度定理：起点而不是终点

策略梯度定理给出的是**梯度形式**，而不是一个可直接优化的损失函数：

{{< math >}}
$$
\nabla_\theta J(\theta)
= \mathbb E_{\pi_\theta}
\big[
\nabla_\theta \log \pi_\theta(a_t\mid s_t), A^\pi(s_t,a_t)
\big].
$$
{{< /math >}}

这一定理说明了：

* 梯度方向由 $ \nabla_\theta \log \pi $决定；
* 学习信号由优势函数 $A$ 提供；
* 它本质上是 **on-policy** 的结论。

但工程上我们并不是直接“写梯度”，而是希望：

> 构造一个目标函数 $L(\theta)$，使其梯度自动给出合理的策略更新。

这正是 PPO / TRPO 所做的事情。

---

## 2. 从 on-policy 到 off-policy：重要性采样的引入

在实践中：

* rollout 使用的是旧策略 $ \pi_{\text{old}} $；
* 更新时参数已经变为 $ \pi_\theta $。

于是需要通过重要性采样来修正期望的测度：

{{< math >}}
$$
\mathbb E_{\pi_\theta}[f(s,a)]
=
\mathbb E_{\pi_{\text{old}}}
\left[
\frac{\pi_\theta(a\mid s)}{\pi_{\text{old}}(a\mid s)}
f(s,a)
\right].
$$
{{< /math >}}

定义**重要性采样率（概率比 / 密度比）**：

{{< math >}}
$$
\boxed{
r_t(\theta)
= \frac{\pi_\theta(a_t\mid s_t)}{\pi_{\text{old}}(a_t\mid s_t)}
}
$$
{{< /math >}}

策略梯度于是可以写为：

{{< math >}}
$$
\mathbb E_{\pi_{\text{old}}}
\big[
r_t(\theta),
\nabla_\theta \log \pi_\theta(a_t\mid s_t),
\hat A_t
\big].
$$
{{< /math >}}

---

## 3. 对梯度“积分”：surrogate objective 的自然出现

注意一个关键恒等式：

{{< math >}}
$$
\nabla_\theta r_t(\theta)
=r_t(\theta),
\nabla_\theta \log \pi_\theta(a_t\mid s_t).
$$
{{< /math >}}

于是上面的梯度可以重写为：

{{< math >}}
$$
\nabla_\theta,
\mathbb E_{\pi_{\text{old}}}
\big[
r_t(\theta),\hat A_t
\big].
$$
{{< /math >}}

这意味着，我们可以定义一个**可积的 surrogate objective**：

{{< math >}}
$$
\boxed{
L^{\text{PG-IS}}(\theta)
=

\mathbb E_{\pi_{\text{old}}}
\big[
r_t(\theta),\hat A_t
\big]
}
$$
{{< /math >}}

它满足：

{{< math >}}
$$
\nabla_\theta L^{\text{PG-IS}}(\theta)
=

\mathbb E_{\pi_{\text{old}}}
\big[
r_t(\theta),
\nabla_\theta \log \pi_\theta(a_t\mid s_t),
\hat A_t
\big].
$$
{{< /math >}}

这一步可以理解为：

> **从策略梯度出发，对梯度进行不定积分，得到一个 surrogate 损失函数。**

TRPO 与 PPO 的分歧，从这里才真正开始。

---

## 4. 为什么这个 surrogate objective 不安全？

单个样本的目标项是：

{{< math >}}
$$
\ell_t(\theta)
=

r_t(\theta),\hat A_t.
$$
{{< /math >}}

问题在于：

* 当 $ \hat A_t > 0 $ 时，优化会推动 $ r_t \to +\infty $；
* 当 $ \hat A_t < 0 $ 时，优化会推动 $ r_t \to 0 $；
* $ r_t $ 对参数的依赖是指数型的（通过 log-prob）。

结论是：

> $L^{\text{PG-IS}}$ 在一阶近似上是正确的，但在数值优化中是**高度不受控的**。

TRPO 通过显式 KL 约束来解决；PPO 则选择了一条更工程化的路径。

---

## 5. PPO-Clip：逐样本的“信任域”近似

PPO 的核心思想不是直接约束 KL，而是：

> **限制每一个样本对策略更新的影响力。**

具体做法是：

* 只关注概率比 $r_t$；
* 要求其不要偏离 1 太远。

定义允许区间：

{{< math >}}
$$
r_t(\theta) \in [1-\epsilon,; 1+\epsilon].
$$
{{< /math >}}

并构造逐样本的分段目标：

{{< math >}}
$$
\boxed{
\ell_t^{\text{CLIP}}(\theta)
=

\min\Big(
r_t(\theta)\hat A_t,;
\text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t
\Big)
}
$$
{{< /math >}}

整体目标为：

{{< math >}}
$$
L^{\text{CLIP}}(\theta)
=

\mathbb E_t
\big[
\ell_t^{\text{CLIP}}(\theta)
\big].
$$
{{< /math >}}

---

## 6. 分段展开：Clip 到底在“杀死”什么梯度？

### 情形一：$ \hat A_t > 0 $

{{< math >}}
$$
\ell_t^{\text{CLIP}}(\theta)
=

\begin{cases}
r_t(\theta)\hat A_t, & r_t \le 1+\epsilon \
(1+\epsilon)\hat A_t, & r_t > 1+\epsilon
\end{cases}
$$
{{< /math >}}

* 合理提升概率：正常策略梯度；
* 提升过度：目标变为常数，梯度为 **0**。

### 情形二：$ \hat A_t < 0 $

{{< math >}}
$$
\ell_t^{\text{CLIP}}(\theta)
=

\begin{cases}
r_t(\theta)\hat A_t, & r_t \ge 1-\epsilon \
(1-\epsilon)\hat A_t, & r_t < 1-\epsilon
\end{cases}
$$
{{< /math >}}

* 合理压低概率：正常梯度；
* 压低过度：梯度直接消失。

**关键结论：**

> PPO-Clip 不是“减小梯度”，而是在危险区间**直接将梯度设为 0**。

---

## 7. 连续动作下的真实含义：概率密度比

在连续动作（高斯策略）下：

{{< math >}}
$$
\pi_\theta(a\mid s)
$$
{{< /math >}}

并不是概率，而是**概率密度**。因此：

{{< math >}}
$$
r_t(\theta)
=

\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\text{old}}(a_t\mid s_t)}
$$
{{< /math >}}

严格来说是 **概率密度比（Radon–Nikodym derivative）**。

工程实现中一定使用 log-density：

{{< math >}}
$$
\log r_t
=
 \log \pi_\theta(a_t\mid s_t)
\log \pi_{\text{old}}(a_t\mid s_t).
$$
{{< /math >}}

PPO-Clip 的含义于是变为：

> **限制新旧策略在已采样动作点处的相对密度变化幅度。**

---

## 8. 是否可以不使用重要性采样率？

* 如果 rollout 数据在策略完全未变的情况下**只更新一次**：

  * 理论上不需要 $r_t$；
  * 算法退化为 A2C / vanilla policy gradient。

* PPO 的设计目标是：

  * 同一批 rollout 数据
  * 允许多 epoch / mini-batch 更新

这本质上已经是 **弱离策略**，因此：

> $r_t$ 是为了“数据复用”而付出的代价，而 Clip 是对这个代价的安全约束。

---

## 9. 总结

* 策略梯度定理给出的是梯度结构；
* 重要性采样把 on-policy 梯度扩展到近似 off-policy；
* 对梯度不定积分自然得到 surrogate objective；
* PPO-Clip 是在该 surrogate 上施加逐样本的信任域近似；
* 在连续动作下，一切概率比都应理解为**概率密度比**。

**一句话总结：**

> PPO = Policy Gradient + Importance Sampling + Sample-wise Trust Region。

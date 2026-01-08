---
title: "Diffusion"
date: 2026-01-08
draft: False 
---

{{< math >}}
$x_t = \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1 - \bar{\alpha}_t}\, \varepsilon,\quad \varepsilon \sim \mathcal{N}(0, I)$
{{< /math >}}

其中：

{{< math >}}
$\alpha_t = 1 - \beta_t,\quad \bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$
{{< /math >}}

## 二、严格推导：用贝叶斯公式（forward 后验）

### 1) 概率图结构与贝叶斯展开

从概率图（forward 链）：
{{< math >}}
$
x_0 \rightarrow x_{t-1} \rightarrow x_t
$
{{< /math >}}

由贝叶斯公式：
{{< math >}}
$
q(x_{t-1}\mid x_t, x_0)
=
\frac{q(x_t\mid x_{t-1}, x_0)\,q(x_{t-1}\mid x_0)}{q(x_t\mid x_0)}.
$
{{< /math >}}

由于 forward 过程的马尔可夫性：
{{< math >}}
$
q(x_t\mid x_{t-1}, x_0)=q(x_t\mid x_{t-1}),
$
{{< /math >}}
因此：
{{< math >}}
$
q(x_{t-1}\mid x_t, x_0)
=
\frac{q(x_t\mid x_{t-1})\,q(x_{t-1}\mid x_0)}{q(x_t\mid x_0)}.
$
{{< /math >}}

---

### 2) 三个分布都是已知高斯

记
{{< math >}}
$
\alpha_t = 1-\beta_t,\qquad \bar\alpha_t=\prod_{s=1}^t \alpha_s.
$
{{< /math >}}

forward 单步：
{{< math >}}
$
q(x_t\mid x_{t-1})=\mathcal N(\sqrt{\alpha_t}\,x_{t-1},\ \beta_t I).
$
{{< /math >}}

forward 边缘（闭式）：
{{< math >}}
$
q(x_{t-1}\mid x_0)=\mathcal N(\sqrt{\bar\alpha_{t-1}}\,x_0,\ (1-\bar\alpha_{t-1})I),
$
{{< /math >}}
{{< math >}}
$
q(x_t\mid x_0)=\mathcal N(\sqrt{\bar\alpha_t}\,x_0,\ (1-\bar\alpha_t)I).
$
{{< /math >}}

于是：
{{< math >}}
$
q(x_{t-1}\mid x_t, x_0)
\propto
q(x_t\mid x_{t-1})\,q(x_{t-1}\mid x_0)
$
{{< /math >}}
是“高斯 × 高斯”的形式，因此后验仍为高斯：
{{< math >}}
$
q(x_{t-1}\mid x_t, x_0)
=
\mathcal N\!\big(\mu_t(x_t,x_0),\ \tilde\beta_t I\big).
$
{{< /math >}}

---

### 3) 后验均值与方差（DDPM 经典闭式）

后验方差：
{{< math >}}
$
\tilde\beta_t
=
\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\,\beta_t.
$
{{< /math >}}

后验均值：
{{< math >}}
$
\mu_t(x_t,x_0)
=
\frac{\sqrt{\bar\alpha_{t-1}}\,\beta_t}{1-\bar\alpha_t}\,x_0
+
\frac{\sqrt{\alpha_t}\,(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}\,x_t.
$
{{< /math >}}

---

### 4) 小结

我们严格地从：
{{< math >}}
$
q(x_{t-1}\mid x_t,x_0)
=
\frac{q(x_t\mid x_{t-1})\,q(x_{t-1}\mid x_0)}{q(x_t\mid x_0)}
$
{{< /math >}}
出发，利用 forward 马尔可夫性与高斯闭包性，得到
{{< math >}}
$
q(x_{t-1}\mid x_t,x_0)=\mathcal N(\mu_t,\tilde\beta_t I),
$
{{< /math >}}

## 噪声预测 ≡ score matching（严格等价）

我们看训练目标（DDPM 常用的 noise-prediction loss）：

{{< math >}}
$
L(\theta)=\mathbb{E}_{x_0,\varepsilon,t}\,\|\varepsilon-\varepsilon_\theta(x_t,t)\|_2^2,
\qquad
x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\ \ \varepsilon\sim\mathcal N(0,I).
$
{{< /math >}}

---

## 1) 最优解是什么？

对固定的 $t$ 与观测到的 $x_t$，这是一个**条件均方误差（conditional MSE）**问题。
令 $f(x_t,t)=\varepsilon_\theta(x_t,t)$。在平方损失下的唯一（几乎处处）最优解为条件期望：

{{< math >}}
$
\varepsilon_\theta^\star(x_t,t)=\mathbb{E}[\varepsilon\mid x_t,t].
$
{{< /math >}}

（直观：平方损失的回归最优预测 = 条件均值。）

---

## 2) 严格推出：$\mathbb{E}[\varepsilon\mid x_t]$ 与 score 的关系

由（Vincent 2011 / Tweedie 公式的形式）：

{{< math >}}
$
\boxed{
\mathbb{E}[\varepsilon\mid x_t]
=
-\sqrt{1-\bar\alpha_t}\ \nabla_{x_t}\log p_t(x_t)
}
$
{{< /math >}}

---

## 3) 把它写成 “噪声预测 ↔ score” 的等式

因为训练使得 $\varepsilon_\theta(x_t,t)\approx \mathbb{E}[\varepsilon\mid x_t]$，于是

{{< math >}}
$
\boxed{
s_\theta(x_t,t)\ \approx\ \nabla_{x_t}\log p_t(x_t)
=
-\frac{1}{\sqrt{1-\bar\alpha_t}}\ \varepsilon_\theta(x_t,t)
}
$
{{< /math >}}

也即

{{< math >}}
$
\boxed{
\varepsilon_\theta(x_t,t)\ \approx\ -\sqrt{1-\bar\alpha_t}\ s_\theta(x_t,t)
}
$
{{< /math >}}

---

## 5) 一句话直觉

- noise-prediction 回归到 $\mathbb{E}[\varepsilon\mid x_t]$
- 由于高斯卷积的解析性质，这个条件均值**等价于**边缘密度 $p_t$ 的 score（差一个确定系数）
- 所以 “预测噪声” 和 “score matching” 在这里是严格同一件事（只是参数化形式不同）

最常用的 DDPM 采样写法是：

{{< math >}}
$
x_{t-1}
=
\frac{1}{\alpha_t}
\Big(
x_t
-
\frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}
\,
\varepsilon_\theta(x_t, t)
\Big)
+
\sigma_t z,
\quad
z \sim \mathcal{N}(0, I)
$
{{< /math >}}

### 3) 用 score 来写同一条公式（更直观）

把上面第 (1) 条代进去，你会看到反向一步大致就是：

{{< math >}}
$
x_{t-1}
\;\approx\;
\underbrace{\frac{1}{\alpha_t} x_t}_{\text{线性“去衰减”}}
\;+\;
\underbrace{\frac{\beta_t}{\alpha_t}\, s_\theta(x_t, t)}_{\text{沿 score 往高概率区推}}
\;+\;
\underbrace{\sigma_t z}_{\text{随机性（保留多解/多模态）}},
\quad z \sim \mathcal{N}(0, I)
$
{{< /math >}}

这就是你想要的直觉把握：

- **score 项**：告诉你往哪里走更像数据（往高密度区推）
- **随机项**：保证你不是“爬山爬到某个峰就塌缩”，而是能覆盖分布的不同模式
- **线性项**：对应正向里那一点点缩放/衰减的逆操作

# 一、一步去噪：从 $x_t$ 得到“当前认为的 clean sample”

你现在已经知道网络在预测噪声：

{{< math >}}
$
\varepsilon_\theta(x_t, t)
$
{{< /math >}}

标准的一步去噪公式就是直接把噪声“减掉”：

{{< math >}}
$
\hat{x}_0(x_t)
=
\frac{1}{\sqrt{\bar{\alpha}_t}}
\left(
x_t
-
\sqrt{1 - \bar{\alpha}_t}\;
\varepsilon_\theta(x_t, t)
\right)
$
{{< /math >}}

直觉理解：

- $ x_t $：现在这个带噪的样本  
- $ \varepsilon_\theta $：模型认为“这里面有多少是噪声”  
- $ \hat{x}_0 $：在第 $t$ 步，模型心中“最可能的干净样本”

> **重要强调（防止误解）：**  
> $ \hat{x}_0 $ 不是最终生成结果，  
> 它只是当前这一步的“临时 clean 解释”。

---

# 二、Guidance 的核心思想（一句话版）

现在假设你有一个目标函数（或损失）：

{{< math >}}
$
L(x_0) \quad \text{或} \quad R(x_0)
$
{{< /math >}}

例如：

- 和目标图像的距离  
- 是否满足某个约束  
- 轨迹 reward  
- classifier 的 log-prob

**Guidance 的思想只有一句话：**

> 既然我已经能在每一步得到一个 $ \hat{x}_0 $，  
> 那我就可以在“采样过程中”  
> 对这个 $ \hat{x}_0 $ 施加梯度修正。

---

# 三、梯度是怎么真正“进 sample 过程”的？

这是关键部分，分三步。

---

## 1️⃣ 先在 clean space 里算梯度

先在干净空间计算梯度：

{{< math >}}
$
g
=
\nabla_{\hat{x}_0}\, \big( - L(\hat{x}_0) \big)
$
{{< /math >}}

如果是 reward，则是：

{{< math >}}
$
\nabla_{\hat{x}_0}\, R(\hat{x}_0)
$
{{< /math >}}

**直觉：**

这个梯度告诉你：  
如果我是一个干净样本，往哪里动能让 loss 变小 / reward 变大。

---

## 2️⃣ 把梯度“传回”到当前噪声层

关键关系是：

{{< math >}}
$
\hat{x}_0
=
\frac{1}{\sqrt{\bar{\alpha}_t}} x_t
-
\frac{\sqrt{1-\bar{\alpha}_t}}{\sqrt{\bar{\alpha}_t}}
\varepsilon_\theta(x_t, t)
$
{{< /math >}}

对 $ x_t $ 求导：

{{< math >}}
$
\frac{\partial \hat{x}_0}{\partial x_t}
=
\frac{1}{\sqrt{\bar{\alpha}_t}} I
$
{{< /math >}}

于是梯度回传非常简单：

{{< math >}}
$
\nabla_{x_t}\, \big( - L(\hat{x}_0) \big)
=
\frac{1}{\sqrt{\bar{\alpha}_t}}
\nabla_{\hat{x}_0}\, \big( - L(\hat{x}_0) \big)
$
{{< /math >}}

这一步本质上是在做：

> 把 clean-space 的偏好，线性映射回当前噪声层。

---

## 3️⃣ 把 guidance 梯度加进反向采样

标准反向采样（score 形式，忽略常数细节）：

{{< math >}}
$
x_{t-1}
\approx
\frac{1}{\alpha_t} x_t
+
\frac{\beta_t}{\alpha_t} \, s_\theta(x_t, t)
+
\sigma_t z
$
{{< /math >}}

其中：

{{< math >}}
$
s_\theta(x_t, t) = \nabla_{x_t} \log p(x_t)
$
{{< /math >}}

加入 guidance 后：

{{< math >}}
$
x_{t-1}
\approx
\frac{1}{\alpha_t} x_t
+
\frac{\beta_t}{\alpha_t}
\left(
s_\theta(x_t, t)
+
\lambda \, \nabla_{x_t} ( - L(\hat{x}_0) )
\right)
+
\sigma_t z
$
{{< /math >}}

其中：

- $ \lambda $：guidance strength（主要调这个）

解释：

- 原本的 score 项：  
  → “像数据分布的方向”
- 新加的 guidance 梯度：  
  → “更符合任务目标的方向”

采样时两股力一起拉着样本往前走。

---

# 一句话总直觉总结

1. 模型告诉你：现在这个 $x_t$ 最可能来自哪个 $\hat{x}_0$  
2. 你在 $\hat{x}_0$ 上计算任务梯度  
3. 通过线性关系把梯度传回 $x_t$  
4. 在反向扩散时把这个方向加进 drift

所以 guidance 不是改训练目标，  
而是**在采样 ODE / SDE 里直接改速度场方向**。


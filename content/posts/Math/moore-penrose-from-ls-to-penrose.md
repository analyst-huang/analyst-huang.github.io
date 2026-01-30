---
title: "从最小二乘到 Penrose 四条件：摩尔–彭若斯逆的几何证明路线"
date: 2026-01-30
tags: ["Linear Algebra", "Least Squares", "Pseudoinverse", "Moore-Penrose"]
math: true
---

> 这篇笔记按**证明顺序**组织：  
> **最小二乘 ⇒ 正交投影**，**最小范数 ⇒ 与 kernel 正交**，  
> 进而“自然构造”出 $A^+$，再推出 **Penrose 四条件**与**唯一性**，并回答“会不会无解”。

---

## 1. 问题动机：为什么摩尔逆看上去“旱地拔葱”？

如果只从“广义逆”的等式出发，Penrose 四条件

{{< math >}}
$
AXA=A,\quad XAX=X,\quad (AX)^\top=AX,\quad (XA)^\top=XA
$
{{< /math >}}

像是凭空列出的约束。更自然的起点其实是一个极其朴素的问题：

> 给定 $A\in\mathbb{R}^{m\times n}$ 与 $b\in\mathbb{R}^m$，  
> 先求最小二乘 $\min_x \|Ax-b\|_2$；若解不唯一，再在所有最小二乘解中选范数最小的那个。

这条路线会把“代数等式”还原成“几何投影”。

---

## 2. 最小二乘 ⇒ 残差与列空间正交（正交投影）

考虑目标函数

{{< math >}}
$
f(x)=\|Ax-b\|_2^2=(Ax-b)^\top(Ax-b).
$
{{< /math >}}

令残差 $r(x)=Ax-b$。对 $x$ 求梯度：

{{< math >}}
$
\nabla f(x)=2A^\top(Ax-b)=2A^\top r(x).
$
{{< /math >}}

此处补充一个求矩阵函数梯度的小技巧：
{{<math>}}
$$
f(x + \delta) - f(x) = \langle \nabla f(x), \delta\rangle + o(infinitesimal)
$$
{{</math>}}
只要表示为这个形式，就能够知道梯度是什么。

若 $x_*$ 为极小点，则一阶必要条件

{{< math >}}
$
A^\top(Ax_*-b)=0\quad\Longleftrightarrow\quad A^\top r_*=0.
$
{{< /math >}}

对任意 $y$，列空间中的向量可写为 $Ay$，于是

{{< math >}}
$
(Ay)^\top r_* = y^\top(A^\top r_*) = 0,
$
{{< /math >}}

即

{{< math >}}
$
\boxed{r_*\perp \operatorname{Im}(A)}.
$
{{< /math >}}

又因为 $Ax_*\in \operatorname{Im}(A)$，我们得到分解

{{< math >}}
$
b = Ax_* + r_*,\qquad Ax_*\in \operatorname{Im}(A),\quad r_*\perp \operatorname{Im}(A).
$
{{< /math >}}

这恰好是“正交投影”的定义性刻画，因此

{{< math >}}
$
\boxed{Ax_*=\Pi_{\operatorname{Im}(A)}(b)}.
$
{{< /math >}}

---

## 3. 最小范数 ⇒ 解与 $\ker(A)$ 正交（并且唯一）

当 $A$ 不满列秩时，最小二乘解一般不唯一。取任意一个最小二乘解 $x_0$，可证明所有最小二乘解恰为

{{< math >}}
$
\mathcal{S}=x_0+\ker(A).
$
{{< /math >}}

**证明要点:** 若 $x$ 与 $x_0$ 都满足正规方程 $A^\top A x=A^\top b$，则相减得
$A^\top A(x-x_0)=0\Rightarrow \|A(x-x_0)\|^2=0\Rightarrow x-x_0\in\ker(A)$；反向也成立。

现在在 $\mathcal{S}$ 中最小化范数：

{{< math >}}
$
\min_{z\in\ker(A)}\|x_0+z\|_2.
$
{{< /math >}}

把 $x_0$ 按正交分解写成

{{< math >}}
$
x_0=u+v,\qquad u\in\ker(A)^\perp,\ v\in\ker(A).
$
{{< /math >}}

则对任意 $z\in\ker(A)$，

{{< math >}}
$
\|x_0+z\|^2=\|u+(v+z)\|^2=\|u\|^2+\|v+z\|^2,
$
{{< /math >}}

最小值在 $z_*=-v$ 处取得，最小范数解为

{{< math >}}
$
\boxed{x_* = u \in \ker(A)^\perp}.
$
{{< /math >}}

并且该解唯一：因为正交分解唯一，$u$ 唯一。

利用基本定理

{{< math >}}
$
\ker(A)^\perp = \operatorname{Im}(A^\top),
$
{{< /math >}}

得到一个常用刻画：

{{< math >}}
$
\boxed{x_*(b)\in \operatorname{Im}(A^\top)}.
$
{{< /math >}}

---

## 4. 用最小二乘 + 最小范数定义 $A^+$，并证明映射线性

对每个 $b$，令 $x_*(b)$ 为“最小二乘 + 最小范数”的唯一解。定义算子

{{< math >}}
$
T:\mathbb{R}^m\to\mathbb{R}^n,\qquad T(b)=x_*(b).
$
{{< /math >}}

### 4.1 一个等价的线性系统（核心）

由上面的两条结论，$x_*(b)$ 等价于解下面的系统：

{{< math >}}
$
(\star)\qquad
\begin{cases}
A^\top A x = A^\top b,\\
x\in \operatorname{Im}(A^\top).
\end{cases}
$
{{< /math >}}

- 第一行来自最小二乘的正规方程；
- 第二行来自最小范数选择（砍掉 $\ker(A)$ 分量）。

### 4.2 为什么 $(\star)$ 的解唯一？

若 $x_1,x_2$ 都满足 $(\star)$，令 $d=x_1-x_2$，则

{{< math >}}
$
A^\top A d=0 \Rightarrow d^\top A^\top A d=\|Ad\|^2=0\Rightarrow d\in\ker(A).
$
{{< /math >}}

又 $d\in\operatorname{Im}(A^\top)=\ker(A)^\perp$，所以 $d=0$。

### 4.3 线性性

系统 $(\star)$ 在固定子空间 $\operatorname{Im}(A^\top)$ 上解线性方程，其解对右端 $b$ 线性依赖，因此 $T$ 是线性算子。于是存在唯一矩阵（把线性算子写成矩阵）

{{< math >}}
$
\boxed{A^+\in\mathbb{R}^{n\times m}\ \text{使得}\ T(b)=A^+b}.
$
{{< /math >}}

这就是摩尔–彭若斯逆的“问题驱动”构造。

---

## 5. 两个投影：$P=AA^+$ 与 $Q=A^+A$

### 5.1 $P=AA^+$ 是到 $\operatorname{Im}(A)$ 的正交投影

给定 $b$，设 $x_*=A^+b$，则

{{< math >}}
$
p:=Ax_*=AA^+b\in\operatorname{Im}(A),
\quad r:=b-p=b-AA^+b.
$
{{< /math >}}

由最小二乘正交性，$r\perp \operatorname{Im}(A)$。因此 $p$ 是 $b$ 在 $\operatorname{Im}(A)$ 上的正交投影：

{{< math >}}
$
\boxed{AA^+ = \Pi_{\operatorname{Im}(A)}}.
$
{{< /math >}}

因此 $AA^+$ 必满足

{{< math >}}
$
(AA^+)^2=AA^+,\qquad (AA^+)^\top=AA^+.
$
{{< /math >}}

### 5.2 $Q=A^+A$ 是到 $\operatorname{Im}(A^\top)$ 的正交投影

对任意 $x$，令 $b=Ax$，则

{{< math >}}
$
Qx=A^+Ax=A^+b=x_*(b)\in\operatorname{Im}(A^\top),
$
{{< /math >}}

所以 $Qx$ 的确落在目标子空间中。要证明正交性，只需验证对所有 $y$：

{{< math >}}
$
\langle x-Qx,\ A^\top y\rangle=0.
$
{{< /math >}}

计算：

{{< math >}}
$
\langle x-Qx,\ A^\top y\rangle
=\langle Ax-AQx,\ y\rangle.
$
{{< /math >}}

而接下来会由 Penrose (1)（马上推出）得到 $AQx=Ax$，于是该内积为 0。结论：

{{< math >}}
$
\boxed{A^+A=\Pi_{\operatorname{Im}(A^\top)}}.
$
{{< /math >}}

因此 $A^+A$ 也满足幂等与对称：

{{< math >}}
$
(A^+A)^2=A^+A,\qquad (A^+A)^\top=A^+A.
$
{{< /math >}}

---

## 6. 从投影性质推出 Penrose 四条件

下面按顺序得到四条等式。

### (1) $AA^+A=A$

对任意 $x$，$Ax\in \operatorname{Im}(A)$。而 $AA^+$ 是到 $\operatorname{Im}(A)$ 的正交投影，所以投影不改变它：

{{< math >}}
$
AA^+(Ax)=Ax\quad\forall x \ \Rightarrow\ AA^+A=A.
$
{{< /math >}}

### (3) $(AA^+)^\top=AA^+$

正交投影算子自伴（对称），故成立。

### (2) $A^+AA^+=A^+$

对任意 $b$，令 $x=A^+b$。由构造 $x\in\operatorname{Im}(A^\top)$。而 $A^+A$ 是到 $\operatorname{Im}(A^\top)$ 的正交投影，所以

{{< math >}}
$
A^+A(A^+b)=A^+b\quad\forall b\ \Rightarrow\ A^+AA^+=A^+.
$
{{< /math >}}

### (4) $(A^+A)^\top=A^+A$

同理，正交投影对称。

至此，$A^+$ 满足 Penrose 四条件。

---

## 7. 仅用 Penrose 四条件证明唯一性

现在抛开最小二乘构造，纯粹从四条件出发证明：若 $X,Y$ 都满足四条件，则 $X=Y$。

### 7.1 先证明 $AX=AY$

由 (1)(3)，$AX$ 与 $AY$ 都是对称幂等矩阵，即正交投影。并且由 $AXA=A$ 可知

{{< math >}}
$
\operatorname{Im}(AX)=\operatorname{Im}(A),
$
{{< /math >}}

所以二者都是到同一子空间 $\operatorname{Im}(A)$ 的正交投影。正交投影唯一，故

{{< math >}}
$
\boxed{AX=AY}.
$
{{< /math >}}

### 7.2 再证明 $XA=YA$

同理由 (2)(4)，$XA$ 与 $YA$ 都是到 $\operatorname{Im}(A^\top)$ 的正交投影，因此

{{< math >}}
$
\boxed{XA=YA}.
$
{{< /math >}}

### 7.3 “夹逼”得到 $X=Y$

利用 (2)：

{{< math >}}
$
X=XAX.
$
{{< /math >}}

把中间的 $AX$ 换成 $AY$（因为 $AX=AY$）：

{{< math >}}
$
X=XAY.
$
{{< /math >}}

同理，对 $Y$，由 (2) 得 $Y=YAY$，把左边的 $YA$ 换成 $XA$（因为 $YA=XA$）：

{{< math >}}
$
Y=XAY.
$
{{< /math >}}

因此

{{< math >}}
$
\boxed{X=XAY=Y}.
$
{{< /math >}}

---

## 8. 会不会无解？（存在性）

在**有限维**的实/复内积空间里，Penrose 四条件**永远有解**，并且由上一节知道**解唯一**。

存在性的“构造性证明”有两条常见路线：

1. **最小二乘 + 最小范数路线（本文）**：对每个 $b$ 存在唯一 $x_*(b)$，且映射 $b\mapsto x_*(b)$ 线性，于是得到矩阵 $A^+$，并验证四条件。
2. **SVD 显式构造**：$A=U\Sigma V^\top$，定义 $\Sigma^+$ 将非零奇异值取倒数、零奇异值仍为 0，令 $A^+=V\Sigma^+U^\top$，可直接逐条验证四条件。

> 备注：在无限维或缺少内积结构（如一般 Banach 空间）时，“正交投影”不一定存在/唯一，Moore–Penrose 逆可能失败；但在线性代数（有限维矩阵）场景下不会。

---

## 9. 常用等价刻画（备忘）

- 正规方程：最小二乘解满足
{{< math >}}
$
  A^\top(Ax-b)=0.
$
{{< /math >}}
- 最小范数解额外满足
{{< math >}}
$
  x\in \operatorname{Im}(A^\top)=(\ker A)^\perp.
$
{{< /math >}}
- 投影算子：
{{< math >}}
$
  AA^+=\Pi_{\operatorname{Im}(A)},\qquad A^+A=\Pi_{\operatorname{Im}(A^\top)}.
$
{{< /math >}}
- 对称幂等 $\Leftrightarrow$ 正交投影：
{{< math >}}
$
  P^2=P,\ P^\top=P \quad\Longleftrightarrow\quad P=\Pi_{\operatorname{Im}(P)}.
$
{{< /math >}}

---

## 10. 小结

按“证明顺序”的一条主线是：

1. 最小二乘 ⇒ 残差正交 ⇒ 正交投影到 $\operatorname{Im}(A)$  
2. 最小范数 ⇒ 去掉 $\ker(A)$ 分量 ⇒ 解落在 $\operatorname{Im}(A^\top)$  
3. 得到线性算子 $b\mapsto x_*(b)$，写成矩阵 $A^+$  
4. $AA^+$ 与 $A^+A$ 识别为两个正交投影  
5. 推出 Penrose 四条件  
6. 仅由四条件可反推唯一性

这就是“摩尔逆不再旱地拔葱”的完整闭环。

---

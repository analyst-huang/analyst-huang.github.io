---
title: "微分IK"
date: 2026-01-30
math: true
---

# 微分 IK（Differential IK）与 Adjoint：从最小二乘到坐标系变换的一条线

> 这篇文章把一次完整的推导链条拼起来：  
> **微分 IK**在算什么 → **最小二乘 / 最小范数**为何同时出现 → 伪逆在**列满秩/行满秩**下如何推导 → **阻尼最小二乘（DLS）**作为优化问题的闭式解 → 为什么 Jacobian 必须用 **Adjoint** 做坐标系变换 → **Adjoint** 本身如何从“刚体上不同点速度不同”推导出来。  
>
> 读者假设：线性代数、最小二乘、一阶条件、正交投影。

---

## 1. 微分 IK 在解决什么问题？

经典 IK 是“给末端位姿，求关节角”：

{{< math >}}
$
x = f(q),\quad \text{给定 }x_d\Rightarrow \text{求 }q
$
{{< /math >}}

微分 IK 把问题改成“给末端**瞬时速度/误差变化率**，求关节**速度**”：

{{< math >}}
$
\dot{x} = J(q)\,\dot{q}
$
{{< /math >}}

离散实现通常是：

{{< math >}}
$
q_{k+1}=q_k+\dot{q}\,\Delta t
$
{{< /math >}}

其中 $J(q)$ 是 Jacobian，作为线性映射：

{{< math >}}
$
J:\;\dot{q}\mapsto \text{twist（末端瞬时运动）}
$
{{< /math >}}

---

## 2. Jacobian 与 twist：输出不是“普通向量”，而是“有坐标系”的速度

在 3D 刚体运动里，常用 6 维 twist 表示瞬时运动：

{{< math >}}
$
V =
\begin{bmatrix}
\omega\\
v
\end{bmatrix}
\in\mathbb{R}^6
$
{{< /math >}}

- $\omega$：角速度
- $v$：某个**参考点**（reference point）的线速度

关键点：**twist 的数值依赖你在哪个坐标系表达、以及线速度对应哪个参考点**。  
因此 Jacobian 也隐含了“输出 twist 的坐标系”这一选择。

---

## 3. 微分 IK 的核心：线性最小二乘 +（必要时）最小范数

从

{{< math >}}
$
J\dot{q}=\dot{x}
$
{{< /math >}}

出发，真实世界里会遇到：

- $J$ 非方阵（任务维度 $m$ 与关节维度 $n$ 不相等）
- 可能超定/欠定
- 可能奇异（秩不足）

因此更稳健的表述是：

### 3.1 最小二乘误差（projection / normal equation）
{{< math >}}
$
\dot{q}^*=\arg\min_{\dot{q}}\;\|J\dot{q}-\dot{x}\|_2^2
$
{{< /math >}}
一阶条件（法方程）：
{{< math >}}
$
J^T(J\dot{q}-\dot{x})=0
$
{{< /math >}}

这会把残差 $r=\dot{x}-J\dot{q}$ 逼到
{{< math >}}
$
r\perp \mathrm{Im}(J)
$
{{< /math >}}
即把 $\dot{x}$ 正交投影到 $\mathrm{Im}(J)$。

### 3.2 为什么还需要“最小范数”？
当解不唯一时（典型：欠定、冗余机器人），仅靠最小二乘条件无法选出唯一解。  
此时常用 **最小范数** 作为二级准则：

{{< math >}}
$
\boxed{
\min_{\dot{q}}\;\|\dot{q}\|_2
\quad \text{s.t.}\quad J\dot{q}=\dot{x}\;\;(\text{若可行})
}
$
{{< /math >}}

最终得到 Moore–Penrose 伪逆解：
{{< math >}}
$
\dot{q}=J^\dagger \dot{x}
$
{{< /math >}}

---

## 4. 伪逆在两种满秩情形下的推导（列满秩 vs 行满秩）

设 $J\in\mathbb{R}^{m\times n}$。

### 4.1 列满秩（column full rank）：$m\ge n,\ \mathrm{rank}(J)=n$

这是“超定最小二乘”的典型情形。  
目标：
{{< math >}}
$
\min_{\dot{q}}\;\|J\dot{q}-\dot{x}\|^2
$
{{< /math >}}
一阶条件：
{{< math >}}
$
J^T(J\dot{q}-\dot{x})=0
\Rightarrow (J^T J)\dot{q}=J^T\dot{x}
$
{{< /math >}}
列满秩保证 $J^T J$ 可逆，因此解唯一：
{{< math >}}
$
\boxed{
\dot{q}=(J^T J)^{-1}J^T\dot{x}
}
$
{{< /math >}}

### 4.2 行满秩（row full rank）：$m<n,\ \mathrm{rank}(J)=m$

这是“欠定但可实现”的典型情形。此时 $\mathrm{Im}(J)=\mathbb{R}^m$，任意 $\dot{x}$ 都可满足：
{{< math >}}
$
J\dot{q}=\dot{x}
$
{{< /math >}}
但解不唯一（存在零空间）。因此最小二乘误差可以做到 0，问题退化成最小范数约束问题：

{{< math >}}
$
\min_{\dot{q}}\;\|\dot{q}\|^2
\quad \text{s.t.}\quad J\dot{q}=\dot{x}
$
{{< /math >}}

**步骤 1：刻画所有可行解**  
取任意特解 $\dot{q}_0$，所有可行解：
{{< math >}}
$
\dot{q}=\dot{q}_0+z,\quad z\in\ker(J)
$
{{< /math >}}

**步骤 2：最小范数条件给出正交性**  
{{< math >}}
$
\|\dot{q}_0+z\|^2=\|\dot{q}_0\|^2+2\langle \dot{q}_0,z\rangle+\|z\|^2
$
{{< /math >}}
要在 $z\in\ker(J)$ 上最小，必须
{{< math >}}
$
\dot{q}_0\perp\ker(J)
$
{{< /math >}}
利用基本关系：
{{< math >}}
$
\ker(J)^\perp=\mathrm{Im}(J^T)
$
{{< /math >}}
因此最小范数解必在 $\mathrm{Im}(J^T)$ 中，可写为
{{< math >}}
$
\dot{q}=J^T\lambda
$
{{< /math >}}

**步骤 3：代回约束并解出 $\lambda$**  
{{< math >}}
$
J\dot{q}=JJ^T\lambda=\dot{x}
$
{{< /math >}}
行满秩保证 $JJ^T$ 可逆：
{{< math >}}
$
\lambda=(JJ^T)^{-1}\dot{x}
$
{{< /math >}}
得到
{{< math >}}
$
\boxed{
\dot{q}=J^T(JJ^T)^{-1}\dot{x}
}
$
{{< /math >}}

> 这一推导的关键不是“法方程”，而是“最小范数 ⇔ 与零空间正交 ⇔ 落在 $\mathrm{Im}(J^T)$”。

---

## 5. 阻尼最小二乘（DLS / Levenberg–Marquardt）= 一个优化问题的闭式解

伪逆在奇异附近会导致 $\dot{q}$ 爆炸。工程上常用 DLS，把问题改写为：

{{< math >}}
$
\boxed{
\dot{q}^*=\arg\min_{\dot{q}}\;\|J\dot{q}-\dot{x}\|^2+\lambda^2\|\dot{q}\|^2
}
$
{{< /math >}}

对 $\dot{q}$ 求导并令零：
{{< math >}}
$
2J^T(J\dot{q}-\dot{x})+2\lambda^2\dot{q}=0
\Rightarrow (J^T J+\lambda^2 I)\dot{q}=J^T\dot{x}
$
{{< /math >}}

闭式解：
{{< math >}}
$
\boxed{
\dot{q}=(J^T J+\lambda^2 I)^{-1}J^T\dot{x}
}
$
{{< /math >}}

常见等价形式（当你想逆 $m\times m$ 而不是 $n\times n$ 时更划算）：
{{< math >}}
$
\boxed{
\dot{q}=J^T(JJ^T+\lambda^2 I)^{-1}\dot{x}
}
$
{{< /math >}}
且恒等式成立（$\lambda>0$）：
{{< math >}}
$
(J^T J + \lambda^2 I)^{-1}J^T = J^T(JJ^T+\lambda^2 I)^{-1}
$
{{< /math >}}

### 5.1 为什么 $(J^T J+\lambda^2 I)$ 一定可逆？
当 $\lambda>0$：
{{< math >}}
$
v^T(J^T J+\lambda^2 I)v = \|Jv\|^2+\lambda^2\|v\|^2>0\quad(\forall v\ne 0)
$
{{< /math >}}
因此它是对称正定矩阵，必可逆。

> 直觉：把奇异值平方 $\sigma_i^2$ 变成 $\sigma_i^2+\lambda^2$，零也被抬起来。

---

## 6. 冗余与零空间（Null Space）项：把“多余自由度”变成二级目标

当 $n>m$ 时（冗余机器人），满足同一任务的 $\dot{q}$ 不唯一。通解可以写成：

{{< math >}}
$
\boxed{
\dot{q}=J^\dagger \dot{x} + (I-J^\dagger J)\,z
}
$
{{< /math >}}

- $J^\dagger \dot{x}$：完成主任务（最小二乘/最小范数意义）
- $(I-J^\dagger J)$：投影到 $\ker(J)$ 的算子
- $z$：二级目标（避限、最小能量、姿态偏好等）

---

## 7. 为什么 Jacobian 需要 Adjoint：因为 twist 有坐标系，而坐标变换不是简单旋转

同一个刚体运动在不同坐标系下的 twist 数值不同。  
设两坐标系 $\{A\},\{B\}$ 的位姿关系为：

{{< math >}}
$
{}^A T_B=
\begin{bmatrix}
R & p\\
0 & 1
\end{bmatrix}
$
{{< /math >}}

则 twist 的坐标变换满足：

{{< math >}}
$
\boxed{
{}^A V = \mathrm{Ad}_{{}^A T_B}\,{}^B V
}
$
{{< /math >}}

于是 Jacobian 也必须随之变换。因为

{{< math >}}
$
{}^B V = {}^B J\,\dot{q}
\quad\Rightarrow\quad
{}^A V = \mathrm{Ad}\,{}^B J\,\dot{q}
$
{{< /math >}}
对任意 $\dot{q}$ 成立，所以
{{< math >}}
$
\boxed{
{}^A J = \mathrm{Ad}_{{}^A T_B}\,{}^B J
}
$
{{< /math >}}

---

## 8. Adjoint 矩阵怎么推导出来？（不要求你熟悉刚体运动学）

你只需要接受一个事实：

> **刚体在转动时，不同点的线速度不同；离“转动中心”越远，线速度越大。**

### 8.1 从“角速度只做旋转”开始
角速度是向量，坐标变换就是旋转：
{{< math >}}
$
\boxed{\omega_A = R\omega_B}
$
{{< /math >}}

### 8.2 线速度为何会多出一项？（核心）
线速度 $v$ 不是“纯向量旋转”这么简单，因为它依赖于你选的参考点。  
当参考点从 $B$ 原点换到 $A$ 原点时，若刚体有角速度 $\omega$，参考点平移 $p$ 会引入额外线速度：

{{< math >}}
$
\boxed{
v_A = Rv_B + \omega_A\times p
}
$
{{< /math >}}

把 $\omega_A=R\omega_B$ 代入：
{{< math >}}
$
v_A = Rv_B + (R\omega_B)\times p
$
{{< /math >}}

用反对称矩阵表示叉乘：$[p]_\times x=p\times x$，则
{{< math >}}
$
(R\omega_B)\times p = [p]_\times R\omega_B
$
{{< /math >}}
所以
{{< math >}}
$
\boxed{
v_A = Rv_B + [p]_\times R\omega_B
}
$
{{< /math >}}

### 8.3 合并成 6×6 的线性变换
把两行合并：
{{< math >}}
$
\begin{bmatrix}
\omega_A\\
v_A
\end{bmatrix}
=
\underbrace{
\begin{bmatrix}
R & 0\\
[p]_\times R & R
\end{bmatrix}
}_{\mathrm{Ad}_{{}^A T_B}}
\begin{bmatrix}
\omega_B\\
v_B
\end{bmatrix}
$
{{< /math >}}

因此
{{< math >}}
$
\boxed{
\mathrm{Ad}_T=
\begin{bmatrix}
R & 0\\
[p]_\times R & R
\end{bmatrix}
}
$
{{< /math >}}

> 直觉：  
> - 角速度只旋转（上左 $R$）  
> - 线速度既旋转（下右 $R$），又要加上“平移 × 角速度”的耦合项（下左 $[p]_\times R$）

---

## 9. “原点是不是在动？”——参考点 vs 坐标系（避免一个常见误解）

讨论 twist 时有两个概念必须分开：

- **参考点**（reference point）：线速度 $v$ 取的是“哪个点”的速度
- **坐标系**（frame）：你用哪组轴来表达向量分量

当你把坐标系 $B$ **附着在刚体上**（body frame），并且参考点选择为该坐标系原点，则在该坐标系下这个原点对自身不动，所以：

{{< math >}}
$
v_B = 0
$
{{< /math >}}

这并不矛盾，因为同一个运动换到空间坐标系 $A$ 后，一般会得到：

{{< math >}}
$
v_A = \omega_A\times p \neq 0
$
{{< /math >}}

因此“$v_B$ 是否为 0”取决于你到底在用 **body twist** 还是 **spatial twist**。

---

## 10. Spatial Jacobian vs Body Jacobian：Adjoint 最常见的落点

- **Spatial Jacobian** $J_s$：输出的 twist 用空间（世界/基座）坐标表达
- **Body Jacobian** $J_b$：输出的 twist 用末端自身坐标表达

若末端位姿为 $T(q)$（从 body 到 space），二者关系：

{{< math >}}
$
\boxed{
J_s(q)=\mathrm{Ad}_{T(q)}\,J_b(q)
}
$
{{< /math >}}
反向：
{{< math >}}
$
\boxed{
J_b(q)=\mathrm{Ad}_{T(q)^{-1}}\,J_s(q)
}
$
{{< /math >}}

---

## 11. 实操清单：在微分 IK 里什么时候必须做 Adjoint 变换？

你真正写控制器时，只需要遵守一条铁律：

> **Jacobian 输出的 twist 坐标系，必须和你构造的 $\dot{x}$/误差所在坐标系一致。**

典型场景：

1) 你用 world frame 写了末端误差/速度 $\dot{x}_A$，但拿到的是 body Jacobian $J_b$。  
则应先把 $\dot{x}_A$ 变到 body：
{{< math >}}
$
\dot{x}_B = \mathrm{Ad}_{T^{-1}}\dot{x}_A
$
{{< /math >}}
再做微分 IK：
{{< math >}}
$
\dot{q}=J_b^\dagger \dot{x}_B
$
{{< /math >}}

2) 多个末端、多任务叠加：先统一到同一 frame，再拼接/加权做最小二乘。

---

## 12. 总结：一条从优化到几何的闭环

- 微分 IK 的方程是 $J\dot{q}=\dot{x}$，在一般情形下用最小二乘表述。
- 解不唯一时引入最小范数，得到伪逆（列满秩/行满秩分别对应两种闭式形式）。
- 为了奇异稳定，加入 Tikhonov 正则得到 DLS，且 $\lambda>0$ 保证可逆。
- Jacobian 之所以要 Adjoint 变换，是因为它输出的是 twist，而 twist 的坐标变换不是简单旋转；平移会与角速度耦合。
- Adjoint 的结构来自一个最基本的事实：**刚体转动时，不同点的线速度不同**。

---

## 附：常用公式速查

- 伪逆（列满秩）：$\;J^\dagger=(J^T J)^{-1}J^T$
- 伪逆（行满秩）：$\;J^\dagger=J^T(JJ^T)^{-1}$
- DLS：$\;\dot{q}=(J^T J+\lambda^2 I)^{-1}J^T\dot{x}=J^T(JJ^T+\lambda^2 I)^{-1}\dot{x}$
- Adjoint：
{{< math >}}
$
\mathrm{Ad}_T=
\begin{bmatrix}
R & 0\\
[p]_\times R & R
\end{bmatrix}
$
{{< /math >}}
- Jacobian 变换：$\;{}^A J=\mathrm{Ad}_{{}^A T_B}\,{}^B J$
- Spatial/Body Jacobian：$\;J_s=\mathrm{Ad}_{T}\,J_b$


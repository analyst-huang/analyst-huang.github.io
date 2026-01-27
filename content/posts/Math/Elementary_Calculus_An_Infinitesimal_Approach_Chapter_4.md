---
title: "Elementary Calculus: An Infinitesimal Approach: Chapter 4"
date: 2026-01-25
draft: false
---

# TLDR;
通过划分区间的方法，非标准分析以直观的形式重新定义黎曼和积分。

### Definition
Let a < b and let $\Delta x$ be a positive real number. Then the **Riemann sum** $\sum_a^b f(x) \Delta x$ is defined as the sum
{{<math>}}
$$
\sum_a^b f(x) \Delta x = f(x_0)\Delta x + f(x_1)\Delta x + ... + f(x_{n-1})\Delta x + f(x_n)(b-x_n)
$$
where n is the largest integer such that $a + n \Delta x \leq b$ and 
$$
x_0 = a, x_k = a + k\Delta x
$$
are the partition points.
{{</math>}}

### Theorem
Let f be a continuous function on an interval I, let a < b be two points in I, and left dx be a positive infinitsimal. Then the infinite Riemann sum
{{<math>}}
$$
\sum_a^bf(x)dx
$$
{{</math>}}
is a finite hyperreal number.

#### Proof
首先因为是连续函数，由连续函数的性质，普通的黎曼和会被上下限制，然后通过Transfer Principle, 就可以对超实数成立。

### Definition
定积分定义为区间内黎曼和的标准部，自然的。

### Theorem
Give a continuous function f on [a,b] and two positive infinitesimals dx and du, the definite integrals with respect to dx and du are the same,
{{<math>}}
$$
\int_a^bf(x)dx = \int_a^bf(u)du
$$
{{</math>}}

#### Proof
证明的方法是证明不同的dx或者du，只能导致一个更高阶的无穷小的差距，然后求和之后的标准部会舍去那一部分。可以取区间重叠之间，最大的那个无穷小的height。

### Theorem
Suppose f is continuous and has minimum value m and maximum value M on a closed interval [a,b]. Then
{{<math>}}
$$
m(b-a) \leq \int_a^bf(x) dx\leq M(b-a)
$$
{{</math>}}

#### Proof
证明是显然的

### Theorem(The Addition Propety)
Suppose f is continuous on an interval . Then for all a,b,c in I,
{{<math>}}
$$
\int_a^cf(x)dx = \int_a^bf(x)dx + \int_b^cf(x)dx
$$
{{</math>}}

#### Proof
因为无穷小的区间是可以任意取的，所以证明是显然的

### Theorem
Left f be continous on an interval I. Choose a point a in I. Then the function F(x) defined by 
{{<math>}}
$$
F(x) = \int_a^xf(t)dt
$$
{{</math>}}
is continuous on I. 

#### Proof
根据积分的加性和连续的性质，是容易证明的。

### FUNDAMENTAL THEOREM OF CALCULUS
Suppose f is continuous on its domain, which is an open interval I.
- For each point a in I, the definite integral of f from a to x considered as a function of x is an antiderivative of f, That is,
{{<math>}}
$$
d(\int_a^xf(t)dt) = f(x)dx
$$
{{</math>}}
- If F is any antiderivative of f, then for any two points (a,b) in I the definite integral of f from a to b is equal to the difference F(b) - F(a)
{{<math>}}
$$
\int_a^bf(x)dx = F(b) - F(a)
$$
{{</math>}}

#### Proof
说实话，如果告诉了积分和导数的定义，然后允许使用无穷小，那么证明也是几乎容易的，毕竟我高中也这样证明出来过。
对于二的证明，只需要导数是常数的函数是常值函数即可证明。

之后就是一些不定积分的计算技巧了，不再赘述。
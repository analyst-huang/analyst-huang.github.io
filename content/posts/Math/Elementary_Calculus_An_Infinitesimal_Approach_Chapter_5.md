---
title: "Elementary Calculus: An Infinitesimal Approach: Chapter 5"
date: 2026-01-28
draft: false
---

# TLDR;
本章通过Transfer Principle，证明了标准分析中$\epsilon - \delta$语言所定义的极限与非标准分析中极限定义的等价性。由此，我们证明了，非标准分析中的定理，只要表述为极限形式，既可以在标准分析中找到对应。

### THEOREM
Let f be defined in some deleted neighborhood of c. Then the following are equivalent: 
- $\lim_{x\rightarrow c}f(x) = L.$
- The $\epsilon , \delta$ condition for $\lim_{x\rightarrow c}f(x) = L $ is true.

### Proof
- 首先假设标准分析的极限定义成立，那么对于任意的$\epsilon$, 都存在一个去心邻域满足大小约束。通过Transfer Principle，任意无穷小都会落在这个邻域中，也就是说，函数的差会小于任何实数的绝对值，也就是说，差是无穷小，则取标准部得证。

- 假设非标准分析的极限定义成立。我们反设标准分析中的定义不成立，也就是说：
{{<math>}}
$$
\exist \epsilon \forall \delta \forall x \in |x - c| < \delta, |f(x) - L| \ge \epsilon
$$
{{</math>}}
同样，通过transfer principle，x可以是c + 无穷小，但是两者之差大于一个实数，也就是说，差的标准部不再是0，与非标准分析极限定义成立矛盾。


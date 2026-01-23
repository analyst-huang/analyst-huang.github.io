---
title: "Elementary Calculus: An Infinitesimal Approach: Chapter 3"
date: 2026-01-23
draft: false
---

# TLDR；
本章讲解了非标准体系下，极限、连续的定义，并证明了费马引理，罗尔定理，中值定理等重要定理。对于**无穷大整数切分区间**的引入，使得证明更加符合直觉。

### Difinition
L is the limit of f(x) as x approaches c if whenever x is infinitely close to but not equal to c, f(x) is infinitely close to L
{{<math>}}
$$
\lim_{x\rightarrow c}f(x) = L
$$
{{</math>}}

#### Remark
这里的L是一个real number，否则等号后面就可以有不同的hyperreal number了。

由极限的定义和标准部的运算法则，可以很容易的推导出极限的运算法则，不再重复。

同理可以定义左极限和右极限。

### Difinition
f is said to be continuous at a point c if:
- f is defined at c
- whenever x is infinitely close to c, f(x) is infinitely close to f(c)

#### Remark
显然连续就等价于左极限等于右极限并且在该点有定义。以及左连续和右连续也是自然的。

运用极限的运算性质，就能推出连续函数的运算法则。（注意，其中连续函数的复合的证明是通过st(f(x)) = f(st(x)) 当且仅当 f(x) 连续完成的）

以下几个说法是等价的：
- f is continous at C
- Whenever x ≈ c, f(x) ≈ f(c)
- Whenever st(x) = c, st(f(x)) = f(c)
- $\lim_{x\rightarrow c}f(x) = f(c)$
- y is continous at x = c
- Whenver $\Delta x $ is infinitesimal, $\Delta y $ is infinitesimal.


接下来我们就要引入**hyperinteger**, 这对我们后续的证明至关重要。
### Definition
A hyperinteger is a hyperreal number y such that y = [x] for some hyperreal x

#### Remark
比如说$[\frac{1}{\epsilon}]$ 就可以是一个超整数。

通过超整数，我们可以构造出一系列的区间来：
{{<math>}}
$$
[a, a+ \delta], [a + \delta, a+ 2\delta]...[a + (H-1)\delta, b]， \delta = (b-a)/H
$$
{{</math>}}
注意，其中的H是一个无穷大整数

### INTERMEDIATE VALUE THEOREM
Suppose the real function f is continuous on the closed interval [a,b] and f(x) is positive at one endpoint and negative at the other endpoint. Then f has a zero in the interval (a,b) ; that is ,f(c) = 0, for some real c in (a,b)

#### PROOF
先做无穷划分，然后取集合{f(x_i) > 0 }.通过transfer principle，可以取index的最小元m。所以f*(x_m-1) <= 0 < f*(x_m)。又因为连续性，取标准部可证明。

### EXTREME VALUE THEOREM
Let f be continuous on its domain, which is a closed interval [a,b]. Then f has a maximum at some point in [a,b], and a minimum at some point in [a,b]

#### PROOF
先做无穷划分，然后可以从中找到f(x_m)是最大值，取标准部即可。

### ROLLE's THEOREM
Suppose that f is continuous on the closed interval [a,b] and differentiable on the open inverval (a,b) If f(a) = f(b) = 0, then there is at leat one point c strictly between a and b where f has derivative zero. 

#### PROOF
分类讨论即可。不在两点，就在中间（极值可以导出导数为0，夹逼）

### MEAN VALUE THEOREM
拉格朗日中值定理。利用罗尔定理容易证明。

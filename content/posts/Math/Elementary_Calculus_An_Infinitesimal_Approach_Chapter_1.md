---
title: "Elementary Calculus: An Infinitesimal Approach: Chapter 1"
date: 2026-01-20
draft: false
---

## 前言
在大一的时候就在高数的书上看到了对非标准分析的科普，当时就找来了Robinson的大部头来看，结果当然是看不懂了，毕竟当时的数学基础很差。最近有空，而且LLM也发展的很好，很多问题都不用自己一个人苦思冥想，还不知道对不对了。所以挑了一本先把模型论等等的知识作直觉把握，然后重写微积分（严谨地）的书。

# TLDR;
非标准分析之所以在某些方面比$\delta-\epsilon$语言清晰和简明，是因为通过将$\mathbb{R}$扩张为$\mathbb{R}^*$（超实数），将$\delta-\epsilon$语言的外在的量词压缩到了无穷小这个超实数的定义中。例如f(x)在a处的极限：
<div align="center">
∀ε>0∃δ>0(∀x,∣x−a∣<δ⇒∣f(x)−f(a)∣<ε)
</div>
如果我们用非标准分析的语言来写，那么这个命题可以写成：
<div align="center">
∀x≈a,f(x)≈f(a)
</div>
其中 x≈a的定义是 x-a是无穷小（指的是超实数，不是原来$\delta-\epsilon$语言的无穷小）。换言之，"对于任意的epsilon"在这里已经被作为*超实数*的无穷小这个概念所覆盖了。

## 超实数轴(The Hyperreal Line)
超实数是对实数的扩展：两端的无穷大，原点附近的无穷小，以及每个实数附近的超实数。通过模型论，可以严格保证——所有关于实数的标准一阶命题，在超实数体系中仍然成立。如果不深入模型论，只需要记住几个principle就可以了。

### THE EXTENSION PRINCIPLE
- The real numbers from a subset of the hyperreal numbers, and the order relation of x < y for the real numbers is a subset of the order relation for the hyperreal numbers.
-  There is a hyperreal number that is greater than zero but less than every positive real number.
- For every real function of one or more variable we are given a corresponding hyperreal function f* of the same number of variables. f* is called the natural extension of f. 

#### Remark
这条准则给出了超实数的扩展方式。这里的natural extension并不是说给超实数来了一个函数的映射关系，而是说，这个延拓出来的函数，保持实数集上的性质，并且将会满足TRANSFER PRINCIPLE(见下)。

### TRANSFER PRINCIPLE
- Every real statement that holds for one or more particular real functions holds for the hyperreal natural extensions of these functions.

#### Remark
例如说： 
<div align="center">
$\forall x\in \mathbb{R} \forall y \in \mathbb{R}(x+y = y+x)$
</div>
将其中的$\mathbb{R}$替换为$\mathbb{R}^*$,命题依然成立。

### 无穷小的定义
如果对于任意的实数r，$-r < \epsilon < r$, $\epsilon$ 被称为无穷小。实数中无穷小只有0. 同理，可以完全凭借直觉的构造无穷大。

## 标准部(STANDARD PARTS)
首先定义，如果两个超实数 b 和 c被称为无限接近(infinitely close), 记为 b ≈ c, 那么b - c 是无穷小（infinitesimal）

很显然 ≈ 具有自反性，对称性和传递性。

### DEFINITION
Let b be a finite hyperreal number. The standard part of b, denoted by st(b), is the real number which is infinitely close to b. Infinite hyperreal numbers do not have standard parts.

也就是说： $ b = st(b) + \epsilon, $for some infinitesimal $\epsilon$,其中存在性可以由实数集合的完备性给出(构造上确界).

根据定义容易证明：
- $st(-a) = -st(a)$
- $st(a+b) = st(a) + st(b)$
- $st(ab) = st(a) * st(b)$
- if $st(b) \neq 0$, then $st(a/b) = st(a)/st(b)$
- $st(a^n) = (st(a))^n$
- If $a \geq 0 $, then $st(\sqrt[n]{a}) = \sqrt[n]{st(a)}$
- If $ a \leq b$, then $st(a) \leq st(b)$


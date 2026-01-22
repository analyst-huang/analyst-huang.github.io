---
title: "Elementary Calculus: An Infinitesimal Approach: Chapter 2"
date: 2026-01-22
draft: false
---

# TLDR;
本章讲述的是用非标准分析建立导数概念的过程。相较于传统教材对dx，dy的语焉不详，非标准分析极清晰地给出了定义，并严格的建立了对$d$的运算法则。

### Definition
S is aid to be the slope of f at a if:
{{< math >}}
$$
S = st(\frac{f(a + \Delta x) - f(a)}{\Delta x})
$$
{{< /math >}}
for every nonzero infinitesimal $\Delta x$

#### Remark
这就是非标准分析中的slope的定义。我们取直觉上斜率在无穷小情况下的标准部，即可得到导数。这里的对于每个非零无穷小，是必要的，例如$|x|$ 在原点处。更好的例子是
{{< math >}}
$$
f(x) = x \sin (x) (x \neq 0), f(0) = 0
$$
{{< /math >}}
容易验证，在0处，原式等于$\sin(\frac{1}{\Delta x})$,我们可以构造无穷小，使得这个表达式可以等于一个确定的值。例如说，我们先取一个整数的无穷大N， 然后构造新的无穷大 $N\pi$, 那么 $\frac{1}{N\pi}$就是一个无穷小，而原式等于0。同样的，我们可以构造出使得原式任意取值的无穷小，因此这一点的slope是不存在的,同时也说明这个定义无法更宽泛了。

### Definition
Let f be a real function of one variable. The derivative of f is the new funtion f' whose value at x is the slope of f at x. In symbols, 
{{<math>}}
$$
f'(x) = st(\frac{f(x + \Delta x) - f(x)}{\Delta x})
$$
{{</math>}}
whenever the slope exists. 

### More Definition
{{<math>}}
$$
\Delta y = f(x+\Delta x ) -f(x)
$$
Here $\Delta x $ is the independent variable and $\Delta y$ is the dependent variable.
$$
y' = f'(x)
$$
$$
y' = st(\frac{\Delta y}{\Delta x})
$$
{{</math>}}

### The Increment Theorem
Let y = f(x), Suppose f'(x) exists at a certain point x, and $\Delta x$ is infinitesimal. Then $\Delta y$ is infinitesimal, and 

{{<math>}}
$$
\Delta y = f'(x) \Delta x + \epsilon \Delta x
$$
{{</math>}}

#### Remark
注意公式成立的条件要求$\Delta x$ 是 infinitesimal

### Definition
- The differential of x is the independent variable $dx = \Delta x$
- The differential of y is the dependent variable dy given by
{{<math>}}
$$
dy = f'(x)dx
$$
When dx is not 0
$$
\frac{dy}{dx} = f'(x)
$$
{{</math>}}

#### Remark
The increment theorem可以被重写为：
{{<math>}}
$$
\Delta y = dy + \epsilon dx
$$
{{</math>}}
这里的dx，dy是明确定义的，dx就是$\Delta x$, 而dy是一个关于f'(x) 和 dx的函数。

这里不再列举关于derivative的运算法则，由于使用了无穷小语言，所以证明几乎就是直接的。这里仅给出反函数求导的证明：

IF: y = f(x), x = g(y), f'(x) and g'(x) exist and are nonzero, then:
{{<math>}}
$$
f'(x) = \frac{1}{g'(x)}
$$
{{</math>}}

PROOF:
Since $\Delta x$ is infinitesimal, so $\Delta y$ is infinitesimal too!
{{<math>}}
$$
f'(x) * g'(x) = st(\frac{\Delta y}{\Delta x}) * st(\frac{\Delta x}{\Delta y}) = 1$$
{{</math>}}

We can say: 
{{<math>}}
$$
\frac{dy}{dx} = \frac{1}{\frac{dx}{dy}}
$$
{{</math>}}
并不是trivial的，因为dy/dx 是以x为独立变量计算的，而1/(dx/dy)是以y为独立变量计算的。

当我们对隐函数/函数方程两边取d的时候，我们其实假设了有导数，然后进行的是形式上的操作，之于真的有没有，算出来之后再说。
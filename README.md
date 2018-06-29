## 碎纸复原问题

### 针对一维切割的情况

#### 问题的形式化描述

根据题意，将一张印有文字的纸沿纵向等宽切割成 19 张条形纸片，并打乱顺序。设计一个算法将打乱顺序的纸片按正确的顺序排列，并复原。

利用 python 的 PIL 模块读取附件 1 中的图片，灰度化后转换为矩阵。$S_i$为第 $i$ 个纸片对应的灰度矩阵，形式如下
$$
S_i = \left[
\begin{matrix}
0 & 0 & \cdots & 0\\
255 & 0 & \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 255 & \cdots & 0\\
\end{matrix}
\right]
$$
矩阵中的每个元素的取值范围为 $a_{ij}\in \left[0, 255\right]$。定义所有纸片灰度矩阵的集合为$\mathbb{S} = \left\{S_1, S_2, \cdots, S_{19}\right\}$。

#### 问题的解

$S_1, S_2, \cdots, S_{19}$ 的一个正确的排列就是该问题的一个解，$S_1, S_2, \cdots, S_{19}$ 的所有排列方式就构成了问题的解空间。由此，该问题的时间复杂度为 $O(n!)$。以矩阵的形式表达，设 $R_{a_1, a_2, \cdots, a_{19}} = \left[\begin{matrix}S_{a_1} & S_{a_2} & \cdots & S_{a_{19}}\end{matrix}\right]$ 为拼接后得到的分块矩阵，则正确的分块矩阵 $R_{origin}$ 即为问题的一个解，$R_{a_1, a_2, \cdots, a_{19}}$ 构成的集合 $\mathbb{R}$ 即为问题的解空间。

#### 匹配度函数

|      符号       |             含义             |  numpy 调用  |
| :-------------: | :--------------------------: | :----------: |
| $\alpha_{i, t}$ |  $S_i$ 第一行元素构成的向量  |   $S_i[1]$   |
| $\alpha_{i, b}$ | $S_i$ 最后一行元素构成的向量 |  $S_i[-1]$   |
| $\alpha_{i, l}$ |  $S_i$ 第一列元素构成的向量  | $S_i[:, 1]$  |
| $\alpha_{i, r}$ | $S_i$ 最后一列元素构成的向量 | $S_i[:, -1]$ |

对于相邻的两片纸片 $S_i$ 与 $S_j$，$S_i$ 的右边缘应与 $S_j$ 的左边缘相似，即 $\alpha_{i, r}$ 与 $\alpha_{j, l}$ 相似。参考论文中采用的是比较 $\alpha_{i, r}$ 与 $\alpha_{j, l}$ 中黑色像素点的个数，即比较 $\left\Vert S_i\right\Vert$ 与 $\left\Vert S_j\right\Vert$，只考虑了黑色像素点的个数，并没有考虑其位置。因此考虑采用余弦相似度来表征 $S_i$ 与 $S_j$ 的匹配度。
$$
m_{ij} = \cos\theta = \dfrac{\left(\alpha_{i, r} \cdot \alpha_{j, l}\right)}{\left\Vert \alpha_{i, r}\right\Vert \left\Vert \alpha_{j, l}\right\Vert}
$$
因为 $S_i$ 中所有元素都为正数，所以 $m_{ij}\in \left[0, 1\right]$。

1. 当 $\alpha_{i, r} = \alpha_{j, l}$ 时，$m_{ij} = 1$，此时 $S_i$ 与 $S_j$ 的匹配度达到最大，注意此处的匹配度并不是 $S_i$ 与 $S_j$ 匹配的概率。
2. 当 $\alpha_{i, r}$ 与 $\alpha_{j, l}$ 正交时，匹配度最小。

#### 搜索解空间


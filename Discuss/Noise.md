# Noise 实验说明

## 这一部分要做什么

这一部分的目标是构造一段 `noise`，用于模拟公共广播或录音链路中常见的高频 hiss 噪声。

这里的噪声不是为了尽可能复杂，而是为了尽可能清楚地体现一个可分析的问题：当语音被高频噪声污染时，基础滤波器能否改善语音质量。

## 为什么选 hiss 噪声

本项目不打算从一开始就使用非常复杂的真实环境噪声，比如站台人群声、列车低频轰鸣、混响和广播回声全部叠加在一起。那样虽然更真实，但会让实验变得不够可控，也不适合用基础 low-pass filter 解释。

所以这里选的是一种更适合课堂展示的噪声模型：

- 听感上像连续的高频底噪
- 在频域中主要偏高频
- 和语音主要频带不是完全重合
- 便于通过滤波器压制

## 背景依据

在铁路站台和公共广播环境中，语音可懂度会受到背景噪声和空间反射的影响。站台环境往往噪声较高，而广播系统设计本身也很关注 speech intelligibility。与此同时，在实际录音或播报链路中，麦克风自噪声、前级放大电路、传输链路等也可能引入类似 hiss 的高频底噪。

虽然真实场景的噪声远不止一种，但在项目初期，把它抽象成高频 hiss 是合理的，因为这样能够突出“频域分析 + 基础滤波”的主线。

## 设计思路

这次的噪声准备采用：

`white hiss + high-pass shaping`

具体思路是：

- 先生成宽带随机噪声
- 再通过一个简单的高通式 shaping，让高频部分更突出
- 最后再对振幅做归一化

这样得到的噪声会比普通白噪声更接近“电子 hiss”的感觉，同时又保持足够简单，方便分析。

## 这个噪声样本需要满足的要求

- 能单独播放并听出明显高频底噪感
- 频谱中高频部分应明显增强
- 强度可控，方便和 clean voice 合成
- 时长与 clean voice 一致，便于后续逐点叠加

## 在整个项目中的作用

`noise` 是整个系统里的干扰项。它的意义主要有两个：

- 在实验上，它是后续构造 noisy voice 的基础
- 在展示上，它能帮助观众理解“滤波器到底在压制什么”

所以这段 noise 不只是一个程序生成的随机信号，它实际上承担了“定义问题”的作用。

## 参考资料

- [Calculating speech intelligibility for the design of public address systems at railway stations](https://journals.sagepub.com/doi/abs/10.1243/0954409011531611)
- [Effects of Artificial Synthetic Speech Control of SNR and Speech Rate on the Intelligibility of Train Station Announcements](https://link.springer.com/article/10.1007/s40857-023-00306-8)
- [Sound field characteristics of underground railway stations – Effect of interior materials and noise source positions](https://www.sciencedirect.com/science/article/abs/pii/S0003682X12001569)

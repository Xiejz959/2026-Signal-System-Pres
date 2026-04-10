# Noisy Voice 实验说明

## 这一部分要做什么

这一部分的目标是构造 `noisy voice`，也就是把前面准备好的 `clean voice` 和 `noise` 合成为一段带噪语音，用来作为滤波系统的输入。

在整个项目中，这一步是最关键的桥梁。因为它把“原始语音”和“噪声模型”真正连接在一起，形成了我们后续需要处理的问题本身。

## 基本模型

最简单的模型可以写成：

`noisy voice = clean voice + noise`

这也是本项目最核心的输入形式。

从信号与系统的角度看，这里体现的是一个很基础但很重要的思想：语音和噪声都可以被看成信号，而带噪语音就是两个信号叠加后的结果。

## 设计思路

这里的关键不是“加上去就行”，而是要让 noisy voice 满足两个要求：

- 噪声要足够明显，听众能感受到问题
- 语音仍然要保持基本可懂度，不能完全被淹没

因此，合成 noisy voice 时需要控制一个合适的噪声强度。这个强度不一定非要一开始就严格用复杂指标定义，但至少要保证：

- 加噪后能明显听到高频 hiss
- 语音的主轮廓仍然可辨认
- 后续滤波后能形成清楚的前后对比

## 为什么 noisy voice 很重要

如果只有 clean voice 和 filtered voice，展示会很难成立，因为观众不知道系统到底解决了什么问题。  
而 noisy voice 的作用正是在课堂上把问题“摆出来”：

- clean voice 告诉大家原始目标是什么
- noisy voice 告诉大家问题出在哪里
- filtered voice 告诉大家系统做了什么改善

这三者必须连成一条完整链路。

## 这个样本需要满足的要求

- 时长与 clean voice 保持一致
- 加噪后听感变化明显
- 不出现削波
- 后续适合做 waveform 和 spectrogram 对比
- 能稳定作为滤波系统输入

## 在整个项目中的作用

`noisy voice` 是后续所有频域分析和滤波实验的直接输入。  
如果说 clean voice 是系统的起点，noise 是干扰来源，那么 noisy voice 就是整个项目真正要处理的对象。

因此，这一步虽然在公式上很简单，但在展示上非常关键，因为它决定了整个项目的“问题感”是否清楚。

## 参考资料

- [Speech Audiometry - StatPearls (NCBI)](https://www.ncbi.nlm.nih.gov/books/n/statpearls/article-142875/)
- [Effects of Artificial Synthetic Speech Control of SNR and Speech Rate on the Intelligibility of Train Station Announcements](https://link.springer.com/article/10.1007/s40857-023-00306-8)

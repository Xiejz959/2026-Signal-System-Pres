# Slide Draft 0.2

## 1. Title and Team

### 页面目标

把题目、课程和团队信息清楚交代出来，让观众一开始就知道你们在做什么。

### 页面内容

- 标题：**Designing a Noise Reduction Filter for Voice Signals**
- 课程：ECE0402 Signals, Systems & Probability
- 小组成员

### 页面结论

我们研究的是一个基于信号与系统视角的语音降噪问题。

## 2. Motivation

### 页面目标

说明这个题为什么值得做。

### 页面内容

- 语音录音、公共广播、语音助手等场景都可能受到噪声污染
- 高噪声会降低语音清晰度和可懂度
- 我们希望用基础滤波方法处理一个清楚的小问题

### 页面结论

语音降噪是一个真实存在的问题，而基础滤波提供了一个可解释的切入点。

## 3. Problem Statement

### 页面目标

定义系统的输入、输出和目标。

### 页面内容

- 输入：带噪语音
- 输出：更清晰的语音
- 目标：削弱高频 hiss，同时尽量保留语音主要信息

建议配一个简单流程图：

`clean voice + noise -> noisy voice -> filter -> filtered voice`

### 页面结论

我们的任务不是做复杂语音增强，而是在一个明确噪声场景下设计基础滤波系统。

## 4. Simulated Application Scenario

### 页面目标

解释为什么用“公共广播背景 + 仿真信号”。

### 页面内容

- 背景：公共广播 / 站台播报
- 实验方式：不录真实复杂环境，而是构造可控的 clean voice 和 hiss noise
- 理由：这样更稳定、更可分析，也更适合课堂展示

### 页面结论

我们保留真实场景背景，但用可控仿真来保证系统设计和结果解释都清楚。

## 5. Signal Characteristics

### 页面目标

说明语音和噪声的频率特征差异。

### 页面内容

- 语音主要信息集中在较低到中频范围
- hiss 噪声主要增强高频区域
- noisy voice 是两者叠加后的结果

建议配图：

- clean / hiss / noisy 的频谱或 spectrogram 对比

### 页面结论

因为语音和高频 hiss 在频域上的分布不同，所以滤波有机会起作用。

## 6. Why Fourier Transform Helps

### 页面目标

把傅里叶变换的作用讲清楚。

### 页面内容

- 时域中语音和噪声叠加后不容易直接分开
- 傅里叶变换可以把信号转到频域
- 在频域里更容易看到高频噪声集中在哪
- 频域分析用来指导滤波器设计，而不是直接完成降噪

### 页面结论

傅里叶变换帮助我们回答“噪声主要在哪些频率上”，从而指导滤波器设计。

## 7. Filter Design Idea

### 页面目标

解释为什么先选 low-pass，以及参数怎么选。

### 页面内容

- 主方法：四阶 Butterworth low-pass filter
- 候选 cutoff：2800 / 3200 / 3600 Hz
- 设计原则：
  - cutoff 太低：噪声少，但语音会变闷
  - cutoff 太高：语音更自然，但噪声残留更多
- 最终主 demo 版本：3200 Hz

### 页面结论

3200 Hz 是当前“噪声压制”和“语音清晰度保留”之间最适合展示的一组平衡参数。

## 8. System Workflow

### 页面目标

把系统流程画清楚。

### 页面内容

- clean voice generation
- hiss noise generation
- noisy voice synthesis
- FFT-based observation
- low-pass filtering
- result evaluation

建议配流程图：

`clean voice -> add hiss -> noisy voice -> low-pass filter -> filtered voice`

### 页面结论

这个项目不是只调用一个包，而是完整经历了建模、分析、设计、比较和评估几个步骤。

## 9. Demo Setup

### 页面目标

说明 demo 用的是什么材料、怎么展示。

### 页面内容

- clean / noisy / filtered 三段音频
- 同一段样本配 waveform 和 spectrogram
- 播放顺序固定

## 10. Results

### 页面目标

展示处理效果。

### 页面内容

- 音频前后对比
- waveform 对比
- spectrogram 对比
- 参数比较图

## 11. Discussion and Limitations

### 页面目标

说明系统为什么有效，以及它的边界在哪里。

### 页面内容

- low-pass 对高频 hiss 有效
- 同时也会削弱一部分高频语音细节
- 更复杂环境噪声不适合只靠基础 low-pass 处理

## 12. Conclusion and Q&A

### 页面目标

把整场展示收住。

### 页面内容

- 问题总结
- 方法总结
- 结果总结
- 局限总结
- Q&A

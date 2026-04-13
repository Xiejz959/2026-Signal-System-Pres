# Slide Draft 0.1

## 1. Title and Team

- 题目：Designing a Noise Reduction Filter for Voice Signals
- 课程信息
- 组员名单

## 2. Motivation

- 语音降噪为什么重要
- 公共广播 / 站台播报为什么适合作为应用背景
- 真实语音场景中噪声会降低可懂度

## 3. Problem Statement

- 输入：带噪语音
- 输出：更清晰的语音
- 目标：削弱高频 hiss，同时尽量保留语音内容

## 4. Simulated Application Scenario

- 为什么不用复杂真实环境录音
- 为什么采用“真实背景 + 可控仿真”
- clean voice、noise、noisy voice 的关系

## 5. Signal Characteristics

- 语音信号的基本频率特征
- hiss 噪声的高频特征
- noisy voice 的频域变化

## 6. Why Fourier Transform Helps

- 时域里难以直接区分噪声和语音
- 频域里能更清楚看到高频噪声分布
- 用频域分析指导滤波器设计

## 7. Filter Design Idea

- 为什么先用 basic low-pass filter
- cutoff 的设计逻辑
- 噪声压制和语音保真之间的 tradeoff

## 8. System Workflow

- clean voice
- add hiss noise
- noisy voice
- low-pass filter
- filtered voice

## 9. Demo Setup

- 音频样本说明
- 噪声生成方式
- 演示中使用 waveform + spectrogram

## 10. Results

- clean / noisy / filtered 音频对比
- waveform 对比
- spectrum / spectrogram 对比

## 11. Discussion and Limitations

- 为什么 low-pass 有效
- 为什么会损失一部分高频语音细节
- 如果噪声更复杂，基础滤波会遇到什么限制

## 12. Conclusion and Q&A

- 方案总结
- 结果总结
- 局限总结
- Q&A

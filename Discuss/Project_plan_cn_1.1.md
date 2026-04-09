# 语音信号降噪项目计划
<a id="Chinese"></a>

[英文](Project_plan_1.1.md#English)

本文档记录 ECE0402 展示项目
**Designing a Noise Reduction Filter for Voice Signals**
的整体执行计划。

本项目聚焦于**高频加性噪声场景下的语音降噪**，展示风格采用**理论与 demo 平衡**的方式。

## 项目摘要

整体流程分为三个主要阶段：

1. 全体成员共同完成文献查找与系统定义
2. 系统方案确定后，分成 Testing Group 和 PPT Group
3. 最后由全组共同完成整合、彩排与 Q&A 准备

为了保证 presentation 聚焦、易讲清楚，项目范围会刻意控制在以下内容内：

- 一种主要噪声场景
- 一种基础且可解释的滤波思路
- 一个清楚的课堂 demo
- 一套前后对比结果

## 技术范围

系统流程定义为：

`clean voice -> add high-frequency noise -> noisy voice -> filter -> filtered voice`

当前版本的默认设定如下：

- **噪声场景：** 高频加性噪声
- **展示风格：** 理论与 demo 平衡
- **工具链：** Python + MATLAB
- **主要方法：** 从基础 low-pass 或 band-pass filter 出发，最后保留更容易解释、结果也更清楚的方案

### 核心概念

- Fourier Transform
- frequency-domain interpretation
- filtering
- LTI-system viewpoint
- 降噪与语音失真之间的 tradeoff

### 需要回答的核心问题

- 哪一部分是语音，哪一部分是噪声
- 为什么在这个场景下滤波是合理方案
- 滤波器是如何设计出来的
- 系统效果改善了多少
- 这种方法的局限是什么

## Phase A：文献查找与系统定义

这一阶段由全体成员共同参与。

### 主要任务

- 收集 speech frequency characteristics 相关参考资料
- 收集 high-frequency noise models 相关参考资料
- 收集 basic digital filter design 相关参考资料
- 收集 simple voice denoising through filtering 相关参考资料
- 明确最终的问题定义
- 确定要展示的滤波器类型
- 确定系统流程图
- 确定课堂上要展示哪些输出
- 统一 slides 和讨论中使用的术语

### 预期产出

- 最终项目标题
- 一段清楚的问题定义
- 一张系统框图
- 一个确定下来的滤波器设计方向
- 一份支持理论部分的参考文献列表

### 完成标准

当满足以下条件时，Phase A 结束：

- 全组对系统方案达成一致
- PPT Group 不等待实验结果也能开始做 slides

## Phase B：系统方案固定后的分组执行

当系统方案固定后，项目分成两组执行。

### Testing Group

成员：

- Xiejz
- Xuzf
- Chenm

### 主要任务

- 准备 clean voice samples
- 准备或生成 high-frequency noise samples
- 在可控条件下构造 noisy voice signals
- 使用 Python 和/或 MATLAB 实现 filtering pipeline
- 比较候选参数
- 选出最适合课堂展示的版本
- 生成实验结果材料：
  - waveform comparison
  - spectrum comparison
  - filtered 与 unfiltered 的音频样本
  - 简短的文字结论
- 总结系统局限与失败情形

### 预期产出

- 一套可复现的语音降噪流程
- 一组推荐参数
- 一套可在课堂 2 分钟内展示的 demo package
- 可直接用于 slides 的图表
- 一段说明为什么所选滤波器有效的解释

### PPT Group

成员：

- Luowt
- Chenym
- Xiejz

### 主要任务

- 在 Phase A 结束后立即开始搭建 slides
- 准备动机与背景页面
- 准备理论页面，包括：
  - voice signal basics
  - high-frequency noise characteristics
  - frequency-domain analysis
  - filter idea and rationale
- 为结果页与 demo 页预留位置
- 根据 Testing Group 的每日进展更新 slides
- 维护视觉一致性与 references
- 准备 speaker notes 与转场逻辑

### 预期产出

- 在实验结果完全打磨之前，先完成一版完整的 draft
- 最终整合好图表、结果和 references 的 slide deck
- 一套和 demo 匹配的展示逻辑

## Phase C：最终整合与彩排

这一阶段由全体成员共同参与。

### 主要任务

- 检查理论部分是否真正对应已实现的系统
- 检查图表和口头讲述是否使用统一术语
- 删除无助于观众理解的多余技术细节
- 确定最终课堂 demo 流程
- 分配讲述部分
- 练习 Q&A
- 在展示日前至少 3 天提交 slides

### 预期产出

- 最终 slide deck
- 最终 demo package
- 最终 references
- 最终成员贡献记录
- 根据 rehearsal 调整后的展示版本

## 协作规则

- 项目采用高层串行流程：
  - first：全员共同完成文献查找与系统设计
  - second：分成 Testing Group 和 PPT Group
  - third：最终整合与彩排
- 在分组执行阶段，Testing Group 必须每天与 PPT Group 同步一次
- 每日同步至少包括：
  - 当前进度
  - 最新图表或音频结果
  - 是否有设计变化
  - 是否出现会影响 slides 表述的新发现
- PPT Group 应在 Phase A 结束后立即开始理论页和结构页，而不是被动等待最终结果
- Slides 中的最终结论必须由 references 或实际实验结果支撑


## 测试计划与验收标准

### 必须完成的测试内容

- clean voice sample
- noisy voice sample with high-frequency noise
- filtered voice sample
- waveform comparison before and after filtering
- frequency-spectrum comparison before and after filtering
- 一段适合课堂展示的短音频 demo

### 验收标准

当满足以下条件时，项目可视为具备展示条件：

- 降噪流程能够完整跑通
- 至少有一组 waveform comparison 能清楚体现改善
- 至少有一组 spectrum comparison 能清楚体现改善
- 音频 demo 能在 2 分钟内让同学听懂效果
- 所选滤波器能用课程概念解释清楚
- slides 内容与实际实现一致
- 每位成员的贡献都能清楚说明

## 备注

- 当前默认使用高频噪声场景，除非后续测试证明它无法形成稳定 demo
- Python 和 MATLAB 都可以使用，但最终展示必须体现为一个统一系统
- 滤波方法默认保持基础、可解释，除非后续发现必须引入更强方法

# Presentation Outline 3.1

这份大纲是在 `Presentation_outline_3.0.md` 的基础上继续升级出来的。  
`3.0` 的重点是把原有 low-pass 方案扩展到 20 分钟展示；`3.1` 的重点是进一步加厚理论和方法层次，让 presentation 不只是一个基础低通滤波 demo，而是形成一条更完整的技术递进线：

`fixed low-pass filter -> frequency-domain mask -> Wiener-style mask`

这条线的好处是，它既保留了原来 low-pass 的直观性，又能自然引入更灵活的频域遮蔽方法，同时通过 Wiener filtering 的思想给 mask 一个更有理论支撑的来源。

---

## 一、核心叙事

这版 presentation 的核心故事可以这样概括：

我们先把语音降噪问题建模成一个可控的信号处理任务。  
第一步用基础 low-pass filter 作为 baseline，因为 high-frequency hiss 主要集中在高频。  
接着指出 low-pass 的局限：它是一个固定的频率响应，只能按频率粗略衰减，容易同时削弱语音高频细节。  
因此我们进一步引入 frequency-domain masking，让系统能够在频域或时频域里更细致地决定“哪些成分保留多一点，哪些成分压低多一点”。  
最后用 Wiener filtering 的思想解释 mask 的设计：如果某个频率区域中语音相对更强，就保留更多；如果噪声相对更强，就压制更多。

一句话版本：

`Low-pass is a fixed mask. Wiener-style frequency masking is a more flexible way to decide how much of each frequency component should be preserved.`

---

## 二、20 分钟时间分配

建议正式展示控制在 `20-22 min`，不含 Q&A。  
这版大纲比 3.0 增加了一个 improved method 部分，所以背景部分要稍微压缩，把时间让给理论和方法。

推荐时间分配如下：

1. Motivation and Problem Setup  
   `2 min`

2. Simulated Voice Denoising Scenario  
   `2 min`

3. Signal Analysis: Time Domain and Frequency Domain  
   `3 min`

4. Baseline Method: Low-pass Filtering  
   `3 min`

5. From Low-pass to Frequency-domain Masking  
   `3 min`

6. Wiener-style Mask Design  
   `3 min`

7. Demo and Result Comparison  
   `4 min`

8. Limitations and Conclusion  
   `2 min`

总时长大约 `22 min`，实际展示时可以压缩 demo 或背景部分，把整体控制在 `20 min` 左右。

---

## 三、PPT 设计大纲

推荐扩展成 `16-18` 页。  
这不是为了堆页数，而是因为现在要讲两个方法：一个 baseline，一个 improved method。每页只承担一个小任务，听众会更容易跟上。

---

### Slide 1. Title and Team

标题：

`Designing a Noise Reduction Filter for Voice Signals`

页面内容：

- 题目
- 组员
- 课程信息

设计建议：

- 深色背景
- 大标题
- 少字
- 不要急着放技术细节

建议时长：`30 sec`

---

### Slide 2. Motivation

这一页回答“为什么语音降噪值得做”。

内容：

- 语音信号在公共广播、语音录音、语音助手和通话系统中很常见
- 噪声会降低清晰度和可懂度
- 项目关注的是 high-frequency hiss 对语音质量的影响

设计建议：

- 一句主结论放大
- 配一个简单的 noisy speech 场景图或流程图

建议时长：`1 min`

---

### Slide 3. Scenario and Scope

这一页讲清楚你们不是直接录真实高铁站，而是做可控仿真。

内容：

- 应用背景：公共广播 / 站台播报
- 实验方式：clean voice + simulated hiss noise
- 目标：保留现实意义，同时保证分析可控

关键句：

`We use a realistic motivation with a controlled simulation setup.`

建议时长：`1 min`

---

### Slide 4. Problem Statement

明确输入、系统和输出。

内容：

- Input: noisy voice
- System: denoising filter
- Output: enhanced voice
- Goal: suppress hiss while preserving speech information

设计建议：

- 用简单 block diagram
- 不要堆文字

建议时长：`1 min`

---

### Slide 5. Signal Model

这一页把问题拉回 Signals and Systems。

内容：

`x_noisy[n] = x_clean[n] + n_hiss[n]`

要讲：

- clean voice 和 hiss noise 都是信号
- noisy voice 是信号叠加
- filter 是输入输出系统

课程联系：

- signal superposition
- input-output system
- LTI system viewpoint

建议时长：`1 min`

---

### Slide 6. Visualizing the Signals

这一页让观众知道你们怎么看图。

内容：

- waveform: time-domain shape
- FFT spectrum: overall frequency distribution
- spectrogram: time-frequency energy map

设计建议：

- 三个小示意图并列
- 每个图只配一句解释

建议时长：`1.5 min`

---

### Slide 7. Frequency-domain Observation

这一页展示为什么 high-frequency hiss 适合先用低通思路。

内容：

- clean voice 的主要结构集中在低到中频
- hiss noise 在高频区域更明显
- noisy voice 的高频背景被抬高

适合放图：

- spectrum 图
- spectrogram 图

建议时长：`1.5 min`

---

### Slide 8. Baseline: Low-pass Filter

这一页介绍第一种方法。

内容：

- low-pass filter 保留低频，衰减高频
- 它可以看作一个固定的 frequency mask
- cutoff 决定保留和衰减的边界

关键表达：

`A low-pass filter is a simple fixed mask in the frequency domain.`

建议时长：`1.5 min`

---

### Slide 9. Baseline Parameter Choice

这一页讲 cutoff 为什么不是随便选。

内容：

- 比较不同 cutoff
- cutoff 太低：噪声少，但语音变闷
- cutoff 太高：语音自然，但噪声残留更多
- 当前主 demo 使用 `3200 Hz`

适合放图：

- parameter comparison 图

建议时长：`1.5 min`

---

### Slide 10. Why Low-pass Is Not Enough

这一页是从 baseline 过渡到 improved method 的关键。

内容：

- low-pass 只按频率做固定衰减
- 它不知道某个频率区域中到底是语音占主导还是噪声占主导
- 因此它会压制噪声，也可能压掉语音细节

关键句：

`The baseline is explainable, but too coarse.`

建议时长：`1.5 min`

---

### Slide 11. Frequency-domain Masking

这一页正式引入 frequency-domain masking。

内容：

`Y(f) = M(f)X(f)`

或者对于 STFT：

`Y(t, f) = M(t, f)X(t, f)`

要讲：

- mask 的值表示保留多少
- 接近 1：保留
- 接近 0：压制
- low-pass 是固定 mask，frequency mask 可以更灵活

设计建议：

- 画一个 mask 热力图
- 用颜色表现保留和压制

建议时长：`2 min`

---

### Slide 12. Wiener-style Mask

这一页给 frequency mask 一个理论来源。

内容：

可以用简化表达：

`M(f) = P_speech(f) / (P_speech(f) + P_noise(f))`

要讲：

- 如果语音能量相对强，mask 接近 1
- 如果噪声能量相对强，mask 接近 0
- 这和 Wiener filtering 的思想一致

注意：

- 不要说自己做了工业级 Wiener denoising
- 可以说是 `Wiener-style frequency mask`

建议时长：`2 min`

---

### Slide 13. Improved Method Workflow

这一页展示第二种方法的系统流程。

建议流程：

`noisy voice -> STFT -> estimate noise power -> compute mask -> apply mask -> inverse STFT -> enhanced voice`

这一页的作用是让第二方法不显得像黑箱。

建议时长：`1.5 min`

---

### Slide 14. Mask Visualization

这是视觉效果最关键的一页。

内容：

- noisy spectrogram
- estimated mask / Wiener gain
- masked spectrogram

要讲：

- mask 亮的地方表示更多保留
- mask 暗的地方表示更多压制
- 高频噪声区域被更有针对性地压低

设计建议：

- 用三联图
- 中间放 mask 图
- 视觉上形成 `Noisy -> Mask -> Enhanced`

建议时长：`2 min`

---

### Slide 15. Result Comparison

这一页比较 baseline 和 improved method。

内容：

- noisy voice
- low-pass result
- Wiener-style mask result

可以比较：

- 听感
- spectrogram
- 高频抑制
- 语音细节保留

设计建议：

- 不要塞太多指标
- 重点放一张对比图和一句结论

建议时长：`2 min`

---

### Slide 16. Demo

这一页实际播放 demo。

播放顺序建议：

1. clean voice
2. noisy voice
3. low-pass filtered voice
4. Wiener-style masked voice

讲解重点：

- low-pass 是基础版本
- mask 方法更灵活
- 两者都不是完美恢复，但可以体现不同设计思想

建议时长：`2 min`

---

### Slide 17. Limitations

这一页讲清楚边界。

内容：

- 仿真噪声比真实环境简单
- mask 依赖噪声估计
- 如果噪声和语音高度重叠，分离会更困难
- 更复杂方法可能需要 adaptive filtering 或 learning-based denoising

建议时长：`1.5 min`

---

### Slide 18. Conclusion

最后收束。

建议结论：

- We modeled voice denoising as a signals-and-systems problem.
- Low-pass filtering provides a clear baseline.
- Frequency-domain masking extends the same idea in a more flexible way.
- A Wiener-style mask gives a principled way to visualize and design frequency-dependent attenuation.

建议时长：`1 min`

---

## 四、需要新增的实验与图

为了支撑这版 `3.1` 大纲，需要在现有项目基础上补一组 improved method 的实验结果。

建议新增：

1. `wiener_masked_voice.wav`

2. `wiener_mask.png`

3. `wiener_mask_spectrogram.png`

4. `method_comparison.png`

5. 如果时间允许，补一个 `lowpass_vs_mask_metrics.json`

这些文件的作用不是替换原来的 low-pass 结果，而是让低通滤波成为 baseline，再用 mask 方法作为升级版。

---

## 五、PPT 视觉设计建议

由于这版加入了 mask，可视化会比原来更有表现力。建议整套 PPT 继续保持深色背景，但在图像页加入更鲜明的颜色层次。

建议视觉原则：

- 背景继续使用深色
- 标题保持极简
- 每页只讲一个结论
- mask 图使用热力图色彩
- clean / noisy / low-pass / mask result 使用固定颜色
- 重点结果页使用大图，不要塞很多文字

推荐颜色逻辑：

- clean: blue
- noisy: red
- low-pass: green
- Wiener-style mask result: cyan or gold
- mask heatmap: magma / inferno style

---

## 六、这版大纲的价值

相比 `3.0`，这版 `3.1` 主要解决三个问题：

1. 理论更厚  
   不再只是介绍 low-pass，而是讲从固定频率响应到自适应频域增益的升级。

2. demo 更有层次  
   可以比较 noisy、low-pass、mask result，不再只有单一结果。

3. 图更有展示感  
   mask 热力图和 spectrogram 对比会让展示更直观，也更容易撑住 20 分钟。

---

## 七、下一步建议

接下来最值得做的是先补实验，再改 PPT。

推荐顺序：

1. 实现一个简化版 Wiener-style frequency mask
2. 生成 masked audio 和 mask 图
3. 比较 low-pass 和 mask result
4. 根据结果决定是否正式放进 PPT
5. 再基于这份 `3.1` 大纲更新 slide deck

这样比较稳，因为如果 mask 结果不够好看，还可以只把它作为 extension；如果效果好，就可以把它升级成第二主方法。

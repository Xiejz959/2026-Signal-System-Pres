# Presentation Outline 3.0

这份大纲是在现有项目内容基础上扩展出来的，目标是把全组展示内容稳定撑到 **20 分钟左右**。  
这里默认不把 Q&A 计算在内，只考虑正式 presentation 的主体部分。

这版大纲的原则不是增加很多新技术，而是把你们已经做出来的内容讲得更完整、更像一个真正的故事。也就是说，我们不额外扩展太多算法，而是把 **背景、分析、设计、结果、局限** 这几块展开。

---

## 一、整体结构与时间分配

建议全组展示控制在 `20-22` 分钟左右，这样比较稳。下面是一版推荐分配：

1. Introduction and Motivation  
   `2 min`

2. Real-world Scenario and Problem Definition  
   `2 min`

3. Signal Background: Voice and High-frequency Hiss  
   `3 min`

4. Why Fourier Transform Helps  
   `3 min`

5. Filter Design Process  
   `4 min`

6. Parameter Comparison and Design Choice  
   `2.5 min`

7. Demo and Result Interpretation  
   `3 min`

8. Limitations and Possible Extensions  
   `2 min`

9. Conclusion  
   `1 min`

这样总时长大约是 `22.5 min` 的上限版本。实际展示时可以通过压缩某些页，把它控制在 `20 min` 左右。

---

## 二、推荐页面结构

如果按 PPT 来组织，我建议扩展成 `14-15` 页左右，而不是原来更紧凑的 12 页。  
原因不是为了凑页数，而是为了让逻辑更舒服，不需要一页塞太多内容。

推荐结构如下。

### Slide 1. Title and Team

内容：

- 题目
- 小组成员
- 课程信息

这一页不要讲太久，控制在 `20-30 秒`。

---

### Slide 2. Motivation

这一页回答“为什么值得做”。

可以讲：

- 语音降噪在现实中很常见
- 公共广播、语音录音、语音助手、通话系统都受噪声影响
- 噪声会直接影响清晰度和可懂度

这一页的目标不是技术，而是建立问题的重要性。

建议时长：`1 min`

---

### Slide 3. Real-world Scenario

这一页专门讲应用背景。

可以讲：

- 我们选用的是公共广播 / 站台播报这一类语音场景
- 这类场景里的语音通常希望清楚、稳定、容易理解
- 现实系统中经常会受到设备噪声或高频底噪影响

这页的作用是把题目和现实世界连起来。

建议时长：`1 min`

---

### Slide 4. Why Simulation Instead of Real Recording

这一页很值得单独拿出来，因为它能提前回答老师和同学可能会有的疑问。

要讲清楚：

- 真实高铁站或站台环境太复杂
- 会同时包含人声、设备声、低频轰鸣、混响等多种因素
- 这会让基础滤波器原理难以解释
- 所以我们采用“真实背景 + 可控仿真”的方式

建议时长：`1 min`

---

### Slide 5. Problem Statement

明确输入、输出、目标。

可以写成：

- Input: noisy voice
- Output: filtered voice
- Goal: suppress high-frequency noise while preserving useful speech information

同时强调：

- 这不是完美恢复问题
- 而是噪声压制和语音保真之间的平衡问题

建议时长：`1 min`

---

### Slide 6. Voice and Noise Characteristics

这一页开始进入真正的信号分析。

需要讲：

- 语音的主要能量分布在哪里
- high-frequency hiss 在频域上有什么特点
- 为什么这两者不是完全重叠

这一页适合放：

- clean voice 的图
- hiss noise 的图
- noisy voice 的图

建议时长：`2 min`

---

### Slide 7. How to Read the Visualizations

这一页是为了把 waveform、FFT、spectrogram 的阅读方式交代清楚。  
如果不讲这页，后面很多图会变成“展示了，但没完全解释”。

这一页可以简短说明：

- waveform 看的是时域变化
- FFT 看的是整体频率能量分布
- spectrogram 看的是时间和频率上的能量分布

重点是让观众知道：

- 为什么 noisy 的高频会变亮
- 为什么 filtered 的高频会变暗

建议时长：`1.5 min`

---

### Slide 8. Why Fourier Transform Helps

这一页是课程联系的重要部分。

要讲清楚：

- 时域里，语音和噪声叠加后不容易分开
- 傅里叶变换把问题带到频域
- 在频域里更容易看到噪声集中在哪些频率
- 所以 Fourier Transform 的作用是指导滤波器设计，而不是直接完成降噪

这一页建议配一句核心结论：

`Fourier Transform helps us see where the noise is, so we can decide what the filter should suppress.`

建议时长：`1.5 min`

---

### Slide 9. Filter Design Idea

这一页专门讲“为什么选择 low-pass filter”。

要讲：

- 当前噪声主要集中在高频
- low-pass 是最自然、最可解释的第一选择
- 这符合信号与系统里“系统频率响应”的思路

这一页不要讲得太程序化，不要变成“我们用了哪个库函数”，而是讲系统设计思想。

建议时长：`1.5 min`

---

### Slide 10. System Workflow

把整个系统流程完整交代出来。

建议结构：

`clean voice -> add hiss noise -> noisy voice -> frequency-domain analysis -> low-pass filter -> filtered voice`

这里要强调的是：

- 建模
- 分析
- 设计
- 比较
- 输出

这页很适合用来回应“你们不只是调包”的疑问。

建议时长：`1.5 min`

---

### Slide 11. Parameter Comparison

这一页是为了让“系统设计”更像一个真正的设计过程，而不是直接报答案。

要讲：

- 我们比较了不同 cutoff
- cutoff 太低会损失语音细节
- cutoff 太高会保留更多高频噪声
- 最终选 `3200 Hz` 作为主 demo

如果要讲得更成熟一点，还可以补一句：

- 参数比较的目的不是寻找唯一正确答案，而是在噪声压制和语音保真之间找一个更合适的平衡点

建议时长：`2 min`

---

### Slide 12. Demo Setup

这一页用于进入 demo 之前的过渡。

内容包括：

- 使用同一段语音样本
- 播放 clean / noisy / filtered
- 配合 waveform 和 spectrogram 一起展示

这一页讲完以后，观众应该已经知道接下来会看什么、听什么。

建议时长：`1 min`

---

### Slide 13. Demo and Results

这是展示效果的核心页。

建议分两步讲：

1. 先播放音频
   - clean
   - noisy
   - filtered

2. 再解释图像
   - noisy 的高频背景增强
   - filtered 的高频区域变暗
   - 语音主体结构仍然保留

这一页不要太急，因为它是观众最容易留下印象的一页。

建议时长：`3 min`

---

### Slide 14. Discussion and Limitations

这一页非常重要，它会让你们显得不只是“做出一个结果”，而是真的理解了这个方法。

可以讲：

- 为什么滤波后语音会有一点变闷
- 为什么 low-pass 不是万能的
- 如果环境噪声更复杂，这种方法会受到限制
- 更复杂场景可能需要更高级的方法

建议时长：`2 min`

---

### Slide 15. Conclusion

最后用非常清楚的方式收束。

可以只保留三到四句：

- We modeled a realistic but controllable voice denoising problem.
- Fourier Transform helped us analyze the noise in the frequency domain.
- A basic low-pass filter reduced the high-frequency hiss effectively.
- The result shows both improvement and tradeoff.

建议时长：`1 min`

---

## 三、这一版大纲相比原来扩充了什么

和之前较短的版本相比，这一版主要增加了 4 个层次：

1. 把应用背景讲厚了  
   不只是说“这是语音降噪”，而是交代为什么选公共广播场景、为什么做仿真。

2. 把图像解释单独拿出来了  
   不然 waveform、FFT、spectrogram 很容易只是展示，而没有被真正讲懂。

3. 把系统设计过程讲成了“设计过程”  
   不是直接说结果，而是交代为什么选 low-pass、为什么做 cutoff 比较。

4. 把 limitations 独立成一页  
   这样项目会显得更完整，也更适合较长时间的 presentation。

---

## 四、对你们当前内容的建议

如果按这份大纲走，你们现在不用去大规模补新实验。  
最合理的做法是：

- 保留当前主实验路线
- 保留 `3200 Hz` 作为主 demo
- 通过更细的讲解把已有内容撑到 20 分钟

也就是说，这一版扩展主要依靠：

- 更完整的背景说明
- 更清楚的图像阅读
- 更成熟的系统设计逻辑
- 更明确的局限分析

而不是靠增加一堆新方法。

---

## 五、下一步怎么推进

基于这份大纲，我建议后面按这个顺序继续：

1. 先按这份结构改 PPT 页数和顺序
2. 把现有图表分别对应到 Slide 6、7、11、13
3. 把 demo 页拆成“设置说明”和“结果展示”两页
4. 给每一页写一句主结论
5. 再开始准备逐页讲稿

如果需要的话，下一步就可以直接在这份 `3.0` 大纲基础上继续写：

- `Presentation_script_3.0.md`
- 或者一版新的 slide draft

# Presentation Script Bilingual 1.0

这份讲稿按当前 `Voice_Noise_Presentation_1.1.pptx` 的 12 页结构来写。  
形式采用中英双语对照，方便你们根据实际需要做取舍。中文版本更适合先熟悉逻辑，英文版本适合直接上台表达或整理英文讲稿。

---

## Slide 1. Title and Team

**中文**

大家好，我们这次展示的题目是 **Designing a Noise Reduction Filter for Voice Signals**。  
我们想研究的是，在一个语音信号受到高频 hiss 噪声污染的场景下，能不能用一个基础、可解释的滤波系统，把语音变得更清晰一些。

**English**

Hello everyone. Our topic today is **Designing a Noise Reduction Filter for Voice Signals**.  
We focus on a simple but meaningful question: when a voice signal is corrupted by high-frequency hiss noise, can a basic and explainable filter make the speech clearer?

---

## Slide 2. Motivation

**中文**

语音降噪是一个很实际的问题。  
在公共广播、语音录音、语音助手和通话系统中，背景噪声都会直接影响语音的清晰度和可懂度。  
我们这次没有去做一个特别复杂的系统，而是选了一个适合课堂展示的小问题：高频 hiss 噪声下的语音降噪。

**English**

Voice denoising is a very practical problem.  
In public announcements, recordings, voice assistants, and communication systems, background noise directly affects speech clarity and intelligibility.  
Instead of building a very complex system, we chose a smaller and more explainable problem: reducing high-frequency hiss noise in voice signals.

---

## Slide 3. Problem Statement

**中文**

这个项目的输入是带噪语音，输出是经过处理后更清晰的语音。  
我们的目标不是完美恢复原始语音，而是在抑制高频噪声的同时，尽量保留语音的主要信息。  
所以这本质上是一个噪声压制和语音保真之间的平衡问题。

**English**

The input of our system is noisy speech, and the output is a cleaner processed voice signal.  
Our goal is not perfect recovery, but a better balance: suppress the high-frequency noise while keeping the main speech information.  
So in essence, this is a tradeoff between noise reduction and speech preservation.

---

## Slide 4. Simulated Application Scenario

**中文**

我们把公共广播或站台播报作为应用背景，但没有直接去录一个复杂真实环境。  
原因是，真实站台环境通常会同时包含人声、设备声、低频噪声和混响，这样会让问题变得过于复杂。  
所以我们采用的是“真实背景 + 可控仿真”的方式，也就是保留现实意义，但让实验条件更稳定、更容易分析。

**English**

We use a public-announcement or station-broadcast scenario as the application background, but we do not directly record a complicated real environment.  
The reason is that a real station usually contains many factors at the same time, such as human voices, equipment noise, low-frequency rumble, and reverberation.  
So we use a “real-world motivation plus controlled simulation” approach, which keeps the scenario meaningful while making the experiment easier to analyze.

---

## Slide 5. Signal Characteristics

**中文**

这里我们先看信号特征。  
语音的主要信息通常集中在较低到中频范围，而我们构造的 hiss 噪声主要增强高频区域。  
所以在 noisy voice 里面，可以看到高频部分被明显抬高，这正是后面滤波器设计的依据。

**English**

Here we first look at the signal characteristics.  
The main information in speech is usually concentrated in the low-to-mid frequency range, while our simulated hiss mainly increases the high-frequency region.  
So in the noisy voice, we can clearly see that the high-frequency part is raised, and this becomes the basis for our filter design.

---

## Slide 6. Why Fourier Transform Helps

**中文**

在时域里，语音和噪声叠加以后，其实很难直接看出哪一部分是噪声。  
傅里叶变换的作用，就是把这个问题转到频域里去看。  
在频域中，我们能更清楚地看到噪声主要集中在哪些频率上，因此它不是直接帮我们降噪，而是帮我们决定滤波器应该怎么设计。

**English**

In the time domain, once speech and noise are mixed together, it is difficult to directly identify which part is noise.  
The role of the Fourier Transform is to move the problem into the frequency domain.  
In the frequency domain, we can see more clearly where the noise energy is concentrated. So the Fourier Transform does not directly remove noise; instead, it guides the filter design.

---

## Slide 7. Filter Design Idea

**中文**

基于前面的频域观察，我们先选择了最基础的 low-pass filter。  
因为当前的噪声主要集中在高频，所以低通滤波器是最自然的第一选择。  
我们比较了 `2800 Hz`、`3200 Hz` 和 `3600 Hz` 三组 cutoff。  
最后选 `3200 Hz` 作为主 demo 版本，因为它在高频噪声压制和语音清晰度保留之间表现得最平衡。

**English**

Based on the frequency-domain observations, we first chose a basic low-pass filter.  
Since the noise is mainly concentrated at high frequencies, a low-pass filter is the most natural starting point.  
We compared three cutoff frequencies: `2800 Hz`, `3200 Hz`, and `3600 Hz`.  
In the end, we selected `3200 Hz` as the main demo version because it gave the best balance between suppressing hiss and preserving speech clarity.

---

## Slide 8. System Workflow

**中文**

整个系统流程其实很清楚。  
我们先生成 clean voice，然后加入模拟的 hiss 噪声，得到 noisy voice。  
接着对 noisy voice 进行频域分析，并用 low-pass filter 去处理，最后得到 filtered voice。  
所以这个项目不只是“调用一个包”，而是经历了建模、分析、设计、比较和评估几个完整步骤。

**English**

The full system workflow is actually quite clear.  
We first generate a clean voice signal, then add simulated hiss noise to obtain the noisy voice.  
After that, we analyze the signal in the frequency domain and apply a low-pass filter to produce the filtered voice.  
So this project is not just about calling a package. It includes modeling, analysis, design, comparison, and evaluation.

---

## Slide 9. Demo Setup

**中文**

在 demo 部分，我们会播放三段音频：clean voice、noisy voice 和 filtered voice。  
这三段音频都来自同一段样本，这样前后对比才是公平的。  
听完之后，我们会结合 waveform 和 spectrogram 再解释图像上的变化。

**English**

In the demo section, we will play three audio clips: the clean voice, the noisy voice, and the filtered voice.  
All three clips come from the same sample, so the comparison is fair and consistent.  
After listening, we will use the waveform and spectrogram to explain the visible differences.

---

## Slide 10. Results

**中文**

这里是结果页。  
从听感上看，滤波后的语音比 noisy voice 更干净，高频 hiss 被明显压低。  
从图上看，不管是 waveform 还是 spectrogram，都能看到处理前后确实发生了变化。  
尤其是在 spectrogram 中，高频区域被削弱得更明显，这和我们的设计目标是一致的。

**English**

This is our results slide.  
From the listening perspective, the filtered voice sounds cleaner than the noisy voice, and the high-frequency hiss is clearly reduced.  
From the figures, both the waveform and the spectrogram show that the signal changes after filtering.  
Especially in the spectrogram, the high-frequency region is reduced more clearly, which matches our design goal.

---

## Slide 11. Discussion and Limitations

**中文**

这个方法为什么有效？因为我们构造的噪声主要集中在高频，而 low-pass filter 正好对高频衰减更强。  
但它也不是完美方案，因为语音本身也有一部分高频细节，所以滤波之后声音会稍微变钝一点。  
如果把问题换成更复杂的真实环境噪声，那基础 low-pass filter 就不一定够用了，这也是这个项目的主要局限。

**English**

Why does this method work? Because our simulated noise is mainly concentrated at high frequencies, and the low-pass filter naturally attenuates those components more strongly.  
But it is not a perfect solution, because speech itself also contains some high-frequency detail, so the filtered voice can sound slightly softened.  
If we move to a more complicated real-world noise environment, a basic low-pass filter may no longer be enough. That is the main limitation of this project.

---

## Slide 12. Conclusion and Q&A

**中文**

总的来说，我们把一个真实语音场景抽象成了一个可控的信号与系统问题。  
通过频域分析，我们找到了噪声主要集中的区域，并据此设计了一个基础 low-pass filter。  
最终结果说明，这种方法在当前高频 hiss 场景下是有效的，但它也体现了噪声抑制和语音保真之间的 tradeoff。  
谢谢大家，欢迎提问。

**English**

In summary, we turned a real voice-related problem into a controlled Signals and Systems case study.  
Using frequency-domain analysis, we identified where the noise was concentrated and designed a basic low-pass filter accordingly.  
The final result shows that this method works in the current high-frequency hiss scenario, while also demonstrating the tradeoff between noise suppression and speech preservation.  
Thank you, and we welcome your questions.

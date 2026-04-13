# Final References 1.0

本项目目前采用简化的展示引用方式：

- 在 PPT 中，涉及背景或方法说明的页面使用简短来源提示
- 在仓库中保留一份完整参考资料清单，方便展示和答辩时统一说明

下面这份清单按用途分组整理。

## 1. 语音频率范围与可懂度背景

### Speech Audiometry - StatPearls

- 来源：[NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/n/statpearls/article-142875/)
- 用途：支持语音可懂度与主要语音频率范围的背景说明
- 可用于支撑：
  - 为什么语音的关键信息集中在较低到中频范围
  - 为什么频域分析对语音问题是合理的

### Audiogram Interpretation - StatPearls

- 来源：[NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK578179/)
- 用途：补充频率范围与听觉相关背景
- 可用于支撑：
  - 语音与听觉敏感频段的关系
  - 为什么高频噪声会影响语音清晰度

## 2. 公共广播 / 铁路站台背景

### Calculating speech intelligibility for the design of public address systems at railway stations

- 来源：[SAGE / Proc IMechE Part F](https://journals.sagepub.com/doi/abs/10.1243/0954409011531611)
- 用途：支持“铁路站台 / 公共广播环境中 speech intelligibility 很重要”的背景
- 可用于支撑：
  - 为什么公共广播是一个合理应用背景
  - 为什么站台环境中的噪声问题值得研究

### Effects of Artificial Synthetic Speech Control of SNR and Speech Rate on the Intelligibility of Train Station Announcements

- 来源：[Springer](https://link.springer.com/article/10.1007/s40857-023-00306-8)
- 用途：支持“车站播报清晰度与噪声、语速等因素相关”的背景
- 可用于支撑：
  - 为什么噪声会直接影响广播语音理解
  - 为什么可懂度是这类系统的重要目标

### Sound field characteristics of underground railway stations – Effect of interior materials and noise source positions

- 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0003682X12001569)
- 用途：支持“真实站台环境非常复杂，因此本项目选择仿真建模”的说明
- 可用于支撑：
  - 为什么真实环境噪声不适合直接作为基础滤波实验主场景
  - 为什么项目采用“真实背景 + 可控仿真”

## 3. 滤波与实现参考

### Oppenheim, Willsky, Nawab - Signals and Systems

- 来源：课程教材
- 用途：支持信号叠加、系统观点、频率响应、Fourier Transform 等核心课程概念
- 可用于支撑：
  - 这个项目为什么属于 Signals and Systems
  - 为什么滤波器可以看成系统

### SciPy Signal Processing Documentation

- 来源：[SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/signal.html)
- 用途：支持 Butterworth filter、filtfilt 等数字滤波实现
- 可用于支撑：
  - Python 中基础滤波器如何实现
  - 为什么当前实现方式合理

## 4. 可选补充

如果你们最后在讲述中提到“更复杂的语音增强方法”，可以在补充资料里提一句下面这些方向，但不建议把它们放成主方法来源：

- MathWorks speech denoising examples
- spectral subtraction
- deep learning based speech enhancement

## 展示时的使用建议

- Motivation / Scenario 页面：引用 railway station / announcement 相关资料
- Signal Characteristics / Why Fourier Transform Helps 页面：引用语音频率范围相关资料
- 方法页：引用教材和 SciPy 实现说明
- 如果最后需要一页 References，可以把上面 4-5 条最关键的来源精简列出

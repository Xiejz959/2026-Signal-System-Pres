# Codes
<a id="Chinese"></a>

[英文](README.md#English)

这个文件夹用于存放项目中使用到的各类支持代码。

这里可能包括 Python 脚本、MATLAB 程序、小型仿真、绘图工具，以及其他为分析、演示或 presentation 材料准备而编写的代码。简单来说，只要它能运行并且对项目有帮助，就适合放在这里。 💻

## 使用方法

这个文件夹推荐使用的 conda 环境文件是：

- `environment_voice.yml`

如果想快速配置环境，可以运行：

```bash
bash setup_env.sh
conda activate voice
```

当前这个文件夹中比较重要的文件包括：

- `simulate_voice_noise_demo.py`：用于生成 demo 音频样本
- `environment_voice.yml`：共享的 conda 环境定义文件
- `setup_env.sh`：共享环境的快速配置脚本

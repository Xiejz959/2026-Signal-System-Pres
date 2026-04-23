"""Analyze clean/noise/noisy signals and generate the first filtered result.

This script:
1. loads the generated demo audio
2. compares several low-pass cutoff frequencies
3. exports the selected filtered voice
4. saves waveform / spectrum / spectrogram figures for presentation
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy import signal

# ------------------------
# 文件 / 目录 / 常量设置
# ------------------------
BASE_DIR = Path(__file__).resolve().parent
# 生成或读取音频文件的目录（脚本同级目录下的 generated_audio 子目录）
AUDIO_DIR = BASE_DIR / "generated_audio"
# 输出图表存放目录（父目录下的 Charts/analysis_round1）
CHART_DIR = BASE_DIR.parent / "Charts" / "analysis_round1"

# 期望采样率（用于提示 / 验证）
FS_EXPECTED = 16_000
# 低通滤波器的阶数（Butterworth）
FILTER_ORDER = 6
# 要比较的低通截止频率候选列表（Hz）
CUTOFF_CANDIDATES = [4000, 5000, 6000, 7000]
# 定义三个不同的截止频率用于实验
EXPERIMENT_CUTOFFS = [3500, 5500, 7000]   ###
# 用于演示比较的窗口时长（秒）
DEMO_WINDOW_SEC = 4.0

# ------------------------
# 工具函数（I/O / 归一化 / 滤波 / 分析）
# ------------------------
def read_audio(name: str) -> tuple[np.ndarray, int]:
    """
    读取音频文件并返回单通道浮点数组与采样率。

    参数:
        name: 音频文件名（相对于 AUDIO_DIR）

    返回:
        x: 音频样本数组（float64，单通道）
        fs: 采样率（Hz）
    """
    x, fs = sf.read(AUDIO_DIR / name)
    # 如果音频是多通道，取平均以获得单通道（简单混合）
    if x.ndim > 1:
        x = x.mean(axis=1)
    # 转换为双精度浮点以保持数值稳定
    return x.astype(np.float64), fs

def normalize_peak(x: np.ndarray, peak: float = 0.92) -> np.ndarray:
    """
    将信号按峰值进行缩放，使最大绝对值为指定峰值（避免裁剪并标准化音量）。

    参数:
        x: 输入信号
        peak: 归一化后的峰值目标（默认为 0.92）

    返回:
        归一化后的信号副本（若输入全零则返回副本）
    """
    m = np.max(np.abs(x))
    if m == 0:
        return x.copy()
    return x * (peak / m)

def save_audio(name: str, x: np.ndarray, fs: int) -> None:
    """
    将音频写入到 AUDIO_DIR 下指定文件名。

    参数:
        name: 保存的文件名
        x: 音频样本数组
        fs: 采样率（Hz）
    """
    # 确保目录存在
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    # 使用 soundfile 写文件，格式由文件扩展名决定
    sf.write(AUDIO_DIR / name, x, fs)

def lowpass_filter(x: np.ndarray, fs: int, cutoff: float, order: int = 4) -> np.ndarray:
    """
    对信号应用 Butterworth 低通滤波器（零相位滤波，filtfilt）。

    参数:
        x: 输入信号
        fs: 采样率（Hz）
        cutoff: 截止频率（Hz）
        order: 滤波器阶数（默认 4）

    返回:
        经过滤波并进行峰值归一化的信号
    """
    # 使用 SciPy 的数字 Butterworth 设计（指定 fs 参数获得数字滤波器特性）
    b, a = signal.butter(order, cutoff, btype="low", fs=fs)
    # filtfilt 做零相位滤波以避免相位畸变
    y = signal.filtfilt(b, a, x)
    # 归一化处理以控制输出幅度
    return normalize_peak(y)

def snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    """
    计算参考信号与估计信号之间的信噪比（SNR，单位 dB）。

    SNR 定义为 10 * log10( sum(reference^2) / sum((estimate-reference)^2) )

    注意：如果误差接近 0，会得到非常大的值或无穷大，调用者需保证输入非零长度。
    """
    error = estimate - reference
    return 10.0 * np.log10(np.sum(reference**2) / np.sum(error**2))

def magnitude_spectrum(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray]:
    """
    计算单段信号的单边幅值谱（使用 rfft）。

    参数:
        x: 输入信号
        fs: 采样率（Hz）

    返回:
        freqs: 频率轴（Hz）
        mag: 对应频点的幅值（非对数）
    """
    freqs = np.fft.rfftfreq(len(x), 1 / fs)
    mag = np.abs(np.fft.rfft(x))
    return freqs, mag

# ------------------------
# 候选滤波器比较
# ------------------------
def compare_candidates(clean: np.ndarray, noisy: np.ndarray, fs: int) -> list[dict]:
    """
    针对预设的 CUTOFF_CANDIDATES 对 noisy 信号应用低通滤波，并与 clean 信号比较，
    计算每个候选的 SNR、相关性以及高频能量抑制比率等指标。

    参数:
        clean: 干净人声参考信号（同长度或更长）
        noisy: 含噪人声信号（待滤波）
        fs: 采样率（Hz）

    返回:
        一个字典列表，每项包含该候选截止频率对应的度量结果：
            - cutoff_hz: 截止频率
            - filter_order: 滤波器阶数
            - input_snr_db: 原始 noisy 相对 clean 的 SNR（dB）
            - output_snr_db: 处理后相对 clean 的 SNR（dB）
            - snr_improvement_db: SNR 改善值（dB）
            - corr_with_clean: 与 clean 的相关系数
            - high_freq_ratio: 在高频段（从 3500Hz 起）处理后能量相对原 noisy 的比率
    """
    # 对齐信号长度（取最短的那段）
    min_length = min(len(clean), len(noisy))
    clean = clean[:min_length]
    noisy = noisy[:min_length]

    # 记录输入时的 SNR（noisy 相对于 clean）
    input_snr = snr_db(clean, noisy)
    records = []

    for cutoff in CUTOFF_CANDIDATES:
        # 对 noisy 应用低通滤波
        filt = lowpass_filter(noisy, fs, cutoff, FILTER_ORDER)

        # 计算输出 SNR（滤波后相对于 clean）
        out_snr = snr_db(clean, filt)

        # 计算时域相关系数（Pearson）
        corr = float(np.corrcoef(clean, filt)[0, 1])

        # 计算高频能量比：选择频谱的从 3500Hz 开始的段落进行比较
        # hf_start 的计算：基于 rfft 的长度与 Nyquist（这里通过比例估算索引）
        hf_start = int(len(np.fft.rfft(noisy)) * 3500 / (fs / 2))
        noisy_fft = np.abs(np.fft.rfft(noisy))
        filt_fft = np.abs(np.fft.rfft(filt))
        # 为避免除以零，理论上可以加小量，但保留原意（假设 noisy_fft 均值不为零）
        hf_ratio = float(np.mean(filt_fft[hf_start:]) / np.mean(noisy_fft[hf_start:]))

        records.append(
            {
                "cutoff_hz": cutoff,
                "filter_order": FILTER_ORDER,
                "input_snr_db": round(float(input_snr), 3),
                "output_snr_db": round(float(out_snr), 3),
                "snr_improvement_db": round(float(out_snr - input_snr), 3),
                "corr_with_clean": round(corr, 4),
                "high_freq_ratio": round(hf_ratio, 4),
            }
        )
    return records

# ------------------------
# 绘图相关函数（保存并关闭图像以免占用内存）
# ------------------------
def plot_waveforms(clean: np.ndarray, noise: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
    """
    保存对比波形图（4 行：clean / noise / noisy / filtered）。

    参数:
        clean: 干净人声
        noise: 噪声信号（例如 hiss）
        noisy: 含噪人声
        filtered: 处理后的音频
        fs: 采样率（Hz）
    """
    # 对齐到相同最短长度
    min_length = min(len(clean), len(noise), len(noisy), len(filtered))
    clean = clean[:min_length]
    noise = noise[:min_length]
    noisy = noisy[:min_length]
    filtered = filtered[:min_length]

    # 时间轴
    t = np.arange(min_length) / fs

    fig, axes = plt.subplots(4, 1, figsize=(13, 9), sharex=True)
    pairs = [
        ("Clean Voice", clean, "tab:blue"),
        ("Hiss Noise", noise, "tab:orange"),
        ("Noisy Voice", noisy, "tab:red"),
        ("Filtered Voice", filtered, "tab:green"),
    ]
    # 绘制各行信号
    for ax, (title, x, color) in zip(axes, pairs):
        ax.plot(t, x, color=color, linewidth=0.8)
        ax.set_title(title)
        ax.set_ylabel("Amp.")
        ax.grid(alpha=0.25)
    axes[-1].set_xlabel("Time (s)")
    fig.suptitle("Waveform Comparison", fontsize=14)
    fig.tight_layout()

    # 保存为 PNG（高分辨率），并关闭 figure 释放内存
    fig.savefig(CHART_DIR / "waveforms_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

def plot_spectra(clean: np.ndarray, noise: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int, ylimit: float = None) -> None:
    """
    保存 2x2 的幅度谱图（FFT magnitude）。

    参数:
        clean, noise, noisy, filtered: 四个信号数组
        fs: 采样率（Hz）
        ylimit: y 轴的最大值（默认为 None，不限制）
    """
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True, sharey=True)
    pairs = [
        ("Clean Voice", clean, "tab:blue"),
        ("Hiss Noise", noise, "tab:orange"),
        ("Noisy Voice", noisy, "tab:red"),
        ("Filtered Voice", filtered, "tab:green"),
    ]
    for ax, (title, x, color) in zip(axes.flat, pairs):
        freqs, mag = magnitude_spectrum(x, fs)
        ax.plot(freqs, mag, color=color, linewidth=0.8)
        ax.set_title(title)
        ax.set_xlim(0, fs / 2)
        if ylimit is not None:
            ax.set_ylim(0, ylimit)  # 设置统一的 y 轴范围
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(alpha=0.25)
    fig.suptitle("FFT Magnitude Spectrum", fontsize=14)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "spectrum_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

def plot_spectrograms(clean: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
    """
    保存 spectrogram（声谱图）比较：清洁、含噪、滤波后（3 行）。

    参数:
        clean: 干净人声
        noisy: 含噪人声
        filtered: 处理后的人声
        fs: 采样率（Hz）
    """
    fig, axes = plt.subplots(3, 1, figsize=(13.5, 10), sharex=True)
    pairs = [
        ("Clean Voice", clean),
        ("Noisy Voice", noisy),
        ("Filtered Voice", filtered),
    ]
    img = None
    for ax, (title, x) in zip(axes, pairs):
        # 使用 SciPy 的 spectrogram 计算时频表示
        freqs, times, spec = signal.spectrogram(
            x,
            fs=fs,
            window="hann",
            nperseg=512,
            noverlap=384,
            scaling="spectrum",
            mode="magnitude",
        )
        # 将幅值转换为 dB 并避免 log(0)
        spec_db = 20 * np.log10(spec + 1e-8)
        img = ax.pcolormesh(times, freqs, spec_db, shading="gouraud", cmap="magma")
        ax.set_title(title)
        ax.set_ylabel("Frequency (Hz)")
        ax.set_ylim(0, fs / 2)
    axes[-1].set_xlabel("Time (s)")
    fig.subplots_adjust(right=0.88, hspace=0.28)
    # 添加颜色条，显示功率的 dB 值
    cax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    fig.colorbar(img, cax=cax, format="%+2.0f dB")
    fig.suptitle("Spectrogram Comparison", fontsize=14)
    fig.savefig(CHART_DIR / "spectrogram_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

def plot_demo_comparison(noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
    """
    绘制 demo 对比图，只展示前 DEMO_WINDOW_SEC 秒的 noisy 与 filtered。

    参数:
        noisy: 含噪人声
        filtered: 处理后人声
        fs: 采样率（Hz）
    """
    # 截取演示窗口长度，避免绘制太长的波形
    n = min(len(noisy), int(DEMO_WINDOW_SEC * fs))
    noisy = noisy[:n]
    filtered = filtered[:n]
    t = np.arange(n) / fs

    fig, axes = plt.subplots(2, 1, figsize=(13, 6), sharex=True)
    axes[0].plot(t, noisy, color="tab:red", linewidth=0.8)
    axes[0].set_title("Noisy Voice")
    axes[0].set_ylabel("Amp.")
    axes[0].grid(alpha=0.25)

    axes[1].plot(t, filtered, color="tab:green", linewidth=0.8)
    axes[1].set_title("Filtered Voice")
    axes[1].set_ylabel("Amp.")
    axes[1].set_xlabel("Time (s)")
    axes[1].grid(alpha=0.25)

    fig.suptitle("Demo Pair Comparison", fontsize=14)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "demo_pair_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

# ------------------------
# 主流程
# ------------------------
def main() -> None:
    """
    主流程：
    1. 创建输出目录
    2. 读取 clean / noise / noisy 三个音频文件
    3. 打印采样率信息（用于确认）
    4. 对候选截止频率进行比较并保存评估指标
    5. 用 SELECTED_CUTOFF 对 noisy 进行滤波并保存音频与图表
    6. 将评估结果写入 JSON 文件
    """
    # 确保图表输出目录存在
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    # 读取音频（均会被转换为单通道 float64）
    clean, fs = read_audio("clean_voice.mp3")
    noise, fs_noise = read_audio("hiss_noise.mp3")
    noisy, fs_noisy = read_audio("noisy_voice.mp3")

    # 打印采样率用于人工检查（脚本不会强制重采样）
    print("Using the following sampling rates:")
    print(f"Clean voice sampling rate: {fs}")
    print(f"Noise sampling rate: {fs_noise}")
    print(f"Noisy voice sampling rate: {fs_noisy}")
    print(f"Expected sampling rate: {FS_EXPECTED}")

    # 对各候选低通的表现进行量化比较（SNR、相关系数、高频能量抑制）
    metrics = compare_candidates(clean, noisy, fs)

    # 使用选定的截止频率对 noisy 做最终滤波
    selected = lowpass_filter(noisy, fs, EXPERIMENT_CUTOFFS[0], FILTER_ORDER)

    # 保存三个不同截止频率的处理结果
    filtered_audio = []
    for cutoff in EXPERIMENT_CUTOFFS:
        filtered_audio.append(lowpass_filter(noisy, fs, cutoff, FILTER_ORDER))

    # Save filtered audio files with descriptive names
    names = ["low", "medium", "high"]
    for i, cutoff in enumerate(EXPERIMENT_CUTOFFS):
        save_audio(f"filtered_voice_{names[i]}.mp3", filtered_audio[i], fs)

        # 计算统一的 ylimit
    max_magnitude = max(
        np.max(magnitude_spectrum(clean, fs)[1]),
        np.max(magnitude_spectrum(noise, fs)[1]),
        np.max(magnitude_spectrum(noisy, fs)[1]),
        np.max(magnitude_spectrum(selected, fs)[1]),
    )
    ylimit = max_magnitude * 1.1  # 留出 10% 的余量

    # 生成并保存各类图表（波形 / 频谱 / 声谱 / demo 对比）
    plot_waveforms(clean, noise, noisy, selected, fs)
    plot_spectra(clean, noise, noisy, selected, fs)
    plot_spectrograms(clean, noisy, selected, fs)
    plot_demo_comparison(noisy, selected, fs)

    # 将比较指标写入 JSON，便于后续记录与展示
    with open(AUDIO_DIR / "filter_metrics_round1.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "experiment_cutoffs_hz": EXPERIMENT_CUTOFFS,
                "filter_order": FILTER_ORDER,
                "candidates": metrics,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 控制台输出结果路径提示
    print("Experiment cutoff frequencies:", EXPERIMENT_CUTOFFS)
    print("Saved filtered audio files to:")
    for name in ["low", "medium", "high"]:
        print(f"- {AUDIO_DIR / f'filtered_voice_{name}.mp3'}")
    print("Saved metrics to:", AUDIO_DIR / "filter_metrics_round1.json")
    print("Saved charts to:", CHART_DIR)

if __name__ == "__main__":
    main()
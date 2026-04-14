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


BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "generated_audio"
CHART_DIR = BASE_DIR.parent / "Charts" / "analysis_round1"
FS_EXPECTED = 16_000
FILTER_ORDER = 4
CUTOFF_CANDIDATES = [2800, 3200, 3600]
SELECTED_CUTOFF = 3200
DEMO_WINDOW_SEC = 4.0


def read_audio(name: str) -> tuple[np.ndarray, int]:
    x, fs = sf.read(AUDIO_DIR / name)
    if x.ndim > 1:
        x = x.mean(axis=1)
    return x.astype(np.float64), fs


def normalize_peak(x: np.ndarray, peak: float = 0.92) -> np.ndarray:
    m = np.max(np.abs(x))
    if m == 0:
        return x.copy()
    return x * (peak / m)


def save_audio(name: str, x: np.ndarray, fs: int) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    sf.write(AUDIO_DIR / name, x, fs)


def lowpass_filter(x: np.ndarray, fs: int, cutoff: float, order: int = 4) -> np.ndarray:
    b, a = signal.butter(order, cutoff, btype="low", fs=fs)
    y = signal.filtfilt(b, a, x)
    return normalize_peak(y)


def snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    error = estimate - reference
    return 10.0 * np.log10(np.sum(reference**2) / np.sum(error**2))


def magnitude_spectrum(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray]:
    freqs = np.fft.rfftfreq(len(x), 1 / fs)
    mag = np.abs(np.fft.rfft(x))
    return freqs, mag


def compare_candidates(clean: np.ndarray, noisy: np.ndarray, fs: int) -> list[dict]:
    input_snr = snr_db(clean, noisy)
    records = []
    for cutoff in CUTOFF_CANDIDATES:
        filt = lowpass_filter(noisy, fs, cutoff, FILTER_ORDER)
        out_snr = snr_db(clean, filt)
        corr = float(np.corrcoef(clean, filt)[0, 1])
        hf_start = int(len(np.fft.rfft(noisy)) * 3500 / (fs / 2))
        noisy_fft = np.abs(np.fft.rfft(noisy))
        filt_fft = np.abs(np.fft.rfft(filt))
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


def plot_waveforms(clean: np.ndarray, noise: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
    t = np.arange(len(clean)) / fs
    fig, axes = plt.subplots(4, 1, figsize=(13, 9), sharex=True)
    pairs = [
        ("Clean Voice", clean, "tab:blue"),
        ("Hiss Noise", noise, "tab:orange"),
        ("Noisy Voice", noisy, "tab:red"),
        ("Filtered Voice", filtered, "tab:green"),
    ]
    for ax, (title, x, color) in zip(axes, pairs):
        ax.plot(t, x, color=color, linewidth=0.8)
        ax.set_title(title)
        ax.set_ylabel("Amp.")
        ax.grid(alpha=0.25)
    axes[-1].set_xlabel("Time (s)")
    fig.suptitle("Waveform Comparison", fontsize=14)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "waveforms_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_spectra(clean: np.ndarray, noise: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
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
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(alpha=0.25)
    fig.suptitle("FFT Magnitude Spectrum", fontsize=14)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "spectrum_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_spectrograms(clean: np.ndarray, noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(13.5, 10), sharex=True)
    pairs = [
        ("Clean Voice", clean),
        ("Noisy Voice", noisy),
        ("Filtered Voice", filtered),
    ]
    img = None
    for ax, (title, x) in zip(axes, pairs):
        freqs, times, spec = signal.spectrogram(
            x,
            fs=fs,
            window="hann",
            nperseg=512,
            noverlap=384,
            scaling="spectrum",
            mode="magnitude",
        )
        spec_db = 20 * np.log10(spec + 1e-8)
        img = ax.pcolormesh(times, freqs, spec_db, shading="gouraud", cmap="magma")
        ax.set_title(title)
        ax.set_ylabel("Frequency (Hz)")
        ax.set_ylim(0, fs / 2)
    axes[-1].set_xlabel("Time (s)")
    fig.subplots_adjust(right=0.88, hspace=0.28)
    cax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    fig.colorbar(img, cax=cax, format="%+2.0f dB")
    fig.suptitle("Spectrogram Comparison", fontsize=14)
    fig.savefig(CHART_DIR / "spectrogram_round1.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_demo_comparison(noisy: np.ndarray, filtered: np.ndarray, fs: int) -> None:
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


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    clean, fs = read_audio("clean_voice.wav")
    noise, fs_noise = read_audio("hiss_noise.wav")
    noisy, fs_noisy = read_audio("noisy_voice.wav")
    assert fs == fs_noise == fs_noisy == FS_EXPECTED

    metrics = compare_candidates(clean, noisy, fs)
    selected = lowpass_filter(noisy, fs, SELECTED_CUTOFF, FILTER_ORDER)
    filtered_3600 = lowpass_filter(noisy, fs, 3600, FILTER_ORDER)
    save_audio("filtered_voice.wav", selected, fs)
    save_audio("filtered_voice_3200.wav", selected, fs)
    save_audio("filtered_voice_3600.wav", filtered_3600, fs)

    plot_waveforms(clean, noise, noisy, selected, fs)
    plot_spectra(clean, noise, noisy, selected, fs)
    plot_spectrograms(clean, noisy, selected, fs)
    plot_demo_comparison(noisy, selected, fs)

    with open(AUDIO_DIR / "filter_metrics_round1.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "selected_cutoff_hz": SELECTED_CUTOFF,
                "filter_order": FILTER_ORDER,
                "candidates": metrics,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("Selected cutoff:", SELECTED_CUTOFF)
    print("Saved filtered audio to:", AUDIO_DIR / "filtered_voice.wav")
    print("Saved metrics to:", AUDIO_DIR / "filter_metrics_round1.json")
    print("Saved charts to:", CHART_DIR)


if __name__ == "__main__":
    main()

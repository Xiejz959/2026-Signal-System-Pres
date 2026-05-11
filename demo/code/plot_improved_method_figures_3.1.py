"""Plot figures for the Wiener-style frequency-mask improved method.

This plotting script reads the version 2.1 team audio from Codes/generated_audio.
It does not compute the low-pass baseline; it compares the existing 2.1
low-pass result with the improved-method audio produced by
improved_method_wiener_mask_3.1.py.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


ROOT = Path(__file__).resolve().parents[1]

import librosa

AUDIO_DIR = ROOT / "Codes" / "generated_audio"
VOICE_DIR = ROOT / "demo" / "Voices"
FIGURE_DIR = ROOT / "demo" / "Figures"
OUTPUT_DIR = ROOT / "Codes" / "improved_method_outputs"

N_PER_SEG = 1024
NO_OVERLAP = 768
DEMO_WINDOW_SEC = 4.0
FS_TARGET = 16_000


COLORS = {
    "clean": "#0071E3",
    "noisy": "#FF453A",
    "baseline": "#30D158",
    "mask": "#5AC8FA",
    "gold": "#FFD60A",
}


def read_mono(path: Path) -> tuple[np.ndarray, int]:
    x, fs = librosa.load(path, sr=FS_TARGET, mono=True)
    return x.astype(np.float64), fs


def align(*signals: np.ndarray) -> list[np.ndarray]:
    n = min(len(x) for x in signals)
    return [x[:n] for x in signals]


def spectrogram_db(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    freqs, times, spec = signal.spectrogram(
        x,
        fs=fs,
        window="hann",
        nperseg=N_PER_SEG,
        noverlap=NO_OVERLAP,
        scaling="spectrum",
        mode="magnitude",
    )
    return freqs, times, 20 * np.log10(spec + 1e-8)


def save_spectrogram(path: Path, x: np.ndarray, fs: int, title: str) -> None:
    freqs, times, spec_db = spectrogram_db(x, fs)
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    img = ax.pcolormesh(times, freqs, spec_db, shading="gouraud", cmap="magma")
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_ylim(0, fs / 2)
    fig.subplots_adjust(right=0.88)
    cax = fig.add_axes([0.90, 0.18, 0.025, 0.66])
    fig.colorbar(img, cax=cax, format="%+2.0f dB")
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_mask(path: Path, freqs: np.ndarray, times: np.ndarray, mask: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    img = ax.pcolormesh(times, freqs, mask, shading="gouraud", cmap="viridis", vmin=0.0, vmax=1.0)
    ax.set_title("Wiener-style Frequency Mask", fontsize=16)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_ylim(0, np.max(freqs))
    fig.subplots_adjust(right=0.88)
    cax = fig.add_axes([0.90, 0.18, 0.025, 0.66])
    fig.colorbar(img, cax=cax, label="Mask gain")
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_mask_pipeline(
    path: Path,
    noisy: np.ndarray,
    enhanced: np.ndarray,
    fs: int,
    freqs: np.ndarray,
    times: np.ndarray,
    mask: np.ndarray,
) -> None:
    noisy_f, noisy_t, noisy_db = spectrogram_db(noisy, fs)
    enhanced_f, enhanced_t, enhanced_db = spectrogram_db(enhanced, fs)

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.3), constrained_layout=False)

    im0 = axes[0].pcolormesh(noisy_t, noisy_f, noisy_db, shading="gouraud", cmap="magma")
    axes[0].set_title("Noisy Spectrogram")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Frequency (Hz)")
    axes[0].set_ylim(0, fs / 2)

    im1 = axes[1].pcolormesh(times, freqs, mask, shading="gouraud", cmap="viridis", vmin=0, vmax=1)
    axes[1].set_title("Wiener-style Mask")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Frequency (Hz)")
    axes[1].set_ylim(0, fs / 2)

    im2 = axes[2].pcolormesh(enhanced_t, enhanced_f, enhanced_db, shading="gouraud", cmap="magma")
    axes[2].set_title("Masked Result")
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Frequency (Hz)")
    axes[2].set_ylim(0, fs / 2)

    fig.suptitle("Noisy -> Mask -> Enhanced", fontsize=18)
    fig.subplots_adjust(right=0.92, wspace=0.24, top=0.82)
    cax_spec = fig.add_axes([0.935, 0.22, 0.012, 0.52])
    fig.colorbar(im2, cax=cax_spec, format="%+2.0f dB")
    cax_mask = fig.add_axes([0.962, 0.22, 0.012, 0.52])
    fig.colorbar(im1, cax=cax_mask)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_method_comparison(
    path: Path,
    noisy: np.ndarray,
    baseline: np.ndarray,
    improved: np.ndarray,
    fs: int,
) -> None:
    names = ["Noisy Voice", "Low-pass Baseline", "Wiener-style Mask Result"]
    signals = [noisy, baseline, improved]

    fig, axes = plt.subplots(3, 1, figsize=(13.5, 10), sharex=True)
    img = None
    for ax, name, x in zip(axes, names, signals):
        freqs, times, spec_db = spectrogram_db(x, fs)
        img = ax.pcolormesh(times, freqs, spec_db, shading="gouraud", cmap="magma")
        ax.set_title(name)
        ax.set_ylabel("Frequency (Hz)")
        ax.set_ylim(0, fs / 2)
    axes[-1].set_xlabel("Time (s)")
    fig.subplots_adjust(right=0.88, hspace=0.32)
    cax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    fig.colorbar(img, cax=cax, format="%+2.0f dB")
    fig.suptitle("Method Comparison", fontsize=16)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_demo_waveform_comparison(
    path: Path,
    clean: np.ndarray,
    noisy: np.ndarray,
    baseline: np.ndarray,
    improved: np.ndarray,
    fs: int,
) -> None:
    signals = [
        ("Clean Voice", clean, COLORS["clean"]),
        ("Noisy Voice", noisy, COLORS["noisy"]),
        ("Low-pass Baseline", baseline, COLORS["baseline"]),
        ("Wiener-style Mask Result", improved, COLORS["mask"]),
    ]
    n = min(int(DEMO_WINDOW_SEC * fs), *(len(x) for _, x, _ in signals))
    t = np.arange(n) / fs

    fig, axes = plt.subplots(4, 1, figsize=(13.5, 9), sharex=True)
    for ax, (name, x, color) in zip(axes, signals):
        ax.plot(t, x[:n], color=color, linewidth=0.8)
        ax.set_title(name)
        ax.set_ylabel("Amp.")
        ax.grid(alpha=0.25)
    axes[-1].set_xlabel("Time (s)")
    fig.suptitle("Demo Window Waveform Comparison", fontsize=16)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    error = estimate - reference
    return float(10.0 * np.log10(np.sum(reference**2) / (np.sum(error**2) + 1e-12)))


def high_frequency_ratio(reference_input: np.ndarray, estimate: np.ndarray, fs: int, start_hz: float = 3500.0) -> float:
    input_fft = np.abs(np.fft.rfft(reference_input))
    estimate_fft = np.abs(np.fft.rfft(estimate))
    freqs = np.fft.rfftfreq(len(reference_input), 1 / fs)
    idx = freqs >= start_hz
    return float(np.mean(estimate_fft[idx]) / (np.mean(input_fft[idx]) + 1e-12))


def main() -> None:
    clean, fs_clean = read_mono(AUDIO_DIR / "clean_voice_2.1.mp3")
    noisy, fs_noisy = read_mono(AUDIO_DIR / "noisy_voice_2.1.mp3")
    baseline, fs_baseline = read_mono(AUDIO_DIR / "filtered_voice_low_2.1.mp3")
    improved, fs_improved = read_mono(VOICE_DIR / "wiener_masked_voice_3.1.wav")
    if len({fs_clean, fs_noisy, fs_baseline, fs_improved}) != 1:
        raise ValueError("All comparison audio files must use the same sampling rate.")

    clean, noisy, baseline, improved = align(clean, noisy, baseline, improved)
    mask_data = np.load(OUTPUT_DIR / "wiener_mask_data_3.1.npz")
    freqs = mask_data["freqs"]
    times = mask_data["times"]
    mask = mask_data["mask"]

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    save_spectrogram(FIGURE_DIR / "noisy_spectrogram_3.1.png", noisy, fs_clean, "Noisy Voice Spectrogram")
    save_mask(FIGURE_DIR / "wiener_mask_3.1.png", freqs, times, mask)
    save_spectrogram(FIGURE_DIR / "wiener_masked_spectrogram_3.1.png", improved, fs_clean, "Wiener-style Mask Result Spectrogram")
    save_mask_pipeline(FIGURE_DIR / "mask_pipeline_3.1.png", noisy, improved, fs_clean, freqs, times, mask)
    save_method_comparison(FIGURE_DIR / "method_comparison_3.1.png", noisy, baseline, improved, fs_clean)
    save_demo_waveform_comparison(FIGURE_DIR / "demo_waveform_comparison_3.1.png", clean, noisy, baseline, improved, fs_clean)

    metrics = {
        "methods": {
            "noisy_input": {
                "snr_vs_clean_db": round(snr_db(clean, noisy), 3),
                "high_freq_ratio_vs_noisy": 1.0,
            },
            "lowpass_baseline": {
                "snr_vs_clean_db": round(snr_db(clean, baseline), 3),
                "snr_improvement_db": round(snr_db(clean, baseline) - snr_db(clean, noisy), 3),
                "high_freq_ratio_vs_noisy": round(high_frequency_ratio(noisy, baseline, fs_clean), 4),
            },
            "wiener_style_mask": {
                "snr_vs_clean_db": round(snr_db(clean, improved), 3),
                "snr_improvement_db": round(snr_db(clean, improved) - snr_db(clean, noisy), 3),
                "high_freq_ratio_vs_noisy": round(high_frequency_ratio(noisy, improved, fs_clean), 4),
            },
        },
        "figures": {
            "noisy_spectrogram": str(FIGURE_DIR / "noisy_spectrogram_3.1.png"),
            "wiener_mask": str(FIGURE_DIR / "wiener_mask_3.1.png"),
            "wiener_masked_spectrogram": str(FIGURE_DIR / "wiener_masked_spectrogram_3.1.png"),
            "mask_pipeline": str(FIGURE_DIR / "mask_pipeline_3.1.png"),
            "method_comparison": str(FIGURE_DIR / "method_comparison_3.1.png"),
            "demo_waveform_comparison": str(FIGURE_DIR / "demo_waveform_comparison_3.1.png"),
        },
    }
    with open(OUTPUT_DIR / "lowpass_vs_mask_metrics_3.1.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("Saved improved-method figures to:", FIGURE_DIR)
    print("Saved comparison metrics to:", OUTPUT_DIR / "lowpass_vs_mask_metrics_3.1.json")


if __name__ == "__main__":
    main()

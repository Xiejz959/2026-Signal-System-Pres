"""Create the improved-method audio using a Wiener-style frequency mask.

This script intentionally does not regenerate clean/noise/noisy audio and does
not recompute the low-pass baseline. It reads the version 2.1 audio prepared by
the team in Codes/generated_audio and writes only the improved-method output
plus mask data.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")

import numpy as np
import soundfile as sf
from scipy import signal


ROOT = Path(__file__).resolve().parents[1]

import librosa

AUDIO_DIR = ROOT / "Codes" / "generated_audio"
VOICE_DIR = ROOT / "demo" / "Voices"
OUTPUT_DIR = ROOT / "Codes" / "improved_method_outputs"

FS_EXPECTED = 16_000
N_PER_SEG = 1024
NO_OVERLAP = 768
MASK_FLOOR = 0.12
MASK_CEILING = 1.0
NOISE_OVER_ESTIMATE = 0.4
MASK_SMOOTHING_BINS = 1


def read_mono_audio(path: Path) -> tuple[np.ndarray, int]:
    x, fs = librosa.load(path, sr=FS_EXPECTED, mono=True)
    return x.astype(np.float64), fs


def align_signals(*signals: np.ndarray) -> list[np.ndarray]:
    n = min(len(x) for x in signals)
    return [x[:n] for x in signals]


def peak_normalize(x: np.ndarray, peak: float = 0.92) -> np.ndarray:
    max_abs = np.max(np.abs(x))
    if max_abs == 0:
        return x.copy()
    return x * (peak / max_abs)


def rms_match(reference: np.ndarray, estimate: np.ndarray) -> np.ndarray:
    ref_rms = np.sqrt(np.mean(reference**2) + 1e-12)
    est_rms = np.sqrt(np.mean(estimate**2) + 1e-12)
    return estimate * (ref_rms / est_rms)


def moving_average_frequency(mask: np.ndarray, bins: int) -> np.ndarray:
    if bins <= 1:
        return mask
    kernel = np.ones(bins) / bins
    smoothed = np.empty_like(mask)
    for frame in range(mask.shape[1]):
        smoothed[:, frame] = np.convolve(mask[:, frame], kernel, mode="same")
    return smoothed


def compute_wiener_style_mask(noisy: np.ndarray, noise: np.ndarray, fs: int) -> dict[str, np.ndarray]:
    freqs, times, noisy_stft = signal.stft(
        noisy,
        fs=fs,
        window="hann",
        nperseg=N_PER_SEG,
        noverlap=NO_OVERLAP,
        boundary="zeros",
        padded=True,
    )
    _, _, noise_stft = signal.stft(
        noise,
        fs=fs,
        window="hann",
        nperseg=N_PER_SEG,
        noverlap=NO_OVERLAP,
        boundary="zeros",
        padded=True,
    )

    noisy_power = np.abs(noisy_stft) ** 2
    noise_power = np.mean(np.abs(noise_stft) ** 2, axis=1, keepdims=True)
    estimated_speech_power = np.maximum(noisy_power - NOISE_OVER_ESTIMATE * noise_power, 0.0)

    mask = estimated_speech_power / (estimated_speech_power + noise_power + 1e-12)
    mask = moving_average_frequency(mask, MASK_SMOOTHING_BINS)
    mask = np.clip(mask, MASK_FLOOR, MASK_CEILING)

    enhanced_stft = mask * noisy_stft
    _, enhanced = signal.istft(
        enhanced_stft,
        fs=fs,
        window="hann",
        nperseg=N_PER_SEG,
        noverlap=NO_OVERLAP,
        input_onesided=True,
        boundary=True,
    )
    enhanced = enhanced[: len(noisy)]
    enhanced = rms_match(noisy, enhanced)
    enhanced = peak_normalize(enhanced)

    return {
        "freqs": freqs,
        "times": times,
        "mask": mask,
        "noisy_power": noisy_power,
        "noise_power": noise_power,
        "enhanced": enhanced,
    }


def snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    error = estimate - reference
    return float(10.0 * np.log10(np.sum(reference**2) / (np.sum(error**2) + 1e-12)))


def main() -> None:
    clean, fs_clean = read_mono_audio(AUDIO_DIR / "clean_voice_2.1.mp3")
    noise, fs_noise = read_mono_audio(AUDIO_DIR / "hiss_noise_2.1.mp3")
    noisy, fs_noisy = read_mono_audio(AUDIO_DIR / "noisy_voice_2.1.mp3")

    if len({fs_clean, fs_noise, fs_noisy}) != 1:
        raise ValueError("Input demo audio files must use the same sampling rate.")
    if fs_clean != FS_EXPECTED:
        print(f"Warning: expected {FS_EXPECTED} Hz, got {fs_clean} Hz. Continuing with input rate.")

    clean, noise, noisy = align_signals(clean, noise, noisy)
    result = compute_wiener_style_mask(noisy, noise, fs_clean)
    enhanced = result["enhanced"]
    clean, noisy, enhanced = align_signals(clean, noisy, enhanced)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sf.write(VOICE_DIR / "wiener_masked_voice_3.1.wav", enhanced, fs_clean)
    np.savez_compressed(
        OUTPUT_DIR / "wiener_mask_data_3.1.npz",
        freqs=result["freqs"],
        times=result["times"],
        mask=result["mask"],
        noisy_power=result["noisy_power"],
        noise_power=result["noise_power"],
        enhanced=enhanced,
        fs=np.array([fs_clean]),
    )

    metrics = {
        "method": "Wiener-style frequency-domain mask",
        "input_files": {
            "clean": str(AUDIO_DIR / "clean_voice_2.1.mp3"),
            "noise": str(AUDIO_DIR / "hiss_noise_2.1.mp3"),
            "noisy": str(AUDIO_DIR / "noisy_voice_2.1.mp3"),
        },
        "output_file": str(VOICE_DIR / "wiener_masked_voice_3.1.wav"),
        "sampling_rate_hz": fs_clean,
        "duration_sec": round(len(enhanced) / fs_clean, 3),
        "stft": {
            "nperseg": N_PER_SEG,
            "noverlap": NO_OVERLAP,
        },
        "mask": {
            "floor": MASK_FLOOR,
            "noise_over_estimate": NOISE_OVER_ESTIMATE,
            "frequency_smoothing_bins": MASK_SMOOTHING_BINS,
            "mean": round(float(np.mean(result["mask"])), 4),
            "min": round(float(np.min(result["mask"])), 4),
            "max": round(float(np.max(result["mask"])), 4),
        },
        "snr": {
            "noisy_vs_clean_db": round(snr_db(clean, noisy), 3),
            "wiener_mask_vs_clean_db": round(snr_db(clean, enhanced), 3),
            "improvement_db": round(snr_db(clean, enhanced) - snr_db(clean, noisy), 3),
        },
    }
    with open(OUTPUT_DIR / "wiener_mask_metrics_3.1.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print("Saved improved audio:", VOICE_DIR / "wiener_masked_voice_3.1.wav")
    print("Saved mask data:", OUTPUT_DIR / "wiener_mask_data_3.1.npz")
    print("Saved metrics:", OUTPUT_DIR / "wiener_mask_metrics_3.1.json")


if __name__ == "__main__":
    main()

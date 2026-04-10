"""Generate playable clean/noise/noisy audio for the ECE0402 demo.

This script avoids third-party dependencies on purpose.
It synthesizes:
1. a speech-like clean signal
2. a high-frequency hiss noise signal
3. a noisy voice signal created by mixing the two
"""

from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path


FS = 16_000
OUTPUT_DIR = Path(__file__).resolve().parent / "generated_audio"


def envelope(i: int, n: int, attack: float = 0.08, release: float = 0.12) -> float:
    if n <= 1:
        return 1.0
    x = i / (n - 1)
    if x < attack:
        return x / attack
    if x > 1.0 - release:
        return max(0.0, (1.0 - x) / release)
    return 1.0


def synth_vowel(duration: float, f0_start: float, f0_end: float, formants: list[tuple[float, float]], amp: float = 0.55) -> list[float]:
    n = max(1, int(duration * FS))
    out: list[float] = []
    phase = 0.0
    for i in range(n):
        frac = i / max(1, n - 1)
        f0 = f0_start + (f0_end - f0_start) * frac
        phase += 2.0 * math.pi * f0 / FS
        sample = 0.0
        max_harm = max(1, int((FS / 2) // max(f0, 1.0)))
        max_harm = min(max_harm, 28)
        for k in range(1, max_harm + 1):
            freq = k * f0
            weight = 0.0
            for center, bw in formants:
                weight += math.exp(-((freq - center) / bw) ** 2)
            weight /= k ** 1.15
            sample += weight * math.sin(k * phase)
        sample *= envelope(i, n)
        out.append(amp * sample)
    return out


def silence(duration: float) -> list[float]:
    return [0.0] * int(duration * FS)


def normalize(samples: list[float], peak: float = 0.9) -> list[float]:
    mx = max(abs(x) for x in samples) if samples else 1.0
    if mx == 0:
        return samples[:]
    scale = peak / mx
    return [x * scale for x in samples]


def synth_clean_voice() -> list[float]:
    # A short "announcement-like" sequence of voiced syllables.
    segments = [
        (0.42, 135, 145, [(730, 90), (1090, 120), (2440, 180)]),   # /a/
        (0.06, 0, 0, []),
        (0.34, 142, 155, [(530, 80), (1840, 130), (2480, 170)]),   # /e/
        (0.05, 0, 0, []),
        (0.30, 148, 160, [(270, 70), (2290, 130), (3010, 200)]),   # /i/
        (0.07, 0, 0, []),
        (0.42, 140, 132, [(570, 90), (840, 100), (2410, 190)]),    # /o/
        (0.06, 0, 0, []),
        (0.40, 130, 126, [(300, 70), (870, 100), (2240, 170)]),    # /u/
        (0.08, 0, 0, []),
        (0.48, 138, 150, [(730, 90), (1090, 120), (2440, 180)]),   # /a/
    ]
    out: list[float] = []
    for duration, f0a, f0b, formants in segments:
        if not formants:
            out.extend(silence(duration))
        else:
            out.extend(synth_vowel(duration, f0a, f0b, formants))
    return normalize(out, peak=0.82)


def synth_hiss_noise(length: int) -> list[float]:
    rng = random.Random(4026)
    white = [rng.gauss(0.0, 1.0) for _ in range(length)]

    # Simple high-pass shaping by differencing plus a small amount of original noise.
    hp: list[float] = []
    prev = 0.0
    for x in white:
        shaped = (x - 0.985 * prev) + 0.18 * x
        hp.append(shaped)
        prev = x

    # Apply a very light slow envelope so the noise sounds more realistic.
    out: list[float] = []
    for i, x in enumerate(hp):
        t = i / FS
        env = 0.88 + 0.12 * math.sin(2.0 * math.pi * 0.35 * t + 0.6)
        out.append(x * env)
    return normalize(out, peak=0.50)


def mix(clean: list[float], noise: list[float], noise_gain: float = 0.42) -> list[float]:
    n = min(len(clean), len(noise))
    mixed = [clean[i] + noise_gain * noise[i] for i in range(n)]
    return normalize(mixed, peak=0.92)


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = bytearray()
    for s in samples:
        s = max(-1.0, min(1.0, s))
        pcm.extend(struct.pack("<h", int(s * 32767)))
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(FS)
        wf.writeframes(bytes(pcm))


def main() -> None:
    clean = synth_clean_voice()
    noise = synth_hiss_noise(len(clean))
    noisy = mix(clean, noise, noise_gain=0.48)

    write_wav(OUTPUT_DIR / "clean_voice.wav", clean)
    write_wav(OUTPUT_DIR / "hiss_noise.wav", noise)
    write_wav(OUTPUT_DIR / "noisy_voice.wav", noisy)

    print("Generated:")
    print(OUTPUT_DIR / "clean_voice.wav")
    print(OUTPUT_DIR / "hiss_noise.wav")
    print(OUTPUT_DIR / "noisy_voice.wav")


if __name__ == "__main__":
    main()

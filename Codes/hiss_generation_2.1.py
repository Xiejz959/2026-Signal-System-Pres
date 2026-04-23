"""Generate a high-frequency hiss noise and save it as an MP3 file.

This script generates a synthetic noise signal with a relatively fixed frequency spectrum,
which can be used for testing noise filtering algorithms.
"""

from pathlib import Path
import numpy as np
import soundfile as sf
import librosa

# Parameters for noise generation
FS = 16000  # Sampling rate
DURATION = 30.0  # Duration in seconds
OUTPUT_FILE = Path("D:/Courses/2026Spring/SigNSys/Codes/generated_audio/hiss_noise.mp3")


def generate_hiss_noise(fs: int, duration: float) -> np.ndarray:
    """Generate a high-frequency hiss noise signal."""
    rng = np.random.default_rng(seed=42)
    n_samples = int(fs * duration)
    white_noise = rng.normal(0, 1, n_samples)

    # High-pass filter to emphasize high frequencies
    b = [1, -0.95]  # Simple high-pass filter coefficients
    a = [1]
    hiss_noise = np.convolve(white_noise, b, mode="same")

    # Normalize the noise to a peak amplitude of 0.2
    max_amp = np.max(np.abs(hiss_noise))
    if max_amp > 0:
        hiss_noise = 0.2 * hiss_noise / max_amp

    return hiss_noise


def save_hiss_noise(file_path: Path, noise: np.ndarray, fs: int) -> None:
    """Save the generated noise to an MP3 file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(file_path, noise, fs)


def analyze_dominant_frequencies(noise: np.ndarray, fs: int, n_peaks: int = 5) -> None:
    """Analyze and print the dominant frequencies in the noise signal."""
    # Compute the magnitude spectrum
    freqs = np.fft.rfftfreq(len(noise), 1 / fs)
    magnitude = np.abs(np.fft.rfft(noise))

    # Find the indices of the top n_peaks frequencies
    dominant_indices = np.argsort(magnitude)[-n_peaks:][::-1]
    dominant_freqs = freqs[dominant_indices]
    dominant_mags = magnitude[dominant_indices]

    print("Dominant Frequencies (Hz) and Magnitudes:")
    for freq, mag in zip(dominant_freqs, dominant_mags):
        print(f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}")


def main() -> None:
    """Main function to read, process, and overwrite hiss noise."""
    # Generate new hiss noise
    hiss_noise = generate_hiss_noise(FS, DURATION)

    # Analyze dominant frequencies
    analyze_dominant_frequencies(hiss_noise, FS)

    # Save the generated noise
    save_hiss_noise(OUTPUT_FILE, hiss_noise, FS)

    print("Hiss noise file has been generated.")


if __name__ == "__main__":
    main()
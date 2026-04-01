#!/usr/bin/env python3
"""Extract perceptually salient Librosa feature vectors for WAV files.

Outputs one JSON file per WAV in Alberto/ as:
[57 numeric feature values..., "<sound filename>.wav"]
"""

from __future__ import annotations

import json
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

SAMPLE_RATE = 22050
DURATION_SECONDS = 2.0
N_MFCC = 20
SINE_FREQUENCY_HZ = 440.0


def create_reference_wavs(target_dir: Path) -> None:
    """Create 2-second 440 Hz sine and white-noise reference files."""
    samples = int(SAMPLE_RATE * DURATION_SECONDS)
    time_axis = np.linspace(0.0, DURATION_SECONDS, samples, endpoint=False)

    sine_wave = 0.5 * np.sin(2.0 * np.pi * SINE_FREQUENCY_HZ * time_axis)
    white_noise = 0.2 * np.random.default_rng(42).standard_normal(samples)

    sf.write(target_dir / "reference-sine-220hz.wav", sine_wave, SAMPLE_RATE)
    sf.write(target_dir / "reference-white-noise.wav", white_noise, SAMPLE_RATE)


def extract_vector(file_path: Path) -> list[float]:
    """Build a stable 57-value descriptor vector from salient audio features."""
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)

    vector: list[float] = []

    vector.extend(np.mean(mfcc, axis=1).tolist())  # 20
    vector.extend(np.std(mfcc, axis=1).tolist())  # 20 -> 40

    vector.extend(np.mean(spectral_contrast, axis=1).tolist())  # 7 -> 47
    vector.extend(np.std(spectral_contrast, axis=1).tolist())  # 7 -> 54

    vector.append(float(np.mean(rms)))  # -> 55
    vector.append(float(np.std(rms)))  # -> 56
    vector.append(float(np.mean(zcr)))  # -> 57

    if len(vector) != 57:
        raise ValueError(f"Expected 57 features, got {len(vector)} for {file_path.name}")

    return [float(value) for value in vector]


def write_vectors(alberto_dir: Path) -> None:
    all_wav_files = sorted(alberto_dir.glob("*.wav"))
    if not all_wav_files:
        raise FileNotFoundError("No WAV files found in Alberto directory")

    all_vectors = [extract_vector(wav_file) for wav_file in all_wav_files]

    for wav_file, vector in zip(all_wav_files, all_vectors, strict=True):
        output_payload = [float(value) for value in vector] + [wav_file.name]
        output_path = alberto_dir / f"{wav_file.stem}-vector.json"
        output_path.write_text(json.dumps(output_payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output_path.name} ({len(vector)} values + filename)")


def main() -> None:
    project_root = Path(__file__).resolve().parent
    alberto_dir = project_root / "Alberto"

    if not alberto_dir.exists():
        raise FileNotFoundError(f"Missing directory: {alberto_dir}")

    create_reference_wavs(alberto_dir)
    write_vectors(alberto_dir)


if __name__ == "__main__":
    main()

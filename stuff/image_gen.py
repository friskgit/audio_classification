#!/usr/bin python3

import torch
import numpy as np
import torchaudio
import matplotlib.pyplot as plt
from PIL import Image

SPECTROGRAM_DPI = 90 # image quality of spectrograms
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_HOPE_LENGHT = 1024

class audio():
    def __init__(self, filepath_, hop_lenght = DEFAULT_HOPE_LENGHT, samples_rate = DEFAULT_SAMPLE_RATE):
        self.hop_lenght = hop_lenght
        self.samples_rate = samples_rate
        self.waveform, self.sample_rate = torchaudio.load(filepath_)

    def plot_spectrogram(self) -> None:
        waveform = self.waveform.numpy()
        _, axes = plt.subplots(1, 1)
        axes.specgram(waveform[0], Fs=self.sample_rate)
        plt.axis('off')
        plt.show(block=False)
    
    def write_disk_spectrogram(self, path, dpi=SPECTROGRAM_DPI) -> None:
        self.plot_spectrogram()
        plt.savefig(path, dpi=dpi, bbox_inches='tight')

input_path = "../segmentation/audio/segment_1.wav"
output_path = "../segmentation/audio/segment_1.png"
sound = audio(input_path)
sound.write_disk_spectrogram(output_path, dpi=SPECTROGRAM_DPI)

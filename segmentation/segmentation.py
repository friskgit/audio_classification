from maad import sound
from maad.rois import find_rois_cwt
from maad.util import plot_spectrogram
import matplotlib.pyplot as plt
import soundfile as sf
import sys
import argparse
import os
from pathlib import Path

"""
Use to segment an audio file using maad library find_rois_cwt() function. It loks for regions of interest in the audio file (first argument) changes in the audio file using a three step process:


1. Filter the signal with a bandpass sinc filter
2. Smoothing the signal by convolving it with a Mexican hat wavelet (Ricker wavelet) [1]
3. Binarize the signal applying a linear threshold

Arguments:

The audio file
--minfrq int 500
--maxfrq int 10000
--display bool false
--time int 3
--threshold int 0
"""
parser = argparse.ArgumentParser()
parser.add_argument("audiofile")
parser.add_argument("--minfrq", nargs='?', type=int, default=500)
parser.add_argument("--maxfrq", nargs='?', type=int, default=10000)
parser.add_argument("--display", nargs='?', type=bool, default=False)
parser.add_argument("--time", nargs='?', type=int, default=3)
parser.add_argument("--threshold", nargs='?', type=float, default=0)
args=parser.parse_args()
segments = []
audio_name = Path(args.audiofile).stem
dir_name = os.path.dirname(args.audiofile)

s, fs = sound.load(args.audiofile)
Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=512)
regions = find_rois_cwt(s, fs, flims=(args.minfrq, args.maxfrq), tlen=args.time, th=args.threshold, display=args.display, figsize=(10,6))
plt.show()

print(regions.head())
print(dir_name + '/' + audio_name + '_segment_{}.wav'.format(1))
for i, row in regions.iterrows():
    start = int(row['min_t'] * fs)
    end = int(row['max_t'] * fs)
    segment = s[start:end]
    sf.write(dir_name + '/' + audio_name + '_segment_{}.wav'.format(i), segment, fs)


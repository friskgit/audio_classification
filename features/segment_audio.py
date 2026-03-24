from maad import sound
from maad.rois import find_rois_cwt
from maad.util import plot_spectrogram
import matplotlib.pyplot as plt
import soundfile as sf
import os
from pathlib import Path

def segmentAudio(path):
# audio_dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/segmentation/audio'
# audio = 'dataton2.wav'
  audio_name = Path(audio).stem
  segment_dir = os.path.join(audio_dir, audio_name + '_segments')
  segment_exists = os.path.isdir(segment_dir)
  segments = []
  if not segment_exists:
    os.mkdir(segment_dir)
    
    s, fs = sound.load(os.path.join(audio_dir, audio))
    Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=512)
    # uncomment if you want to plot 
    # plot_spectrogram(Sxx, extent=ext, db_range=60, gain=20, colorbar=False, figsize=(2.5,10))
    # plt.show()
    # print(df_trill)

    regions = find_rois_cwt(s, fs, flims=(80,10000), tlen=4, th=0.05, display=False, figsize=(10,6))
    # print segments
    # print(regions.head())

    for i, row in regions.iterrows():
      start = int(row['min_t'] * fs)
      end = int(row['max_t'] * fs)
      segment = s[start:end]
      segments.append = os.path.join(segment_dir, Path(audio).stem + '_segment_{}.wav'.format(i))
      sf.write(segments[i], segment, fs)

  return segments

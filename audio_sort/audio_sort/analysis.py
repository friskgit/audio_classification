import os
import pandas as pd
pd.set_option("display.max_rows", None)     # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
from multiprocessing import Pool
import warnings
import numpy as np
from scipy import stats
import librosa
from tqdm import tqdm
import utils
import json
import math
import sys

class Analysis:
  """A class that computes the featurees of a SoundFile instance"""
  feature_sizes = dict(chroma_stft=12, chroma_cqt=12, # chroma_cens=12,
                       tonnetz=6, mfcc=20, rms=1, zcr=1,
                       spectral_centroid=1, spectral_bandwidth=1,
                       spectral_contrast=7, spectral_rolloff=1, tempogram=13) #, position=1, clarity=1)
  moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

  def __init__(self):
    print('Loaded')

  def columns(self):
    columns = []
    for name, size in self.feature_sizes.items():
      for moment in self.moments:
        it = ((name, moment, (i+1)) for i in range(size))
        columns.extend(it)

    names = ('feature', 'statistics', 'number')
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # More efficient to slice if indexes are sorted.
    return columns.sort_values()

  def compute_features(self, tid, audio, sr):

    features = pd.Series(index=self.columns(), dtype='float64', name=tid)

    # Catch warnings as exceptions (audioread leaks file descriptors).
    warnings.filterwarnings('error', module='librosa')

    def feature_stats(name, values):
      features[name, 'mean'] = np.mean(values, axis=1)
      features[name, 'std'] = np.std(values, axis=1)
      features[name, 'skew'] = stats.skew(values, axis=1)
      features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
      features[name, 'median'] = np.median(values, axis=1)
      features[name, 'min'] = np.min(values, axis=1)
      features[name, 'max'] = np.max(values, axis=1)

    try:
  #    filepath = os.path.join(path, tid)

  #    print(tid)

  #    x, sr = librosa.load(filepath, sr=None, mono=True)  # kaiser_fast
  #    x_stereo, sr = librosa.load(tid, sr=None, mono=False)  # kaiser_fast

      x = librosa.util.normalize(audio, norm=np.inf, axis=0, threshold=None, fill=None)
  #    pos, clar = extract_stereo(x_stereo, sr, n_mels=16)
  #    feature_stats('position', pos)
  #    feature_stats('clarity', clar)

      tempogram = librosa.feature.tempogram(y=x, sr=sr)
      f = librosa.feature.tempogram_ratio(tg=tempogram, sr=sr)
      feature_stats('tempogram', f)

      f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
      feature_stats('zcr', f)

      cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=256, bins_per_octave=12, n_bins=7*12, tuning=None))
      assert cqt.shape[0] == 7 * 12
      assert np.ceil(len(x)/256) <= cqt.shape[1] <= np.ceil(len(x)/256)+1

      f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
      feature_stats('chroma_cqt', f)
  #    f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
  #    feature_stats('chroma_cens', f)
      f = librosa.feature.tonnetz(chroma=f)
      feature_stats('tonnetz', f)

      del cqt
      stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
      assert stft.shape[0] == 1 + 2048 // 2
      assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
      del x

      f = librosa.feature.chroma_stft(S=stft**2, n_chroma=12)
      feature_stats('chroma_stft', f)

      f = librosa.feature.rms(S=stft)
      feature_stats('rms', f)

      f = librosa.feature.spectral_centroid(S=stft)
      feature_stats('spectral_centroid', f)
      f = librosa.feature.spectral_bandwidth(S=stft)
      feature_stats('spectral_bandwidth', f)
      f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
      feature_stats('spectral_contrast', f)
      f = librosa.feature.spectral_rolloff(S=stft)
      feature_stats('spectral_rolloff', f)

      mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
      del stft
      f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
      feature_stats('mfcc', f)

    except Exception as e:
  #    print("exception")
      print('{}: {}'.format(tid, repr(e)))
      features.fillna(0, axis=0, inplace=True)  

    return features

  def extract(self, audio, sr, n_fft=2048, n_mels=32):
    spect = librosa.stft(audio, n_fft=n_fft)
    mel_L, mel_R = (
      librosa.feature.melspectrogram(S=spect[0,:], n_mels=n_mels, sr=sr),
      librosa.feature.melspectrogram(S=spect[1,:], n_mels=n_mels, sr=sr)
    )
    return position_and_clarity(np.stack([mel_L, mel_R]))


  def position_and_clarity(self, spect):
    mid = spect[1,:] + spect[0,:]
    side = spect[1,:] - spect[0,:]
    mag_mid = np.abs(mid)
    mag_side = np.abs(side)
    delta_phi_ms = np.angle(mid) - np.angle(side)
    sigma = 0.5 * np.arctan((2 * mag_side * mag_mid * np.cos(delta_phi_ms))/(mag_mid**2 - mag_side**2))
    C = 0.5 * (np.cos(2 * delta_phi_ms) + 1)
    return sigma, C

  def call_for_file(self, audiof):
    """Function to generate a json with features"""
    # compute single file
    # audiof = 'Berta_Trupia-003.wav'
    jsonf, ext = os.path.splitext(audiof)
    jsonf = jsonf + '-feat.json'
    ser = compute_features(audiof)
    if ser != 0:
      json_file = ser.to_dict()

    full_path = os.path.abspath(audiof)

    # Add filename header
    json_file = { str(k): v for k,v in json_file.items() }
    json_file = {audiof: json_file}
  #  json_file['segment'] = 
  #  json_file = {'file_name': 'Yo', json_file}

    # Write to file
    with open(os.path.join(path, jsonf), 'w', encoding='utf-8') as f:
      f.write(json.dumps(json_file))

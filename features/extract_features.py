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
from stereo_features import extract as extract_stereo

path = '/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/Alberto'

feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                       tonnetz=6, mfcc=20, rms=1, zcr=1,
                       spectral_centroid=1, spectral_bandwidth=1,
                       spectral_contrast=7, spectral_rolloff=1, tempogram=13,
                       position=16, clarity=16)
moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

def columns():
  columns = []
  for name, size in feature_sizes.items():
    for moment in moments:
      it = ((name, moment, (i+1)) for i in range(size))
      columns.extend(it)
      
  names = ('feature', 'statistics', 'number')
  columns = pd.MultiIndex.from_tuples(columns, names=names)
      
  # More efficient to slice if indexes are sorted.
  return columns.sort_values()

def compute_features(tid):

  features = pd.Series(index=columns(), dtype='float64', name=tid)
  
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
    filepath = os.path.join(path, tid)
      
    # print(filepath)
    
    x, sr = librosa.load(filepath, sr=None)  # kaiser_fast

    tempogram = librosa.feature.tempogram(y=x, sr=sr)
    f = librosa.feature.tempogram_ratio(tg=tempogram, sr=sr)
    feature_stats('tempogram', f)
    
    f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
    feature_stats('zcr', f)
    
    cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12, n_bins=7*12, tuning=None))
    assert cqt.shape[0] == 7 * 12
    assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512)+1
      
    f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
    feature_stats('chroma_cqt', f)
    f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
    feature_stats('chroma_cens', f)
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
    print('{}: {}'.format(tid, repr(e)))
    
  return features

def call_for_file(audiof):
  """Function to generate a json with features"""
  # compute single file
  # audiof = 'Berta_Trupia-003.wav'
  jsonf, ext = os.path.splitext(audiof)
  jsonf = jsonf + '-feat.json'
  ser = compute_features(audiof)
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

def call_for_files(directory, selector='.wav'):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  for f in files:
    if f.endswith(selector):
#      paths.append(os.path.join(directory, f))
      print(os.path.join(directory, f))
      call_for_file(os.path.join(directory, f))

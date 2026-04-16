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
# from stereo_features import extract as extract_stereo

path = '/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/Alberto'

feature_sizes = dict(chroma_stft=12, chroma_cqt=12, # chroma_cens=12,
                       tonnetz=6, mfcc=20, rms=1, zcr=1,
                       spectral_centroid=1, spectral_bandwidth=1,
                       spectral_contrast=7, spectral_rolloff=1, tempogram=13)
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

def call_for_file(audiof):
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

def call_for_files(directory, selector='.wav'):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  for f in files:
    if f.endswith(selector):
#      paths.append(os.path.join(directory, f))
      print(os.path.join(directory, f))
      call_for_file(os.path.join(directory, f))

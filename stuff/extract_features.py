import os
import pandas as pd
from multiprocessing import Pool
import warnings
import numpy as np
from scipy import stats
import librosa
from tqdm import tqdm
import utils

def columns():
    feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                         tonnetz=6, mfcc=20, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')
    
    columns = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
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
            filepath = os.path.join('/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/Claudio', tid)
            
            print(filepath)
            x, sr = librosa.load(filepath, sr=None)  # kaiser_fast
            
            f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
            feature_stats('zcr', f)
            
            cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12,
                                     n_bins=7*12, tuning=None))
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
            
            f = librosa.feature.rmse(S=stft)
            feature_stats('rmse', f)
            
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

tracks = pd.read_csv('/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/metadata.csv')
features = pd.DataFrame(index=tracks.index, columns=columns(), dtype=np.float32)

  # More than usable CPUs to be CPU bound, not I/O bound. Beware memory.
  #nb_workers = int(1.5 * len(os.sched_getaffinity(0)))

  # Longest is ~11,000 seconds. Limit processes to avoid memory errors.
  # table = ((5000, 1), (3000, 3), (2000, 5), (1000, 10), (0, nb_workers))
tids = tracks.file_name

print(tids)
pool = multiprocessing.Pool(4)
it = pool.imap_unordered(compute_features, tids)

for i, row in enumerate(tqdm(it, total=len(tids))):
    features.loc[row.name] = row
      
    if i % 1000 == 0:
        save(features, 10)
        test(features, 10)

compute_features('Berta_Trupia-003.wav')

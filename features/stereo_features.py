import librosa
import numpy as np
import sys

def extract(audio, sr, n_fft=2048, n_mels=32):
  spect = librosa.stft(audio, n_fft=n_fft)
  mel_L, mel_R = (
    librosa.feature.melspectrogram(S=spect[0,:], n_mels=n_mels, sr=sr),
    librosa.feature.melspectrogram(S=spect[1,:], n_mels=n_mels, sr=sr)
  )
  return position_and_clarity(np.stack([mel_L, mel_R]))


def position_and_clarity(spect):
  mid = spect[1,:] + spect[0,:]
  side = spect[1,:] - spect[0,:]
  mag_mid = np.abs(mid)
  mag_side = np.abs(side)
  delta_phi_ms = np.angle(mid) - np.angle(side)
  sigma = 0.5 * np.arctan((2 * mag_side * mag_mid * np.cos(delta_phi_ms))/(mag_mid**2 - mag_side**2))
  C = 0.5 * (np.cos(2 * delta_phi_ms) + 1)
  return sigma, C


# if __name__ == "__main__":
#   audio, sr = librosa.load(sys.argv[1], mono=False, sr=48000)
#   extract(audio, sr, n_mels=32)

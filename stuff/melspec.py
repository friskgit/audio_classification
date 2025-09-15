import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/training_data/'
classes = ['Impulse', 'Iteration', 'Vsustain', 'Fsustain']
data_dir = os.path.join(dir, classes[1])
afile = os.path.join(data_dir, '2.wav')

print(afile)
y, sr = librosa.load(afile, sr=None)

S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

fig, ax = plt.subplots()
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title='Mel-frequency spectrogram')

plt.show()

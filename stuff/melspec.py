import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.image import resize

dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/training_data/testing/'
classes = ['Impulse', 'Iteration', 'Vsustain', 'Fsustain']
file_name = 'X1-impulse.wav'
afile = os.path.join(dir, file_name)

print(afile)
y, sr = librosa.load(afile, sr=None)
target_shape = (128, 128)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=20, fmax=10000)
# S = resize(np.expand_dims(S, axis=-1), target_shape)
S = np.resize(S, target_shape)
fig, ax = plt.subplots()
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title='Mel-frequency spectrogram')

plt.show()

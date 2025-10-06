import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/training_data/testing/'
classes = ['Impulse', 'Iteration', 'Vsustain', 'Fsustain']
file_name = 'X1-impulse.wav'
afile = os.path.join(dir, file_name)

print(afile)
y, sr = librosa.load(afile, sr=None)
target_shape = (128, 256)

mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=64)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=20, fmax=8000)
S = np.resize(S, target_shape)
fig, ax = plt.subplots(nrows=2, sharex=True)
img = librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                               x_axis='time', y_axis='mel', fmax=8000,
                               ax=ax[0])
fig.colorbar(img, ax=[ax[0]])
ax[0].set(title='Mel spectrogram')
ax[0].label_outer()
img = librosa.display.specshow(mfccs, x_axis='time', ax=ax[1])
fig.colorbar(img, ax=[ax[1]])
ax[1].set(title='MFCC')
plt.show()

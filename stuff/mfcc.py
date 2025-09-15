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
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
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

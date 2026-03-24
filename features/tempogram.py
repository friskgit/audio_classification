import librosa
import matplotlib.pyplot as plt
import numpy as np
y, sr = librosa.load('/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/training_data/testing/N2-repeating.wav')
tempogram = librosa.feature.tempogram(y=y, sr=sr)
tgr = librosa.feature.tempogram_ratio(tg=tempogram, sr=sr)
fig, ax = plt.subplots(nrows=2, sharex=True)
librosa.display.specshow(tempogram, x_axis='time', y_axis='tempo', ax=ax[0])

librosa.display.specshow(tgr, x_axis='time', ax=ax[1])
ax[0].label_outer()
ax[0].set(title="Tempogram")
ax[1].set(title="Tempogram ratio")
plt.show()
# print(tgr.size)

# np.max(tgr, -1)

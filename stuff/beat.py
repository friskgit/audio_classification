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
import scipy.stats
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
# Or compute pulse with an alternate prior, like log-normal

prior = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
pulse_lognorm = librosa.beat.plp(onset_envelope=onset_env, sr=sr,
                                 prior=prior)
melspec = librosa.feature.melspectrogram(y=y, sr=sr)
fig, ax = plt.subplots(nrows=3, sharex=True)
librosa.display.specshow(librosa.power_to_db(melspec,
                                             ref=np.max),
                         x_axis='time', y_axis='mel', ax=ax[0])

ax[0].set(title='Mel spectrogram')
ax[0].label_outer()
ax[1].plot(librosa.times_like(onset_env),
           librosa.util.normalize(onset_env),
           label='Onset strength')
ax[1].plot(librosa.times_like(pulse),
            librosa.util.normalize(pulse),
             label='Predominant local pulse (PLP)')
ax[1].set(title='Uniform tempo prior [30, 300]')
ax[1].label_outer()
ax[2].plot(librosa.times_like(onset_env),
             librosa.util.normalize(onset_env),
             label='Onset strength')
ax[2].plot(librosa.times_like(pulse_lognorm),
             librosa.util.normalize(pulse_lognorm),
             label='Predominant local pulse (PLP)')
ax[2].set(title='Log-normal tempo prior, mean=120', xlim=[5, 20])
ax[2].legend()

plt.show()

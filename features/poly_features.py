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
  S = np.abs(librosa.stft(y))
  p0 = librosa.feature.poly_features(S=S, order=0)
  p1 = librosa.feature.poly_features(S=S, order=1)
  p2 = librosa.feature.poly_features(S=S, order=2)

  print(p2)
  
  fig, ax = plt.subplots(nrows=4, sharex=True, figsize=(8, 8))
  times = librosa.times_like(p0)
  ax[0].plot(times, p0[0], label='order=0', alpha=0.8)
  ax[0].plot(times, p1[1], label='order=1', alpha=0.8)
  ax[0].plot(times, p2[2], label='order=2', alpha=0.8)
  ax[0].legend()
  ax[0].label_outer()
  ax[0].set(ylabel='Constant term ')
  ax[1].plot(times, p1[0], label='order=1', alpha=0.8)
  ax[1].plot(times, p2[1], label='order=2', alpha=0.8)
  ax[1].set(ylabel='Linear term')
  ax[1].label_outer()
  ax[1].legend()
  ax[2].plot(times, p2[0], label='order=2', alpha=0.8)
  ax[2].set(ylabel='Quadratic term')
  ax[2].legend()
  librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax[3])
                           
  plt.show()

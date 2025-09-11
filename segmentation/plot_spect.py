import matplotlib.pyplot as plt
from maad import sound, util

s, fs = sound.load('./sax.wav')
s_slice = sound.trim(s, fs, 20, 22)

pxx, f_idx = sound.spectrum(s_slice, fs, nperseg=1024)

fig, ax = plt.subplots(2,1, figsize=(10,6))

util.plot_wave(s_slice, fs, ax=ax[0])

util.plot_spectrum(pxx, f_idx, ax=ax[1], log_scale=True)

plt.show()

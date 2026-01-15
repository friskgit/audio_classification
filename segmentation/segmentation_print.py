from maad import sound
from maad.rois import find_rois_cwt
from maad.util import plot_spectrogram
import matplotlib.pyplot as plt
import soundfile as sf

split = []
s, fs = sound.load('./audio/dataton2.wav')
Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=512)
plot_spectrogram(Sxx, extent=ext, db_range=60, gain=20, colorbar=False, figsize=(2.5,10))

regions = find_rois_cwt(s, fs, flims=(7000,10000), tlen=4, th=0, display=True, figsize=(10,6))

plt.show()
print(regions.head)

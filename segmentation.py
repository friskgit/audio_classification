from maad import sound
from maad.rois import find_rois_cwt
from maad.util import plot_spectrogram
import matplotlib.pyplot as plt
import soundfile as sf

s, fs = sound.load('./audio/dataton2.wav')
Sxx, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=512)
plot_spectrogram(Sxx, extent=ext, db_range=60, gain=20, colorbar=False, figsize=(2.5,10))

regions = find_rois_cwt(s, fs, flims=(80,10000), tlen=3, th=0, display=False, figsize=(10,6))

# plt.show()
# print(df_trill)
print(regions.head())

for i, row in regions.iterrows():
    start = int(row['min_t'] * fs)
    end = int(row['max_t'] * fs)
    segment = s[start:end]
    sf.write('audio/segment_{}.wav'.format(i), segment, fs)

# for i,_ in regions.iterrows():

from maad.rois import find_rois_cwt
import librosa
import sounddevice as sd
import soundfile as soundf
from pathlib import Path
import os
import subprocess
from .analysis import Analysis

class SoundFile:
  MAX_LENGTH = 4
  minfrq = 100
  maxfrq = 10000
  tlen = 3
  threshold = 0
  analysis = 0
  
  def __init__(self, path, name):
    self.name = name
    self.path = path
    self.segment_dir = ''
    self.segment_names = []
    self.start = []
    self.end = []
    self.segmented = False
    self.soundfile, self.fs = librosa.load(os.path.join(self.path, self.name), sr=None, mono=True)
    self.length = librosa.get_duration(y = self.soundfile)
    # an array of the segments, or the soundfile if no segments
    self.analysis = []
    self.analysis = Analysis()

  def get_analysis_object(self):
    return self.analysis
  
  def print_path(self):
    if self.segmented:
      return self.segment_dir
    else:
      return self.path

  def print_me(self):
    print(f"{self.name} is the audio.")
    print(f"{self.length} is the length")
    if self.segmented:
      print(self.start)
      for j in range(len(self.start)):
        print('Segment:', self.segment_names[j])
        print('Segment is:', self.start[j], ':', self.end[j])
    
  def play(self, name='default'):
    print(f"{self.name} is playing...")
    print(os.path.join(self.path, self.name))
    sd.play(self.soundfile[self.start[0], self.end[0]], self.fs)
    sd.wait()

  def segment_audio(self):
    """Segment longer files into segments"""
    if self.length > self.MAX_LENGTH:
      self.segmented = True
      regions = find_rois_cwt(self.soundfile, self.fs, flims=(self.minfrq, self.maxfrq), tlen=self.tlen, th=self.threshold, display=False, figsize=(10,6))
      self.segment_dir = os.path.join(self.path, Path(self.name).stem + '_segments')
      if regions.empty:
        if not os.path.isdir(self.segment_dir):
          #        print("create directory")
          os.mkdir(self.segment_dir)
        print("no regions of interest")
        self.start.append(int(0 * self.fs))
        self.end.append(int(4 * self.fs))
        segment = self.soundfile[self.start[0]:self.end[0]]
        self.segment_names.append(self.segment_dir + '/' + Path(self.name).stem + '_segment_{}.wav'.format(0))
        # apply window to segment
        segment = self.apply_fade(segment)
        # change this to maad or librosa
        soundf.write(self.segment_names[0], segment, self.fs)
        return
      else:
        if not os.path.isdir(self.segment_dir):
          #        print("create directory")
          os.mkdir(self.segment_dir)
        for i, row in regions.iterrows():
          #        print(i)
          self.start.append(int(row['min_t'] * self.fs))
          self.end.append(int(row['max_t'] * self.fs))
          segment = self.soundfile[int(row['min_t'] * self.fs):int(row['max_t'] * self.fs)]
          self.segment_names.append(self.segment_dir + '/' + Path(self.name).stem + '_segment_{}.wav'.format(i))
          # apply window to segment
          segment = self.apply_fade(segment)
          # change this to maad or librosa
          soundf.write(self.segment_names[i], segment, self.fs)
    else:
      self.start.append(0)
      self.end.append(int(self.length * self.fs))
      self.segmented = False
      
  def analyze(self):
    """Function to generate a json with features for each segment (if applicable)"""
    if self.segmented:
      for i in range(len(self.segment_names)):
        audiof = self.segment_names[i]
        jsonf, ext = os.path.splitext(audiof)
        no_ext, ext = os.path.splitext(self.name)
        no_ext = no_ext + '-feat-{}.json'.format(i)
        jsonf = os.path.join(str(Path(os.path.dirname(audiof)).parents[0]), no_ext)
        ser = compute_features(audiof, self.soundfile, self.fs)
        json_file = ser.to_dict()
        json_file = { str(k): v for k,v in json_file.items() }
        # the name of the segmented file is parent
        json_file = {"fname": os.path.join(self.path, self.name), "start_time": self.start[0], "end_time": self.end[0], "data": json_file}
        self.analysis.append(json_file)
        with open(os.path.join(path, jsonf), 'w', encoding='utf-8') as f:
          f.write(json.dumps(json_file))
    else:
      audiof = os.path.join(self.path, self.name)
      jsonf, ext = os.path.splitext(audiof)
      jsonf = jsonf + '-feat-0.json'
      ser = compute_features(audiof, self.soundfile, self.fs)
      json_file = ser.to_dict()
      # Add filename header
      json_file = { str(k): v for k,v in json_file.items() }
      json_file = {"fname": audiof, "start_time": self.start[0], "end_time": self.end[0], "data": json_file}
      self.analysis.append(json_file)
      # Write to file
      with open(os.path.join(path, jsonf), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_file))

  def segment_file_name(self, fname):
    import re
    x = re.findall('.*_segment_[0-9]+.wav', fname)
    if len(x) < 1:
      return False
    else:
      return True

  def apply_fade(self, audio, fade_in_duration=0.1, fade_out_duration=0.1):
      # convert to audio indices (samples)
    length_in = int(fade_in_duration * self.fs)
    length_out = int(fade_out_duration * self.fs)
    end = audio.shape[0]
    out = end - length_out

    # compute fade out curve
    # linear fade
    fade_curve_in = np.linspace(0.0, 1.0, length_in)
    fade_curve_out = np.linspace(1.0, 0.0, length_out)

    # apply the curve
    audio[out:end] = audio[out:end] * fade_curve_out
    audio[:length_in] = audio[:length_in] * fade_curve_in
    return audio

  def query_features(self, segment=0, feat='chroma_stft', moment='mean', index = -1):
    """This is a function to extract features from the analysis. 'moments' is a global variable defined in 'imports'"""
    params = (feat, moment)
    value = []
    data = self.analysis[segment]
    for name, size in feature_sizes.items():
      if name is params[0]:
        for mom in moments:
          if mom is params[1]:
            if index < 0:
              for i in range(size):
                query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
                value.append(data['data'][query])
            elif index > 0:
              query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=index)
              value.append(data['data'][query])
    return value

  def feature_vector(self, segment=0, moment='mean'):
    """Function to stack all feature vectors into one. 'moments' is a global variable defined in 'imports'"""
    stacked = []
    data = self.analysis[segment]
    for name, size in feature_sizes.items():
      for mom in moments:
        if mom is moment:
          for i in range(size):
            query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
            stacked.append(data['data'][query])
    return stacked

  def all_feature_vectors(self, moment='mean'):
    """
    Collect all feature vectors for all segments of this file and stack them.
    'moments' is a global variable defined in 'imports'
    """
    all_vectors = []
    for j, a in enumerate(self.analysis):
#      print(f'segment {j}')
      f_vect = {}
      data = a
      stacked = []
      for name, size in feature_sizes.items():
        for mom in moments:
          if mom is moment:
            for i in range(size):
              query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
              stacked.append(data['data'][query])
              f_vect['name'] = data['fname']
              f_vect['segment'] = j
              f_vect['data'] = stacked
      all_vectors.append(f_vect)
    return all_vectors

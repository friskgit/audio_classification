def analyze_sf(directory, selector='.wav'):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  soundfiles = []
  for f in files:
    print(f)
    soundfiles.append(SoundFile(directory, f))
#    if f.endswith(selector):
#      paths.append(os.path.join(directory, f))
#      print(os.path.join(directory, f))
#      call_for_file(os.path.join(directory, f))

from maad import sound
from maad.rois import find_rois_cwt
import librosa
import soundfile as sf
from pathlib import Path
import os
import subprocess

class SoundFile:
  MAX_LENGTH = 4
  minfrq = 500
  maxfrq = 10000
  tlen = 3
  threshold = 0
  
  def __init__(self, path, name):
    self.name = name
    self.path = path
    self.segment_dir = ''
    self.segment_names = []
    self.start = []
    self.end = []
    self.soundfile, self.fs = sound.load(os.path.join(self.path, self.name))
    self.length = librosa.get_duration(path = os.path.join(self.path, self.name))
    if self.length > self.MAX_LENGTH:
      self.segmented = True
      self.segmentAudio()
    else:
      self.start.append(0)
      self.end.append(int(self.length * self.fs))
      self.segmented = False

  def printPath(self):
    if self.segmented:
      return self.segment_dir
    else:
      return self.path

  def printMe(self):
    print(f"{self.name} is the audio.")
    print(f"{self.length} is the length")
    for j in range(len(self.start)):
      print('Segment:', self.segment_names[j])
      print('Segment is:', self.start[j], ':', self.end[j])

  def play(self):
    start = 
    print(f"{self.name} is playing...")
    subprocess.call(['play', os.path.join(self.path, self.name), 'trim', '0', self.MAX_LENGTH])
  
  def segmentAudio(self):
    """Segment longer files into segments"""
    self.truncated = 1
    regions = find_rois_cwt(self.soundfile, self.fs, flims=(self.minfrq, self.maxfrq), tlen=self.tlen, th=self.threshold, display=False, figsize=(10,6))
    self.segment_dir = os.path.join(self.path, Path(self.name).stem + '_segments')
    if not os.path.isdir(self.segment_dir):
      os.mkdir(self.segment_dir)
    for i, row in regions.iterrows():
      self.start.append(int(row['min_t'] * self.fs))
      self.end.append(int(row['max_t'] * self.fs))
      segment = self.soundfile[int(row['min_t'] * self.fs):int(row['max_t'] * self.fs)]
      self.segment_names.append(self.segment_dir + '/' + Path(self.name).stem + '_segment_{}.wav'.format(i))
      sf.write(self.segment_names[i], segment, self.fs)

  def analyze(self):
    """Function to generate a json with features for each segment (if applicable)"""
    if self.segmented:
      for i in range(len(self.segment_names)):
        f = self.segment_names[i]
        jsonf, ext = os.path.splitext(f)
        file_name = os.path.basename(self.name)
        no_ext, ext = os.path.splitext(self.name)
        no_ext = no_ext + '-feat.json'
        jsonf = os.path.join(str(Path(os.path.dirname(f)).parents[0]), no_ext)
        print(jsonf)

    else:
      audiof = os.path.join(self.path, self.name)
      jsonf, ext = os.path.splitext(audiof)
      jsonf = jsonf + '-feat.json'
      ser = compute_features(audiof)
      json_file = ser.to_dict()

      full_path = os.path.abspath(audiof)
  
      # Add filename header
      json_file = { str(k): v for k,v in json_file.items() }
      json_file = {audiof: json_file}
      #    json_file[self.segment_names] = 
  
      # Write to file
      with open(os.path.join(path, jsonf), 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_file))

  def analyzebu(self):
    """Function to generate a json with features for each segment (if applicable)"""
    audiof = os.path.join(self.path, self.name)
    jsonf, ext = os.path.splitext(audiof)
    jsonf = jsonf + '-feat.json'
    ser = compute_features(audiof)
    json_file = ser.to_dict()

    full_path = os.path.abspath(audiof)
  
    # Add filename header
    json_file = { str(k): v for k,v in json_file.items() }
    json_file = {audiof: json_file}
#    json_file[self.segment_names] = 
  
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

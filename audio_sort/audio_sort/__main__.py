import sys
import os
import json
from curses import wrapper
from .soundfile import SoundFile
from .analysis import Analysis

def main():
  # unimportant stuff
  print('in main')
  args = sys.argv[1:]
  print('count of args :: {}'.format(len(args)))
  for arg in args:
    print('passed argument :: {}'.format(arg))

  # the real code
  if len(arg) > 0 and os.path.exists(args[0]):
    print(f"Calling sf_read() with ", args[0])
    sf = read_sf(args[0])
  else:
    print("The directory is not valid.")
  
if __name__ == '__main__':
  main()

def read_sf(directory, selector=['.wav', '.aiff', '.aifc', '.flac', '.ogg', '.mp3']):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  soundfiles = [] # instances of the SoundFile class
  for f in files:
    for s in selector:
      if f.endswith(s):
        soundfiles.append(SoundFile(directory, f))
        print(f)
  for g in soundfiles:
    exists = g.segment_json_exists() 
    if exists == 'none':
      g.segment_audio()
      g.analyze()
    else:
      jsonf = exists
      read_json_file(g, jsonf)
    print(g.analysis)
  return soundfiles

def read_json(directory):
  """Load all the json files in the directory 'directory' into memory"""
  files = os.listdir(directory)
  soundfiles = [] # instances of the SoundFile class
  for f in files:
    # first create SoundFile instances for each 'feat-0.json
    if f.endswith('feat-0.json'):
      full_path = os.path.join(directory, f)
      with open(full_path) as json_file:
        data = json.load(json_file)
        audiof = data['fname']
        directory, fname = os.path.split(audiof)
        sf = SoundFile(directory, audiof)
        update_sound_file(sf, data)
        soundfiles.append(sf)
        print(f'added {fname}')
  for f in files:
    # add segments to existing SoundFile instances
    if f.endswith('.json'):
      full_path = os.path.join(directory, f)
      with open(full_path) as json_file:
        data = json.load(json_file)
        audiof = data['fname']
        directory, fname = os.path.split(audiof)
        if is_segmented(f) == 1:
          for sfi in soundfiles:
            if sfi.name == audiof:
              update_sound_file(sfi, data)
  return soundfiles

def read_json_file(sfi, jsonf):
  with open(os.path.join(sfi.path, jsonf)) as json_file:
    data = json.load(json_file)
    sfi.analysis.append(data)

def update_sound_file(sfi, data):
  """Update an instance with segment data"""
  sfi.analysis.append(data)
  sfi.start.append(data['start_time'])
  sfi.end.append(data['end_time'])
  return sfi

def is_segmented(fname):
  """Returns -1 if fname is not a segment, 0 if the index is > 0 and 1 if the index is equal to 0"""
  import re
  tag = fname[-10:]
  number = re.findall(r'\d+', tag)
  if len(number) > 0:
    if int(number[0]) == 0:
      return 0
    elif int(number[0]) > 0:
      return 1
  else:
    return 0

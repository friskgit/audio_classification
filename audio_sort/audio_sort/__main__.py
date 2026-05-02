import sys
import os
import json
from .soundfile import SoundFile
from .analysis import Analysis
from .read_features import compare_vectors

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

    # play loop
  while True:
    choice = input("Enter a letter: ").lower()
    if choice == 'c':
      number = input("Enter a number: ").lower()
      print('Compare vector at index {}'.format(number))
      r = compare_vectors(sf, int(number))
      winners = r.sort_values(by='value').tail(5)
#      winners = r.drop(index=r.index[0], axis=0, inplace=True)
      print(winners)
      while True:
        play = int(input('Play soundfile: ').lower())
        if play == 0:
          print(winners.iloc[4]['sf_index'])
          afile = sf[winners.iloc[4]['sf_index']]
          afile.play()
        elif play == 1:
          print(winners.iloc[3]['sf_index'])
          afile = sf[winners.iloc[3]['sf_index']]
          afile.play()
        elif play == 2:
          print(winners.iloc[2]['sf_index'])
          afile = sf[winners.iloc[2]['sf_index']]
          afile.play()
        elif play == 3:
          print(winners.iloc[1]['sf_index'])
          afile = sf[winners.iloc[1]['sf_index']]
          afile.play()
        elif play == 4:
          print(winners.iloc[0]['sf_index'])
          afile = sf[winners.iloc[0]['sf_index']]
          afile.play()
  #      file1 = winners.iloc[3]['name']
        elif play == -1:
          break
        else:
          print('Try again')

          # exit
    elif choice == 'q':
      print("Exiting program...")
      break
    else:
      print("Invalid choice, try again.")
  
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
  # print(g.analysis)
  return soundfiles

def read_json(directory): # UNUSED
  """Load all the json files in the directory 'directory' into memory"""
  files = os.listdir(directory)
  soundfiles = [] # instances of the SoundFile class
  audiof = '' # full name
  directory = '' # directory portion
  fname = '' # audio file name
  for f in files:
    # first create SoundFile instances for each 'feat-0.json
    if f.endswith('feat-0.json'):
      full_path = os.path.join(directory, f)
      with open(full_path) as json_file:
        data = json.load(json_file)
        audiof = data['fname']
        directory, fname = os.path.split(audiof)
        sf = SoundFile(directory, fname) # error?
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
            print(f'sfi.name is {sfi.name}')
            print(f'fname is {fname}')
            if sfi.name == fname:
              update_sound_file(sfi, data)
  return soundfiles

def read_json_file(sfi, jsonf):
  with open(os.path.join(sfi.path, jsonf)) as json_file:
    data = json.load(json_file)
    update_sound_file(sfi, data)


def update_sound_file(sfi, data):
  """Update an instance with segment data"""
  sfi.analysis.append(data) # load the entire json file into memory
  sfi.start.append(data['start_time'])
  e = data['end_time']
  sfi.end.append(e)
  print(f'       end time is: {e}')
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

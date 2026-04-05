def read_sf(directory, selector='.wav'):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  soundfiles = [] # instances of the SoundFile class
  for f in files:
    if f.endswith(selector):
#      print(f)
      soundfiles.append(SoundFile(directory, f))
  for g in soundfiles:
    g.print_me()
    g.segment_audio()
    g.analyze()
    if g.segmented:
       print("number of segments:", len(g.segment_names))
  return soundfiles
#      paths.append(os.path.join(directory, f))
#      print(os.path.join(directory, f))
#      call_for_file(os.path.join(directory, f))

def read_json(directory):
  """Load all the json files in the directory 'directory' into memory"""
  files = os.listdir(directory)
  soundfiles = [] # instances of the SoundFile class
  for f in files:
    if f.endswith('.json'):
      print(f)
      full_path = os.path.join(directory, f)
      with open(full_path) as json_file:
        data = json.load(json_file)
        print(data['fname'])
        
#      soundfiles.append(SoundFile(directory))

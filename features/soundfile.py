def read_sf(directory, selector='.wav'):
  """Call 'func' for each matching file in the directory 'directory'"""
  files = os.listdir(directory)
  paths = []
  soundfiles = [] # instances of the SoundFile class
  for f in files:
    if f.endswith(selector):
      print(f)
      soundfiles.append(SoundFile(directory, f))
  for g in soundfiles:
    if g.segmented:
      print("number of segments:", len(g.segment_names))
  return soundfiles
#      paths.append(os.path.join(directory, f))
#      print(os.path.join(directory, f))
#      call_for_file(os.path.join(directory, f))

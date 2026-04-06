filename = '/Users/henrik_frisk/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/Alberto/campione 9-feat.json'
parent = filename[:-12] + '.wav'
with open(filename) as file:
  jsonf = json.load(file)
  for name, size in feature_sizes.items():
    for mom in moments:
      for i in range(size):
        query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
        # print(parent + "/" + query)
        print(jsonf[parent][query])

def query_features(filename, feat='chroma_stft', moment='mean', index = -1):
  """This is a function to extract features from a json file associated with a sound file"""
  params = (feat, moment)
  value = []
  parent = filename[:-12] + '.wav'
  with open(filename) as file:
    jsonf = json.load(file)
    for name, size in feature_sizes.items():
      if name is params[0]:
        for mom in moments:
          if mom is params[1]:
            if index < 0:
              for i in range(size):
                query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
                value.append(jsonf[parent][query])
            elif index > 0:
              query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=index)
              value.append(jsonf[parent][query])
  return value

# print(query_features(filename='Berta_Trupia-003-feat.json', feat='tonnetz'))

def stack_features(filename, moment='mean'):
  """This is a function to stack all feature vectors into one supplying a json file associated with a sound file"""
  params = (moment)
  stacked = []
  parent = filename[:-10] + '.wav'
  with open(filename) as file:
    jsonf = json.load(file)
    for name, size in feature_sizes.items():
      for mom in moments:
        if mom is moment:
          for i in range(size):
            query = "('{n}', '{m}', {i})".format(n=name, m=mom, i=(i+1))
            stacked.append(jsonf[parent][query])
  return stacked

# print(query_features(filename='Berta_Trupia-003-feat.json', feat='tonnetz'))

def compare_vectors_old(master, directory, moment='mean'):
  """Take the vector of the master file and a name of a directory of json files and outputs the cosine similarity between the two. Optionally supply the moment to use."""
  from sklearn.metrics.pairwise import cosine_similarity
  results = {
    'name': ['default'],
    'value': [0]
  }
  for f in os.listdir(directory):
    if f.endswith('.json'):
      feat = stack_features(os.path.join(directory, f))
      sim = cosine_similarity([master], [feat])
      results['name'].append(f[:-10])
      results['value'].append(sim[0][0])
  results_df = pd.DataFrame(results)
  print(results_df.sort_values(by='value'))

def compare_vectors(soundfiles, master=0, moment='mean'):
  """Take the soundfiles[master] vector and get the cosine similarity between it and all other soundfiles. Optionally supply the moment to use."""
  from sklearn.metrics.pairwise import cosine_similarity
  results = {
    'name': ['default'],
    'segment': ['-1'],
    'value': [0]
  }
  mst_feat = soundfiles[master].feature_vector()
#  print(soundfiles[master].name)
  for f in soundfiles:
    feats = f.all_feature_vectors()
    for feature in feats:
      cmp_feat = feature['data']
      sim = cosine_similarity([mst_feat], [cmp_feat])
      results['name'].append(os.path.basename(feature['name']))
 #     print(os.path.basename(feature['name']))
      results['segment'].append(feature['segment'])
      results['value'].append(sim[0][0])
  results_df = pd.DataFrame(results)
  print(results_df.sort_values(by='value'))

def play_name(name, soundfiles):
  for sf in soundfiles:
    if os.path.basename(sf.name) == name:
      print(f"{os.path.basename(sf.name)} is playing...")
      start_sec = str(sf.start[0] / sf.fs)
      stop_sec = str(sf.end[0] / sf.fs)
      subprocess.call(['play', sf.name, "trim", start_sec, stop_sec])

from sklearn.metrics.pairwise import cosine_similarity
a = query_features(filename='Berta_Trupia-006-feat.json')
b = query_features(filename='Berta_Trupia-007-feat.json')
c = query_features(filename='Berta_Trupia-008-feat.json', feat='spectral_contrast')
d = query_features(filename='Berta_Trupia-007-feat.json', feat='spectral_contrast')
sim1 = cosine_similarity([a], [b])
sim2 = cosine_similarity([c], [d])
print(sim1)
print(sim2)

with open(os.path.join(path, 'campione 9-feat.json')) as file:
  jsonf = json.load(file)
  print(jsonf['/Users/henrik_frisk/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/Alberto/campione 9.wav']["('tempogram', 'mean', 2)"])
  #x = json.loads(jsonf)
  #        y = x['Berta_Trumpia.wav']

  tracks = pd.read_csv('/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/metadata.csv')
  features = pd.DataFrame(index=tracks.index, columns=columns(), dtype=np.float32)

    # More than usable CPUs to be CPU bound, not I/O bound. Beware memory.
    #nb_workers = int(1.5 * len(os.sched_getaffinity(0)))

    # Longest is ~11,000 seconds. Limit processes to avoid memory errors.
    # table = ((5000, 1), (3000, 3), (2000, 5), (1000, 10), (0, nb_workers))
  tids = tracks.file_name

  print(tids)
    pool = multiprocessing.Pool(4)
    it = pool.imap_unordered(compute_features, tids)

    for i, row in enumerate(tqdm(it, total=len(tids))):
        features.loc[row.name] = row
        
        if i % 1000 == 0:
            save(features, 10)

  import json
  with open('/Users/henrik_frisk/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/dataset/SCHAEFFER/data.json', 'w', encoding='utf-8') as f:
      json.dump(json_file, f, ensure_ascii=False, indent=4)

  # json stuff
  file_name = "Berta_Trupia-003.wav"
  feature = "cnhroma_cens"
  stat = 'kurtosis'
  num = [1, 2, 3]
  value = 1.208494e+00
  chroma_cens_reg = {"name": file_name "feat": feature}
  json.dumps(chroma_cens_reg)

  files = os.listdir(path)
  for f in files:
      print(f)

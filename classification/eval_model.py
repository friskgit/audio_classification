  test_accuracy=model.evaluate(X_test,y_test,verbose=0)
  print(test_accuracy[1])

  test_accuracy=model.evaluate(X_test,y_test,verbose=0)
  print(test_accuracy[1])

  test_accuracy=model.evaluate(X_test,y_test,verbose=0)
  print(test_accuracy[1])

  import glob

  # Load the saved model
  dir = os.getcwd()
  print(dir)
  print(os.path.join(dir, 'audio_classification.keras'))
  #model = load_model(os.path.join(dir, 'audio_classification.keras'))

  # Define the target shape for input spectrograms
  target_shape = (128, 128)

  # Define your class labels
  classes = ['HarmSus', 'HarmImp', 'HarmIter', 'NoiseSus', 'NoiseImp', 'NoiseIter', 'CompositeSus', 'CompositeImp', 'CompositeIter']
  tartyp = ['N0', 'N1', 'N2', 'X0', 'X1', 'X2', 'Y0', 'Y1', 'Y2']
  # Function to preprocess and classify an audio file
  def test_audio(file_path, model):
      # Load and preprocess the audio file
      audio_data, sample_rate = librosa.load(file_path, sr=None)
      audio_data = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
      audio_data = resize(np.expand_dims(audio_data, axis=-1), target_shape)
      audio_data = tf.reshape(audio_data, (1,) + target_shape + (1,))
          
      # Make predictions
      predictions = model.predict(audio_data)
      
      # Get the class probabilities
      class_probabilities = predictions[0]
      
      # Get the predicted class index
      predicted_class_index = np.argmax(class_probabilities)
      
      return class_probabilities, predicted_class_index

  def test_audio_mfcc(file_path, model):
    # Load and preprocess the audio file
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    audio_data = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
    audio_data = resize(np.expand_dims(audio_data, axis=-1), target_shape)
    audio_data = tf.reshape(audio_data, (1,) + target_shape + (1,))
        
    # Make predictions
    predictions = model.predict(audio_data)
    
    # Get the class probabilities
    class_probabilities = predictions[0]
    
    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)
    
    return class_probabilities, predicted_class_index

  # Test an audio file
  test_audio_dir = os.path.join(dir, 'training_data/testing/')

  extension = "*.wav"
  for test_audio_file in glob.glob(os.path.join(test_audio_dir, extension)):
      class_probabilities, predicted_class_index = test_audio_mfcc(test_audio_file, model)
      print(f'{os.path.basename(test_audio_file)}, , ,')
      print(f'Class, Probability, Accuracy, Classified, Analyzed')
      # Display results for all classes
      for i, class_label in enumerate(classes):
          probability = class_probabilities[i]
          print(f'{class_label}, {probability:.4f}')

      for i, c in enumerate(tartyp):
          if c in test_audio_file:
              match = classes[i]
          
      # Calculate and display the predicted class and accuracy
      predicted_class = classes[predicted_class_index]
  #    if('{os.path.basename(test_audio_file)}' )
      accuracy = class_probabilities[predicted_class_index]
      print(f', , {accuracy:.4f}, {predicted_class}, {match}')

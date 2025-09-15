test_accuracy=model.evaluate(X_test,y_test,verbose=0)
print(test_accuracy[1])

import glob
# Load the saved model
# dir = os.getcwd()
dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/'
model = load_model(dir + 'audio_classification_imp_iter.keras')

# Define the target shape for input spectrograms
target_shape = (128, 128)

# Define your class labels
classes = ['Impulse', 'Iteration', 'Vsustain', 'Fsustain']

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

# Test an audio file
test_audio_dir = '/Volumes/Freedom/Dropbox/Documents/kmh/forskning/applications/KK/KKS 2022 IRESAP/audio_classification/classification/training_data'

extension = "*.wav"
for test_audio_file in glob.glob(os.path.join(test_audio_dir, extension)):
    class_probabilities, predicted_class_index = test_audio(test_audio_file, model)

    # Display results for all classes
    for i, class_label in enumerate(classes):
        probability = class_probabilities[i]
        print(f'Class: {class_label}, Probability: {probability:.4f}')

        # Calculate and display the predicted class and accuracy
        predicted_class = classes[predicted_class_index]
        accuracy = class_probabilities[predicted_class_index]
        print(f'The audio {os.path.basename(test_audio_file)} is classified as: {predicted_class}')
        print(f'Accuracy: {accuracy:.4f}')

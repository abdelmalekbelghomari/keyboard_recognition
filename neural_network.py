import tensorflow as tf
import numpy as np
import librosa  # for loading and preprocessing audio files

# Define a fixed size for the spectrograms
spectrogram_length = 400  # You can adjust this based on your data
spectrogram_height = 128  # Typical height for a Mel spectrogram with default settings

# Function to load an audio file and convert it to a spectrogram
def load_audio_file(file_path, max_pad_len=spectrogram_length):
    audio, sample_rate = librosa.load(file_path, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)

    # Padding or trimming the spectrogram
    if spectrogram.shape[1] < max_pad_len:
        pad_width = max_pad_len - spectrogram.shape[1]
        spectrogram = np.pad(spectrogram, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        spectrogram = spectrogram[:, :max_pad_len]

    spectrogram = spectrogram[..., np.newaxis]  # Adding the channel dimension
    return spectrogram

# Function to read sentences from a file and generate space/non-space labels
def generate_labels(file_path, max_pad_len=spectrogram_length):
    all_labels = []
    with open(file_path, 'r') as file:
        for line in file:
            sentence = line.strip().split('. ', 1)[-1]
            char_labels = [1 if char == ' ' else 0 for char in sentence]
            # Pad or trim the label list to match the spectrogram length
            if len(char_labels) < max_pad_len:
                char_labels.extend([0] * (max_pad_len - len(char_labels)))  # Pad with 0s
            else:
                char_labels = char_labels[:max_pad_len]  # Trim to the length
            all_labels.append(char_labels)  # Add the labels for this sentence
    return all_labels

# Path to your sentences file
sentences_file_path = 'sentences.txt'

# Load your data and labels
x_train = []
y_train = generate_labels(sentences_file_path)

for i in range(1, 51):
    file_name = f'fichiers wav/Nouvel enregistrement {i}.wav'
    x_train.append(load_audio_file(file_name))

x_train = np.array(x_train)
y_train = np.array(y_train)
# print(y_train)

## Create a simple model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(spectrogram_height, spectrogram_length, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(400, activation='sigmoid')  # Une sortie pour chaque frame du spectrogramme
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=100)

# Evaluate the model
# Use a different file for testing
test_audio = load_audio_file('fichiers wav/Nouvel enregistrement 1.wav')
test_audio = np.array([test_audio])
predictions = model.predict(test_audio)
print(predictions)
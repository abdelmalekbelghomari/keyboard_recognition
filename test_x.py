import librosa
import numpy as np
# Fonction pour charger un fichier audio et le convertir en spectrogramme
def load_audio_file(file_path, max_pad_len=400):
    audio, sample_rate = librosa.load(file_path, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)

    # Padding ou trimming du spectrogramme
    if spectrogram.shape[1] < max_pad_len:
        pad_width = max_pad_len - spectrogram.shape[1]
        spectrogram = np.pad(spectrogram, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        spectrogram = spectrogram[:, :max_pad_len]

    spectrogram = spectrogram[..., np.newaxis]  # Ajout de la dimension de canal
    return spectrogram

# Charger le premier fichier audio et le convertir en spectrogramme
file_path = 'fichiers wav/Nouvel enregistrement 1.wav'
spectrogram = load_audio_file(file_path)

# Convertir en décibels
spectrogram_db = librosa.power_to_db(spectrogram.squeeze(), ref=np.max)


# Si vous voulez visualiser le spectrogramme
import matplotlib.pyplot as plt

# Afficher le spectrogramme avec une échelle de couleur améliorée
plt.figure(figsize=(10, 4))
librosa.display.specshow(spectrogram_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
plt.title('Spectrogramme')
plt.colorbar(format='%+2.0f dB')
plt.show()

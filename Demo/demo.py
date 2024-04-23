from flask import Flask, request, send_from_directory
from flask_cors import CORS
import os
import subprocess  
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

app = Flask(__name__, static_folder='spectrogrammes')
CORS(app)

def supprimer_fichier(chemin_fichier):
    if os.path.exists(chemin_fichier):
        os.remove(chemin_fichier)

@app.route('/upload', methods=['POST'])
def upload_audio():
    fichier_audio = './uploads/audio_converted.wav'
    fichier_spectrogramme = './spectrogrammes/spectrogram.png'
    supprimer_fichier(fichier_audio)
    supprimer_fichier(fichier_spectrogramme)
    if 'audio' not in request.files:
        return 'Aucun fichier audio trouvé', 400

    audio = request.files['audio']
    filename = 'audio_received.wav'
    path_to_save = os.path.join('uploads', filename)
    audio.save(path_to_save)

    converted_filename = 'audio_converted.wav'
    path_to_converted = os.path.join('uploads', converted_filename)
    subprocess.run(['D:\\Application\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe', '-i', path_to_save, '-acodec', 'pcm_s16le', '-ar', '44100', path_to_converted], check=True)

    y, sr = librosa.load(path_to_converted, sr=None)
    sf.write(path_to_converted, y, sr, format='wav')

    S = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.ioff()
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    spectrogram_path = os.path.join('spectrogrammes', 'spectrogram.png')
    plt.savefig(spectrogram_path)
    plt.close()

    full_spectrogram_path = os.path.abspath(spectrogram_path)
    return {'spectrogram   Path': full_spectrogram_path}

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('spectrogrammes', path)


@app.route('/predict', methods=['POST'])
def predict():
    command = [
        "python", "person_pipeline.py"
    ]
    subprocess.run(command, check=True)
    return {'sucess': 'coucou'}


@app.route('/predict_letter', methods=['POST'])
def predict_letter():
    command = [
        "python", "letter_pipeline.py"
    ]
    subprocess.run(command, check=True)
    return {'sucess': 'coucou'}


if __name__ == '__main__':
    app.run(debug=True)

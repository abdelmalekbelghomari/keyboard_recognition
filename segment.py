import librosa
import numpy as np
import os
from scipy.io.wavfile import write

def detect_key_strokes(input_audio_path, output_dir, frame_length=2048, hop_length=512, energy_threshold=0.01, min_silence_duration=0.1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    y, sr = librosa.load(input_audio_path, mono=True)

    # Calcul de l'énergie sur des fenêtres glissantes
    energy = np.array([np.sum(np.abs(y[i:i+frame_length])**2) for i in range(0, len(y) - frame_length, hop_length)])
    
    # Seuil d'énergie pour détecter la présence d'un son (peut nécessiter un ajustement)
    threshold_indices = np.nonzero(energy > energy_threshold)[0]

    # Fusion des indices proches pour créer des segments de frappes de clavier
    key_strokes = []
    previous_index = None
    for index in threshold_indices:
        if previous_index is None or index > previous_index + (min_silence_duration * sr / hop_length):
            key_strokes.append(index * hop_length)
        previous_index = index

    # Sauvegarder les segments détectés
    for i, start in enumerate(key_strokes):
        end = start + frame_length
        if end <= len(y):
            segment_audio = y[start:end]
            segment_filename = f'keystroke_{i}.wav'
            segment_path = os.path.join(output_dir, segment_filename)
            write(segment_path, sr, (segment_audio * 32767).astype(np.int16))
            print(f'Segment saved: {segment_path}')

if __name__ == "__main__":
    input_audio_path = "lettres/cedric/audio/e_cedric.wav"
    output_dir = "segmented_audios"
    detect_key_strokes(input_audio_path, output_dir)

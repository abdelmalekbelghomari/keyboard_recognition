import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.io import wavfile
from scipy.signal import find_peaks

def split(audio_path, alpha = 1.47, min_distance_sec = 0.31, seconds_to_remove = 0.3, low_threshold = 40) :
    if not os.path.exists(audio_path):
        print("L'audio spécifié n'existe pas.")
        return
    segments = []
    
    sample_rate, data = wavfile.read(audio_path)
    samples_to_remove = int(sample_rate * seconds_to_remove)
    data = data[:-samples_to_remove]
    
    # Calculer le seuil et trouver les pics
    mean_val = np.mean(abs(data[data > low_threshold]))
    threshold = alpha * mean_val
    
    peaks, _ = find_peaks(data, height=threshold, distance=int(sample_rate * min_distance_sec))
    num_peaks = len(peaks)
    #print(f"{audio_path} : {num_peaks} segments trouvés")
    '''
    # Visualisation des résultats pour le débogage
    times = np.arange(len(data)) / sample_rate
    
    plt.figure(figsize=(12, 7))
    plt.plot(times, data, label='Signal')
    plt.plot(times[peaks], data[peaks], "x", label='Pics détectés', color='red')
    plt.title(f'Détection des pics dans l\'audio {audio_path}')
    plt.xlabel('Temps (secondes)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()
    '''
    for i, _ in enumerate(peaks):
        start = 0 if i == 0 else (peaks[i] + peaks[i-1]) // 2
        end = len(data) if i == num_peaks - 1 else (peaks[i] + peaks[i+1]) // 2
        segments.append(data[start:end])
    return segments, sample_rate
    

def generate_audio_segments(audio_path, output_folder, alpha = 1.47, min_distance_sec = 0.31, seconds_to_remove = 0.3, low_threshold = 40):
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
    segments, sample_rate = split(audio_path=audio_path, alpha = alpha, min_distance_sec = min_distance_sec, seconds_to_remove = seconds_to_remove, low_threshold = low_threshold)
    for i, segment in enumerate(segments):
        output_path = os.path.join(output_folder, f'segment_{i+1}.wav')
        wavfile.write(output_path, sample_rate, segment)
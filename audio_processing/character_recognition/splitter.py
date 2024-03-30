from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np

def split(audio_path, alpha=1.47, min_distance_sec=0.31, seconds_to_remove=0.3, low_threshold=40):
    sample_rate, data = wavfile.read(audio_path)
    samples_to_remove = int(sample_rate * seconds_to_remove)
    data = data[:-samples_to_remove]
    
    mean_val = np.mean(abs(data[data > low_threshold]))
    threshold = alpha * mean_val
    peaks, _ = find_peaks(data, height=threshold, distance=int(sample_rate * min_distance_sec))

    segments = []
    num_peaks = len(peaks)
    for i in range(num_peaks):
        start = 0 if i == 0 else (peaks[i] + peaks[i-1]) // 2
        end = len(data) if i == num_peaks - 1 else (peaks[i] + peaks[i+1]) // 2
        segments.append(data[start:end])
    return segments, sample_rate
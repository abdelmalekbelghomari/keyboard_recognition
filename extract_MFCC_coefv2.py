import os
import librosa
import csv
import argparse
import numpy as np
from scipy.io.wavfile import read, write
import shutil

def normalize(x: np.ndarray):
    return x / np.max(np.abs(x))

def split_key_presses(input_file: str, output_dir: str = './key_audios/', prefix: str = 'output',
                      trigger: float = 250, time_before: float = 0.020, time_after: float = 0.20,
                      normalize_result: bool = False):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    sample_rate, audio = read(input_file)
    length_after = int(time_after * sample_rate)
    length_before = int(time_before * sample_rate)
    outputs = []

    i = 0
    while i < len(audio):
        if i + length_after > len(audio):
            break
        if audio[i] >= trigger and i >= length_before:
            key_stroke = audio[i - length_before:i + length_after]
            if normalize_result:
                key_stroke = normalize(key_stroke)
            outputs.append(key_stroke)
            i += length_after
        i += 1

    os.makedirs(output_dir, exist_ok=True)

    for i, key_stroke in enumerate(outputs):
        output_file = os.path.join(output_dir, f'{prefix}_{i+1}.wav')
        write(output_file, sample_rate, np.asarray(key_stroke, dtype=np.int16))

def extract_mfcc(audio_file, csv_file, label, append_csv=True):
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_vector = mfccs.flatten()
    
    mode = 'a' if append_csv else 'w'
    header = ['label'] + [f'feature{i+1}' for i in range(len(mfccs_vector))]
    
    with open(csv_file, mode, newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header only if file is empty
            writer.writerow(header)
        writer.writerow([label] + list(mfccs_vector))

def extract_mfcc_from_folder(output_csv, label, input_dir='./key_audios/'):
    if not os.path.exists(input_dir):
        print("Input directory does not exist.")
        return
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    files.sort()

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        extract_mfcc(input_path, output_csv, label, append_csv=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, required=True, help='Path to the audio file')
    parser.add_argument('--csv_file', type=str, required=True, help='Path to the output CSV file')
    parser.add_argument('--label', type=str, required=True, help='Label for all audio segments')
    args = parser.parse_args()

    split_key_presses(args.audio_file)
    extract_mfcc_from_folder(args.csv_file, args.label)

if __name__ == "__main__":
    main()

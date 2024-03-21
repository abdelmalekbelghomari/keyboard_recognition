import os
import csv
import librosa
import argparse
import numpy as np

def extract_mfccs_from_audio(y, sr, n_mfcc, n_segments=20):
    total_samples = len(y)
    samples_per_segment = total_samples // n_segments
    mfccs_vectors = []

    for segment in range(n_segments):
        start_sample = segment * samples_per_segment
        end_sample = start_sample + samples_per_segment

        mfccs = librosa.feature.mfcc(y=y[start_sample:end_sample], sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        
        mfccs_vectors.extend(mfccs_mean)
    
    return mfccs_vectors

def extract_mfccs_to_csv(input_dir, labels_file, output_csv, n_mfcc, n_segments=20):
    labels = []
    with open(labels_file, 'r') as f:
        for line in f:
            # Strip whitespace and skip empty lines
            clean_line = line.strip()
            if clean_line:  # Cette condition exclut les lignes vides
                labels.append(clean_line)

    file_exists = os.path.isfile(output_csv)
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            headers = ['label'] + [f'feature{i+1}' for i in range(n_segments * n_mfcc)]
            writer.writerow(headers)
        
        audio_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.wav')])
        if len(labels) != len(audio_files):
            print("Attention: Le nombre de labels ne correspond pas au nombre de fichiers audio.")

        for index, filename in enumerate(audio_files):
            if index < len(labels):
                file_path = os.path.join(input_dir, filename)
                y, sr = librosa.load(file_path)
                mfccs_vector = extract_mfccs_from_audio(y, sr, n_mfcc, n_segments=n_segments)
                writer.writerow([labels[index]] + mfccs_vector)
            else:
                print(f"Aucun label correspondant pour {filename}")

def main():
    parser = argparse.ArgumentParser(description="Extract MFCCs from WAV files to a CSV file, with unique labels for each file.")
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing .wav files.')
    parser.add_argument('--labels_file', type=str, required=True, help='Path to the .txt file containing labels for each audio file.')
    parser.add_argument('--output_csv', type=str, required=True, help='Path to the output CSV file.')
    parser.add_argument('--n_mfcc', type=int, default=20, help='Number of MFCC features to extract for each segment.')
    parser.add_argument('--n_segments', type=int, default=20, help='Number of segments to divide each audio file into.')
    
    args = parser.parse_args()
    
    extract_mfccs_to_csv(args.input_dir, args.labels_file, args.output_csv, args.n_mfcc, args.n_segments)

if __name__ == "__main__":
    main()
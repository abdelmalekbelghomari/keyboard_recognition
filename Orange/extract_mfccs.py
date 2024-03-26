import os
import csv
import librosa
import argparse
import numpy as np

def extract_mfccs_from_audio(y, sr, n_mfcc, n_segments=20):
    """
    Extract MFCCs from an audio file and ensure that the MFCCs cover the entire audio evenly,
    divided into n_segments.
    """
    total_samples = len(y)
    samples_per_segment = total_samples // n_segments
    mfccs_vectors = []

    for segment in range(n_segments):
        start_sample = segment * samples_per_segment
        end_sample = start_sample + samples_per_segment

        # Extract MFCCs for this segment
        mfccs = librosa.feature.mfcc(y=y[start_sample:end_sample], sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)  # Taking the mean to reduce dimensionality
        
        mfccs_vectors.extend(mfccs_mean)
    
    return mfccs_vectors

def extract_mfccs_to_csv(input_dir, label, output_csv, n_mfcc, n_segments=20):
    """
    Extract MFCCs from audio files by adjusting the segment length based on the audio file's total length,
    aiming to produce a fixed number of features (MFCCs) for each file.
    
    Parameters:
        input_dir (str): Directory containing .wav files.
        label (str): Label to use for the first column of the CSV.
        output_csv (str): Path to the output CSV file.
        n_mfcc (int): Number of MFCC features to extract for each segment.
        n_segments (int): Number of segments to divide each audio file into.
    """
    file_exists = os.path.isfile(output_csv)
    
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            headers = ['label'] + [f'feature{i+1}' for i in range(n_segments * n_mfcc)]  # Adjust based on n_mfcc
            writer.writerow(headers)
        
        for filename in os.listdir(input_dir):
            if filename.endswith('.wav'):
                file_path = os.path.join(input_dir, filename)
                y, sr = librosa.load(file_path)

                mfccs_vector = extract_mfccs_from_audio(y, sr, n_mfcc, n_segments=n_segments)
                
                writer.writerow([label] + mfccs_vector)

def main():
    parser = argparse.ArgumentParser(description="Extract MFCCs from WAV files to a CSV file, adjusting the number of segments based on audio file's length.")
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing .wav files.')
    parser.add_argument('--label', type=str, required=True, help='Label for the first column of the CSV.')
    parser.add_argument('--output_csv', type=str, required=True, help='Path to the output CSV file.')
    parser.add_argument('--n_mfcc', type=int, default=20, help='Number of MFCC features to extract for each segment.')
    parser.add_argument('--n_segments', type=int, default=20, help='Number of segments to divide each audio file into.')
    
    args = parser.parse_args()
    
    extract_mfccs_to_csv(args.input_dir, args.label, args.output_csv, args.n_mfcc, args.n_segments)

if __name__ == "__main__":
    main()

import argparse
import os
from audio_processing.character_recognition.splitter import split
from audio_processing.character_recognition.mfcc_extractor import extract_mfcc
import pandas as pd

def process_audio_files(audio_folder, label_file, output_csv, n_mfcc=13):
    all_dataframes = []
    with open(label_file, 'r') as file:
        labels = [line.rstrip("\n") for line in file]

    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.wav')])

    for audio_file, label in zip(audio_files, labels):
        audio_path = os.path.join(audio_folder, audio_file)
        segments, sample_rate = split(audio_path=audio_path)
        label = label if label.strip() else ' ' * len(segments)  # Handle space labels
        
        if len(segments) != len(label):
            print(f"Warning: Mismatch for {audio_file} - {len(segments)} segments vs. {len(label)} labels.")
            continue

        mfcc_dataframes = extract_mfcc(segments, sample_rate, label, n_mfcc=n_mfcc)
        all_dataframes.extend(mfcc_dataframes)
        
        print(f"MFCC extracted for {audio_file} with {len(segments)} segments matching {len(label)} labels.\n")

    concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    concatenated_df.columns = ['label'] + [f'feature{i+1}' for i in range(n_mfcc)]
    concatenated_df.to_csv(output_csv, index=False)
    print(f"All MFCC data has been saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract MFCC features for audio files into a single CSV file, including space labels.")
    parser.add_argument("--audio_folder", help="Path to the folder containing the audio files.")
    parser.add_argument("--label_file", help="Path to the label file.")
    parser.add_argument("--output_csv", help="Path for the output CSV file where all MFCC data will be saved.")
    parser.add_argument("--n_mfcc", type=int, default=13, help="Number of MFCC features to extract.")

    args = parser.parse_args()

    if not os.path.exists(args.audio_folder) or not os.path.exists(args.label_file):
        print("Audio folder or label file not found.")
        exit(1)
    if not os.path.isdir(os.path.dirname(args.output_csv)):
        os.makedirs(os.path.dirname(args.output_csv))

    process_audio_files(args.audio_folder, args.label_file, args.output_csv, args.n_mfcc)
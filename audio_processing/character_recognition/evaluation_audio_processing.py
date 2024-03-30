# main_no_labels.py

import argparse
import os
from splitter import split
from mfcc_extractor import extract_mfcc
import pandas as pd

def process_audio_files_no_labels(audio_folder, output_csv, n_mfcc=13):
    all_dataframes = []
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.wav')])

    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        segments, sample_rate = split(audio_path=audio_path)
        
        # Créer une chaîne de '?' correspondant au nombre de segments
        label = '?' * len(segments)

        mfcc_dataframes = extract_mfcc(segments, sample_rate, label, n_mfcc=n_mfcc)
        all_dataframes.extend(mfcc_dataframes)
        
        print(f"MFCC extracted for {audio_file} with {len(segments)} segments, labels set to '?'.\n")

    concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    concatenated_df.columns = ['label'] + [f'feature{i+1}' for i in range(n_mfcc)]
    concatenated_df.to_csv(output_csv, index=False)
    print(f"All MFCC data without actual labels has been saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract MFCC features for audio files into a single CSV file, setting labels to '?'.")
    parser.add_argument("--audio_folder", help="Path to the folder containing the audio files.")
    parser.add_argument("--output_csv", help="Path for the output CSV file where all MFCC data will be saved, with '?' as labels.")
    parser.add_argument("--n_mfcc", type=int, default=20, help="Number of MFCC features to extract.")

    args = parser.parse_args()

    if not os.path.exists(args.audio_folder):
        print("Audio folder not found.")
        exit(1)
    if not os.path.isdir(os.path.dirname(args.output_csv)):
        os.makedirs(os.path.dirname(args.output_csv))

    process_audio_files_no_labels(args.audio_folder, args.output_csv, args.n_mfcc)

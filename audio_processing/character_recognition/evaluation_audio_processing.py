import argparse
from splitter import split
from mfcc_extractor import extract_mfcc
import pandas as pd
import os

def process_audio_file_no_labels(audio_file, output_csv, n_mfcc=13):
    if not os.path.isfile(audio_file):
        print(f"Le fichier audio spécifié n'a pas été trouvé : {audio_file}")
        exit(1)

    if not os.path.isdir(os.path.dirname(output_csv)):
        os.makedirs(os.path.dirname(output_csv))

    segments, sample_rate = split(audio_file)
    
    # Créer une chaîne de '?' correspondant au nombre de segments
    label = ['?' for _ in range(len(segments))]

    mfcc_dataframes = extract_mfcc(segments, sample_rate, label, n_mfcc=n_mfcc)
    
    concatenated_df = pd.concat(mfcc_dataframes, ignore_index=True)
    concatenated_df.columns = ['label'] + [f'feature{i+1}' for i in range(n_mfcc)]
    concatenated_df.to_csv(output_csv, index=False)
    print(f"MFCC extracted for {audio_file} with {len(segments)} segments, labels set to '?'.")
    print(f"The MFCC data without actual labels has been saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract MFCC features from a single audio file into a CSV file, setting labels to '?'.")
    parser.add_argument("--audio_file", required=True, help="Path to the audio file.")
    parser.add_argument("--output_csv", required=True, help="Path for the output CSV file where the MFCC data will be saved, with '?' as labels.")
    parser.add_argument("--n_mfcc", type=int, default=20, help="Number of MFCC features to extract.")

    args = parser.parse_args()

    process_audio_file_no_labels(args.audio_file, args.output_csv, args.n_mfcc)

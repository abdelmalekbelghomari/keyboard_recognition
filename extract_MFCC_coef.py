import os
import subprocess

import librosa
import csv
from IPython.display import Audio
import pandas as pd
import numpy as np
from scipy.io.wavfile import read, write
import shutil
import argparse

def normalize(x: np.ndarray):
    return x / np.max(x)

def split_key_presses(input_file: str, output_dir: str = './key_audios/', prefix: str = 'output',
                      trigger: float = 370, time_before: float = 0.020, time_after: float = 0.20,
                      normalize_result: bool = False):
    # Nettoyer le dossier de sortie avant de créer de nouveaux fichiers
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Load the audio from the input file
    sample_rate, audio = read(input_file)

    # Calculate the splitting parameters
    length_after = int(time_after * sample_rate)
    length_before = int(time_before * sample_rate)

    # Initialize the list to store key stroke excerpts
    outputs = []

    i = 0
    while i < len(audio):
        # End of usable recording
        if i + length_after > len(audio):
            break
        # If the threshold is exceeded and we have reached "time_before" before the threshold
        if audio[i] >= trigger and i >= length_before:
            # Extract the excerpt
            key_stroke = audio[i - length_before:i + length_after]
            # Normalize if necessary
            if normalize_result:
                key_stroke = normalize(key_stroke)
            outputs.append(key_stroke)
            i += length_after
        i += 1

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each key stroke as a separate WAV file
    for i, key_stroke in enumerate(outputs):
        output_file = os.path.join(output_dir, f'{prefix}_{i+1}.wav')
        write(output_file, sample_rate, np.asarray(key_stroke, dtype=np.int16))
        # print(f'Created {output_file}')


def extract_mfcc(audio_file, csv_file, label):
    y, sr = librosa.load(audio_file)
    
    # Extraction des coefficients MFCC
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # Aplatir les coefficients MFCC en un vecteur
    mfccs_vector = mfccs.flatten()
           
    # Écrire les coefficients MFCC aplatis dans le fichier CSV
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['label'] + ['feature{}'.format(i+1) for i in range(len(mfccs_vector))])
        # Écrire les données dans le fichier CSV
        writer.writerow([label] + list(mfccs_vector))


def extract_mfcc_from_folder(output_csv, label_file, input_dir='./key_audios/'):
    if not os.path.exists(input_dir):
        print("Le répertoire d'entrée spécifié n'existe pas.")
        return

    # Liste des fichiers dans le répertoire d'entrée
    files = os.listdir(input_dir)
    files.sort()  # Tri des noms de fichiers

    mfcc_dataframes = []

    # Lecture du fichier de labels
    with open(label_file, 'r') as labels:
        label_data = labels.read().strip()  # Lire tous les caractères du fichier de labels

    # Assurez-vous que la longueur des labels correspond au nombre de fichiers audio
    if len(label_data) != len(files):
        print("Nombre de fichiers audio et de labels ne correspond pas: il y a")
        print(len(label_data), "keywords")
        print(len(files), "audios")
        return

    for filename, label in zip(files, label_data):
        if filename.endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(input_dir, filename.replace('.wav', '_mfcc.csv'))
            
            # Remplacer les espaces par "space" dans le label
            label_modifie = label.replace(" ", "space")

            # Appel à la fonction extract_mfcc pour extraire les MFCC et écrire dans un fichier CSV
            extract_mfcc(input_path, output_path, label_modifie)  

            # Lecture du fichier CSV nouvellement généré
            df = pd.read_csv(output_path)

            # Ajout du DataFrame à la liste des DataFrames MFCC
            mfcc_dataframes.append(df)

            # Suppression du fichier CSV individuel une fois la concaténation terminée
            os.remove(output_path)

    # Concaténation de tous les DataFrames en un seul DataFrame
    concatenated_df = pd.concat(mfcc_dataframes, ignore_index=True)
    
    # Écriture du DataFrame global dans un fichier CSV unique
    concatenated_df.to_csv(output_csv, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, help='Chemin vers le fichier audio')
    parser.add_argument('--csv_file', type=str, help='Chemin vers le fichier CSV de sortie')
    parser.add_argument('--label_file', type=str, help='Chemin vers le fichier de labels')
    args = parser.parse_args()

    split_key_presses(args.audio_file)
    extract_mfcc_from_folder(args.csv_file, args.label_file)
    
if __name__ == "__main__":
    main()

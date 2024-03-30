import librosa
import pandas as pd
import numpy as np

def extract_mfcc(data_audios, sample_rate, labels_file, output_csv, n_mfcc=13):
    with open(labels_file, 'r') as file:
        labels = [char for char in file.read() if char != '\n']

    if len(labels) != len(data_audios):
        print(f"Warning : Labels count: {len(labels)} vs. Audio segments count: {len(data_audios)}")
        return
    
    # Convertir les données audio en float32
    data_audios = [np.float32(data) for data in data_audios]
    
    mfcc_dataframes = []

    for data, label in zip(data_audios, labels):
        label = "space" if label == ' ' else label
        
        mfccs = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=n_mfcc)
        mfccs_vector = np.mean(mfccs, axis=1)
        
        df = pd.DataFrame([np.append(label, mfccs_vector)])
        mfcc_dataframes.append(df)

    # Concaténation des DataFrames individuels
    concatenated_df = pd.concat(mfcc_dataframes, ignore_index=True)
    
    # Définition des noms de colonne, en incluant 'label' comme première colonne
    concatenated_df.columns = ['label'] + [f'feature{i+1}' for i in range(n_mfcc)]
    
    # Sauvegarde du DataFrame dans un fichier CSV
    concatenated_df.to_csv(output_csv, index=False)
    print(f"Les données MFCC ont été sauvegardées dans {output_csv}")


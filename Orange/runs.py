import os
import subprocess
import csv

# Définition du chemin de base et du script à exécuter
base_dir = os.path.expanduser('~/projet2A/Orange')
script_path = os.path.join(base_dir, 'extract_mfccs.py')
model_script_path = os.path.join(base_dir, 'script.py')

# Chemins d'entrée relatifs
input_dirs = ['../phrases/haykel_phrase/', '../phrases/cedric_phrase/', '../phrases/abdel_phrase/', '../phrases/bedda_phrase/']
labels = ['haykel', 'cedric', 'abdel', 'bedda']

# Fichier de résultats
results_csv = os.path.join(base_dir, 'mfcc_results.csv')

# Itérer sur une gamme de valeurs pour MFCC et segments
for n_mfcc in range(5, 51, 5):  # de 5 à 50 inclus, par pas de 5
    for n_segments in range(5, 51, 5):
        # Suppression du fichier 'phrases.csv' s'il existe
        phrases_csv_path = os.path.join(base_dir, 'phrases.csv')
        if os.path.exists(phrases_csv_path):
            os.remove(phrases_csv_path)

        # Exécuter le script d'extraction pour chaque dossier d'entrée et label
        for input_dir, label in zip(input_dirs, labels):
            abs_input_dir = os.path.abspath(os.path.join(base_dir, input_dir))
            subprocess.run(["python3", script_path, "--input_dir", abs_input_dir, "--label", label, "--output_csv", phrases_csv_path, "--n_mfcc", str(n_mfcc), "--n_segments", str(n_segments)], check=True)

        # Exécuter le script du modèle
        predictions_output_path = os.path.join(base_dir, 'results.txt')
        subprocess.run(["python3", model_script_path, "--input_csv", phrases_csv_path, "--predictions_output", predictions_output_path], check=True)

        # Lire le contenu du fichier 'results.txt' pour obtenir la performance
        with open(predictions_output_path, 'r') as file:
            model_performance = file.read()

        # Écrire les paramètres et la performance dans 'mfcc_results.csv'
        with open(results_csv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([n_mfcc, n_segments, model_performance.strip()])


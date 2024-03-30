import os
from spliter import split
from mfcc_generator import extract_mfcc
import argparse

def generate_label_mapping():
    """
    Génère une correspondance entre les lettres de l'alphabet (et "space") et les numéros de fichiers de labels.
    """
    mapping = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for i, letter in enumerate(alphabet, start=1):
        mapping[letter] = str(i) + ".txt"
    mapping["space"] = "27.txt"
    return mapping

def extract_mfcc_for_folder(audio_folder, labels_folder, output_folder, n_mfcc = 13):
    """
    Extrait les MFCC pour chaque fichier audio dans un dossier donné,
    en utilisant les labels correspondants dans un autre dossier,
    en suivant l'ordre alphabétique pour les labels.
    """
   
    # Lister et trier les fichiers audio
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.wav')])
    labels_files = sorted([f for f in os.listdir(labels_folder) if f.endswith('.txt')])
    labels_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]) if os.path.splitext(os.path.basename(x))[0].isdigit() else float('inf'))

    for audio_file, labels_file in zip(audio_files, labels_files):
        audio_path = os.path.join(audio_folder, audio_file)
        label_file_path = os.path.join(labels_folder, labels_file)
        
        # Générer les segments audio et extraire les MFCC
        segments, sample_rate = split(audio_path=audio_path)
        
        # Construire le chemin de sortie pour les MFCC
        output_csv_path = os.path.join(output_folder, os.path.splitext(audio_file)[0] + '_mfcc.csv')
        
        # Extraire et sauvegarder les MFCC dans un fichier CSV
        extract_mfcc(segments, sample_rate, label_file_path, output_csv_path, n_mfcc=n_mfcc)
        
        print(f"MFCC extracted and saved for {audio_file} using label {labels_file}.\n")
        
        
        
if __name__ == "__main__":
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(description="Extract MFCC features for audio files in a folder.")
    
    # Ajout des arguments attendus
    parser.add_argument("audio_folder", help="Path to the folder containing the audio files.")
    parser.add_argument("labels_folder", help="Path to the folder containing the label files.")
    parser.add_argument("output_folder", help="Path to the folder where the MFCC CSV files will be saved.")
    parser.add_argument("n_mfcc", help="number of features")
    
    # Parse les arguments de la ligne de commande
    args = parser.parse_args()
    
    # Vérifier que les dossiers existent
    if not os.path.exists(args.audio_folder):
        print(f"Audio folder '{args.audio_folder}' not found.")
        exit(1)
    if not os.path.exists(args.labels_folder):
        print(f"Labels folder '{args.labels_folder}' not found.")
        exit(1)
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    
    # Appeler la fonction principale avec les chemins fournis
    extract_mfcc_for_folder(args.audio_folder, args.labels_folder, args.output_folder, int(args.n_mfcc))

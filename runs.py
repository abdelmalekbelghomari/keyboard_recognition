
import subprocess
import string
import os 

def run_extraction_for_alphabet(audio_directory='lettres/cedric/audio/', csv_file='lettres_cedric.csv'):
    for letter in string.ascii_lowercase:  # Génère toutes les lettres de a à z
        # Construire le nom du fichier basé sur la lettre actuelle
        audio_file_name = f"{letter}_cedric.wav"
        audio_file_path = os.path.join(audio_directory, audio_file_name)

        # Construire la commande à exécuter
        command = [
            "python3", "extract_MFCC_coefv2.py",
            "--audio_file", audio_file_path,
            "--csv_file", csv_file,
            "--label", letter
        ]

        print(f"Exécution de la commande pour la lettre '{letter}': {command}")
        
        # Exécuter la commande
        try:
            subprocess.run(command, check=True)
            print(f"Commande exécutée avec succès pour la lettre '{letter}'.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de la commande pour la lettre '{letter}': {e}")

if __name__ == "__main__":
    run_extraction_for_alphabet()
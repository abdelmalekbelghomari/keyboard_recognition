import subprocess
import os

def execute_commands_and_delete_csv():
    # Définition de la première commande pour extraire les MFCCs
    command1 = [
        "python3", "extract_mfccs_file.py",
        "--audio_file", "../phrases/cedric_phrase/1_cedric.wav",
        "--label", "?",
        "--output_csv", "test.csv"
    ]
    
    # Définition de la deuxième commande pour exécuter le modèle entraîné
    command2 = [
        "python3", "trained_model.py",
        "--model", "../models/person_recognizer.joblib",
        "--scaler", "../scalers/scaler.joblib",
        "--input_csv", "test.csv",
        "--predictions_output", "results.txt"
    ]

    try:
        # Exécution de la première commande
        print("Exécution de la première commande...")
        subprocess.run(command1, check=True)
        print("Première commande exécutée avec succès.")
        
        # Exécution de la deuxième commande
        print("Exécution de la deuxième commande...")
        subprocess.run(command2, check=True)
        print("Deuxième commande exécutée avec succès.")

    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de l'exécution des commandes: {e}")
        return

    # Suppression du fichier CSV
    csv_file = "test.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"Le fichier {csv_file} a été supprimé avec succès.")
    else:
        print(f"Le fichier {csv_file} n'existe pas et ne peut être supprimé.")

if __name__ == "__main__":
    execute_commands_and_delete_csv()

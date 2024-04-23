import subprocess
import os

def execute_workflow():
    # Définition de la première commande pour extraire les MFCC et écrire dans test.csv
    command1 = [
        "python", "../audio_processing/character_recognition/evaluation_audio_processing.py",
        "--audio_file", "./uploads/audio_converted.wav",
        "--output_csv", "../test1.csv",
    ]
    
    # Définition de la deuxième commande pour exécuter le modèle entraîné et enregistrer les prédictions dans results.txt
    command2 = [
        "python", "../evaluation/trained_model.py",
        "--model", "../models/third_letter_recognizer.joblib",
        "--scaler", "../scalers/20_feature_scaler.joblib",
        "--input_csv", "../test1.csv",
        "--predictions_output", "../models_results/letter_results.txt"
    ]

    try:
        # Exécution de la première commande
        print("Extraction des MFCCs et écriture dans test.csv...")
        subprocess.run(command1, check=True)
        print("Extraction terminée avec succès.")
        
        # Exécution de la deuxième commande
        print("Exécution du modèle et enregistrement des prédictions dans results.txt...")
        subprocess.run(command2, check=True)
        print("Modèle exécuté avec succès et prédictions enregistrées.")

    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de l'exécution des commandes: {e}")
        return

    # Suppression du fichier CSV
    csv_file = "../test1.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"Le fichier {csv_file} a été supprimé avec succès.")
    else:
        print(f"Le fichier {csv_file} n'existe pas et ne peut être supprimé.")

if __name__ == "__main__":
    execute_workflow()
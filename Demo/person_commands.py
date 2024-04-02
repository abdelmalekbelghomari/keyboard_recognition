import subprocess
import os

def execute_commands_and_delete_csv():
    # Définition de la première commande pour extraire les MFCCs
    command1 = [
        "python3", "../audio_processing/person_recognition/evaluation_mfcc_extractor.py",
        "--audio_file", "../sentences_audios/haykel_sentences/1_haykel.wav",
        "--output_csv", "../test2.csv",
    ]
    
    # Définition de la deuxième commande pour exécuter le modèle entraîné
    command2 = [
        "python3", "../evaluation/trained_model.py",
        "--model", "../models/second_person_recognizer.joblib",
        "--scaler", "../scalers/400_features_scaler.joblib",
        "--input_csv", "../test2.csv",
        "--predictions_output", "../models_results/person_results.txt"
    ]

    try:
        # Exécution de la première commande
        print("Exécution de la première commande...")
        subprocess.run(command1, check=True)
        print("Première commande exécutée avec succès.")
        csv_file = "../test2.csv"
        if os.path.exists(csv_file):
            print(f"Le fichier {csv_file} a été créé avec succès.")
        else:
            print(f"Le fichier {csv_file} n'a pas été créé.")
            return
        
        # Exécution de la deuxième commande
        print("Exécution de la deuxième commande...")
        subprocess.run(command2, check=True)
        print("Deuxième commande exécutée avec succès.")

    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de l'exécution des commandes: {e}")
        return

    # Suppression du fichier CSV
    csv_file = "../test2.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"Le fichier {csv_file} a été supprimé avec succès.")
    else:
        print(f"Le fichier {csv_file} n'existe pas et ne peut être supprimé.")

if __name__ == "__main__":
    execute_commands_and_delete_csv()

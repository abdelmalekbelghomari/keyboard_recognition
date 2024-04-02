import argparse
from joblib import load
import pandas as pd
import nltk
from nltk.corpus import words
from Levenshtein import distance as levenshtein_distance

def find_closest_word(input_word, dictionary):
    """
    Trouve le mot le plus proche dans le dictionnaire en utilisant la distance de Levenshtein.
    """
    closest_word = min(dictionary, key=lambda word: levenshtein_distance(word, input_word))
    return closest_word


def correct_output_with_dictionary(model_output, dictionary):
    """
    Corrige la sortie du modèle en utilisant la distance de Levenshtein pour chaque mot prédit.
    """
    return [find_closest_word(word, dictionary) for word in model_output]

def load_dictionary(language):
    """
    Charge un dictionnaire anglais ou français en fonction de la langue spécifiée.
    """
    if language == 'english':
        nltk.download('words', quiet=True)
        return set(words.words())
    elif language == 'french':
        with open('french_words.txt', 'r') as file:
            return set(file.read().split())
    else:
        raise ValueError("Langue non supportée.")
    

# Définition des arguments pour le script
parser = argparse.ArgumentParser(description="Exécute un modèle sauvegardé sur des données d'entrée et écrit les prédictions.")
parser.add_argument('--model', required=True, help='Chemin vers le fichier du modèle sauvegardé (.joblib).')
parser.add_argument('--scaler', required=True, help='Chemin vers le fichier du scaler sauvegardé (.joblib).')
parser.add_argument('--use_levenshtein', action='store_true', help='Utiliser la distance de Levenshtein pour la correction.')
parser.add_argument('--language', choices=['english', 'french'], help='Choisir la langue pour la correction par distance de Levenshtein.')
parser.add_argument('--input_csv', required=True, help='Chemin vers le fichier CSV d\'entrée contenant les données à prédire.')
parser.add_argument('--predictions_output', required=True, help='Chemin de sortie pour enregistrer les prédictions dans un fichier texte.')

args = parser.parse_args()

if args.use_levenshtein and not args.language:
    raise ValueError("--use_levenshtein nécessite --language avec 'english' ou 'french'.")

dictionary = None
if args.use_levenshtein:
    dictionary = load_dictionary(args.language)


# Chargement du modèle et du scaler
model = load(args.model)
scaler = load(args.scaler)

# Chargement des données d'entrée
data = pd.read_csv(args.input_csv)

# Séparation des caractéristiques (features) et de la cible (target)
X = data.iloc[:, 1:].values  # Assurez-vous que cela correspond à la structure de vos données
# Pas de y (cible) ici, car nous faisons des prédictions

# Mise à l'échelle des caractéristiques avec le scaler chargé
X_scaled = scaler.transform(X)

# Faire des prédictions avec le modèle
predictions = model.predict(X_scaled)

# Replace 'space' with ' ' in predictions
predictions = [prediction.replace('space', ' ') for prediction in predictions]


# Écrire les prédictions dans le fichier de sortie spécifié
with open(args.predictions_output, 'w') as f:
    for prediction in predictions:
        f.write(f"{prediction}")
    f.write(f"\n")

print(f"Prédictions enregistrées dans : {args.predictions_output}")

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import load, dump
import nltk
import argparse
from nltk.corpus import words
from Levenshtein import distance as levenshtein_distance

# nltk.download('words') only one time
english_words = set(words.words())

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
        return set(words.words())
    elif language == 'french':
        with open('french_words.txt', 'r') as file:
            return set(file.read().split())
    else:
        raise ValueError("Langue non supportée.")

parser = argparse.ArgumentParser(description="Script pour prédiction avec option de correction par distance de Levenshtein.")
parser.add_argument('--use_levenshtein', action='store_true', help='Utiliser la distance de Levenshtein pour la correction.')
parser.add_argument('--language', choices=['english', 'french'], help='Choisir la langue pour la correction par distance de Levenshtein.')
parser.add_argument('--input_csv', required=True, help='Chemin vers le fichier CSV d\'entrée contenant les données.')
parser.add_argument('--predictions_output', required=True, help='Chemin de sortie pour enregistrer les prédictions.')


args = parser.parse_args()

if args.use_levenshtein:
    if not args.language:
        parser.error("--use_levenshtein nécessite --language avec 'english' ou 'french'.")
    dictionary = load_dictionary(args.language)
else:
    dictionary = None

df = pd.read_csv(args.input_csv)

y = df.iloc[:, 0].values
X = df.iloc[:, 1:].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = MLPClassifier(hidden_layer_sizes=(500,), activation='relu', solver='adam', alpha=0.0001, max_iter=200, random_state=1)

model.fit(X_train_scaled, y_train)

print("Score de précision sur l'ensemble d'entraînement:", model.score(X_train_scaled, y_train))
print("Score de précision sur l'ensemble de test:", model.score(X_test_scaled, y_test))

# Prédictions du modèle sur l'ensemble de test
predictions = model.predict(X_test_scaled)

if args.use_levenshtein:
    predictions = correct_output_with_dictionary(predictions, english_words)

# Affichage des prédictions et des valeurs réelles
print("\nPrédictions du modèle sur l'ensemble de test:")
print(predictions)

print("\nValeurs réelles de l'ensemble de test:")
print(y_test)

# Écriture des prédictions dans un fichier texte
with open(args.predictions_output, 'w') as file:
    for prediction in predictions:





        
        file.write(f"{prediction}")
    file.write(f"\n")

print(f"Prédictions enregistrées dans : {args.predictions_output}")

# Enregistrement du modèle
model_filename = '../models/mlp_model.joblib'
dump(model, model_filename)
print(f"Modèle enregistré sous le nom : {model_filename}")

# Enregistrement du scaler
scaler_filename = '../scalers/scaler.joblib'
dump(scaler, scaler_filename)
print(f"Scaler enregistré sous le nom : {scaler_filename}")
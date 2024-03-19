import argparse
from joblib import load
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Définition des arguments pour le script
parser = argparse.ArgumentParser(description="Exécute un modèle sauvegardé sur des données d'entrée et écrit les prédictions.")
parser.add_argument('--model', required=True, help='Chemin vers le fichier du modèle sauvegardé (.joblib).')
parser.add_argument('--scaler', required=True, help='Chemin vers le fichier du scaler sauvegardé (.joblib).')
parser.add_argument('--input_csv', required=True, help='Chemin vers le fichier CSV d\'entrée contenant les données à prédire.')
parser.add_argument('--predictions_output', required=True, help='Chemin de sortie pour enregistrer les prédictions dans un fichier texte.')

args = parser.parse_args()

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

# Écrire les prédictions dans le fichier de sortie spécifié
with open(args.predictions_output, 'w') as f:
    for prediction in predictions:
        f.write(f"{prediction}")
    f.write(f"\n")

print(f"Prédictions enregistrées dans : {args.predictions_output}")

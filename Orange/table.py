import pandas as pd

# Remplacez 'mfcc_results.csv' par le chemin vers votre fichier CSV
file_path = 'mfcc_results.csv'

# Lire les données CSV
df = pd.read_csv(file_path)

# Restructurer les données pour le tableau pivot
pivot_df = df.pivot(index='Nombre de Segments', columns='Nombre de MFCCs', values='Performance du Modèle')

# Afficher le tableau
print(pivot_df)
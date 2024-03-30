def fusionner_fichiers(chemins_fichiers, fichier_sortie):
    with open(fichier_sortie, 'w') as output_file:
        # Ouvre tous les fichiers en même temps
        with open(chemins_fichiers[0], 'r') as file1, \
             open(chemins_fichiers[1], 'r') as file2, \
             open(chemins_fichiers[2], 'r') as file3:

            # Lit toutes les lignes de tous les fichiers en même temps
            lignes_fichier1 = file1.readlines()
            lignes_fichier2 = file2.readlines()
            lignes_fichier3 = file3.readlines()

            # Boucle à travers toutes les lignes et les écrit dans le fichier de sortie
            for ligne1, ligne2, ligne3 in zip(lignes_fichier1, lignes_fichier2, lignes_fichier3):
                output_file.write(f"{ligne1.strip()}\n")
                output_file.write(f"{ligne2.strip()}\n")
                output_file.write(f"{ligne3.strip()}\n")

# Liste des chemins des fichiers d'entrée
chemins_fichiers = ["../cedric/labels.txt", "../haykel/labels.txt", "../winnie/labels.txt"]
fichier_sortie = "labels.txt"

# Appel de la fonction pour fusionner les fichiers
fusionner_fichiers(chemins_fichiers, fichier_sortie)

print("La fusion des fichiers a été effectuée avec succès.")
# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 13/02/2025

-------------------------------------------------------------------------------
                    020 Init Fichier
-------------------------------------------------------------------------------
"""


# __init__.py

# Lire les versions des packages depuis requirements.txt
def print_versions():
    with open(prog_folder+r"\requirements.txt", encoding="utf-8") as f:
        for line in f:
            print(line.strip())


# Si nécessaire, appeler la fonction pour afficher les versions
print_versions()  # Décommente pour afficher toutes les versions

# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 09/02/2025

-------------------------------------------------------------------------------
                    260 ajout_donnees_freq
-------------------------------------------------------------------------------
"""


def etape260():

    
    etape = "260_ajout_donnees_freq"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.6.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.6.1: Importation Données")
    
    df = pd.read_excel(os.path.join(output_folder_200, 'Films_250.xlsx'))
    
    df_frequentation = pd.read_excel(_0_file_frequentation_cinema, 
                                     sheet_name="semaine", 
                                     header = 6)
    
    # On supprime la première ligne car cxela fait doublons avec semaine 52:
    df_frequentation = df_frequentation.iloc[1:].reset_index(drop=True)
    
    # 2.6.2: On créé les données de fréquentations
    logging.info("2.6.2: Création des données de fréquentation")
    
    # Trouver l'index "Entrées (millions)" égale "Recette guichet (M€)"
    index = df_frequentation[df_frequentation["Entrées (millions)"] == "Recettes guichet (M€)"].index[0]
    
    # On garde les lignes avant cet index
    df_frequentation = df_frequentation.iloc[:index]
    
    # Renommer la première colonne pour identifier les semaines
    df_frequentation.rename(columns={df_frequentation.columns[0]: "Semaine"}, inplace=True)
    
    # Transformer les données de format large à format long
    df_frequentation = df_frequentation.melt(id_vars=["Semaine"], var_name="Année", value_name="Nb Entrées")
    
    # Trier les données
    df_frequentation = df_frequentation.sort_values(by=["Année", "Semaine"]).reset_index(drop=True)
    
    df_frequentation = df_frequentation[df_frequentation["Semaine"].astype(str).str.startswith("semaine")]
    
    # On fait en fonction de 2 années précédentes
    df_frequentation['Année Cible'] = df_frequentation['Année'] + 2
    
    df_frequentation["Semaine"] = df_frequentation["Semaine"].str.replace('semaine ', '', regex=True)
    df_frequentation["Semaine"] = df_frequentation["Semaine"].str.replace(r'\*', '', regex=True)
    df_frequentation["Semaine"] = df_frequentation["Semaine"].astype(int)
    df_frequentation = df_frequentation.sort_values(by=["Année", "Semaine"]).reset_index(drop=True)
    
    # 2.6.3: On fusionne les 2 dataframes
    logging.info("2.6.3: Fusion des 2 dataframes")
    
    # Fusionner sur "Semaine" et "Année_cible"
  
    df["Semaine"] = df['Date de sortie'].dt.isocalendar().week
    df["Année"] = df['Date de sortie'].dt.isocalendar().year
    
    df = df.merge(df_frequentation, left_on=["Semaine", "Année"], right_on=["Semaine", "Année Cible"], how="left")

    df.drop(['Semaine', 'Année_x', 'Année_y', 'Année Cible'], axis=1, inplace=True)  
    
    df.rename(columns={'Nb Entrées': 'Nb entrées semaine année précédente'}, inplace=True)
    
    
    # TEMPORAIRE : AJOUTER UNE ETAPE QUI REMPLACE LES VALEURS MANQUANTES DE BUDGET-----
    df['Nb entrées semaine année précédente'] = df['Nb entrées semaine année précédente'].fillna(1500000)
    # TEMPORAIRE ----------------------------------------------------------------------
    
    
    
    # 2.6.4: Exportation Données étape 260:
    logging.info('Exportation Données étape 260')
    
    df.to_excel(os.path.join(output_folder_200, 'Films_260.xlsx'), index=False)
        
    
    logger.info('Fréquentation des cinémas ajoutés')
    print('Fréquentation des cinémas ajoutés')
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------

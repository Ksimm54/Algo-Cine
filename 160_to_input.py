# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 31/03/2025

-------------------------------------------------------------------------------
                    160_to_input
-------------------------------------------------------------------------------
"""

def etape160():
    
    
    global scraping_do
    
    
    etape = "160_to_input"
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.6.1: Import des données
    logging.info("1.6.1: Import des données")
    
    df_y = pd.read_excel(_0_file_films_youtube)
    df_w = pd.read_excel(_0_file_films_w)
    df_films = pd.read_excel(_0_file_films)
    df_cd = pd.read_excel(_0_file_films_cd)
    
    if os.path.exists(_0_file_to_complete) == True:
        dossier = to_complete_folder
        file = _0_file_to_complete
        
    elif os.path.exists(_0_file_films_to_ad) == True:
        dossier = input_folder
        file = _0_file_films_to_ad
        
    else: 
        
        logger.info("Fichier en Input n'existe pas")
        print("Fichier en Input n'existe pas")
        
        # ---------- FIN DU JOURNAL
        logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
        logging.shutdown()
        # ----------
        
        sys.exit()
        
        
    df_input = pd.read_excel(os.path.join(dossier, file))    
    
    # On séléctionne seulement les films en 1:
    df_w = df_w[df_w['Wiki'] == 1]
    
    # Création de la table des clés pour relier les films entre youtube et wikipedia
    
    df_w_tit = df_w[["Titre_key", "Titre", "Date de sortie"]].copy()
    df_w_tit['Source'] = 'Wiki'
    df_w_tit["Date de sortie"] = pd.to_datetime(df_w_tit["Date de sortie"], errors="coerce")
    
    df_y_tit = df_y[["Titre_key_1", "Titre_key_2", "Titre"]].copy()
    df_y_tit['Source'] = 'Youtube'
    
    # Définition de Titre_key_2 pour wikipedia
    
    # Application de la transformation
    df_w_tit["Titre_key_1"] = (
        df_w_tit["Titre"]  # Sélectionner la colonne "Titre"
        .apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)  # Appliquer unidecode pour enlever les accents et convertir en minuscule
        .str.replace(r"\s*:\s*.*", "", regex=True)  # Supprimer tout après le premier ":" et ce qui suit
        .str.replace(r"\W+", " ", regex=True)  # Remplacer les caractères spéciaux par des espaces
        .str.replace(r"\s+", "", regex=True)  # Supprimer tous les espaces
        .str.strip()  # Enlever les espaces au début et à la fin
        .str.replace(r"\d+\s*$", "", regex=True)  # Supprimer les numéros à la fin de la chaîne
    )
    
    df_w_tit['Titre_key_1'] = df_w_tit['Titre_key_1']+df_w_tit['Date de sortie'].dt.year.astype(str)
    
    
    # Full join sur 'Titre_key_1'
    df_merged = pd.merge(df_w_tit, df_y_tit, on="Titre_key_1", how="outer", suffixes=("_wiki", "_youtube"))
    
    # Création de la colonne finale 'Source'
    df_merged["Source"] = df_merged.apply(
        lambda row: f"{row['Source_wiki'] or ''} | {row['Source_youtube'] or ''}", axis=1
    )
    
    # Suppression des anciennes colonnes inutiles
    df_merged = df_merged[["Titre_key", "Titre_key_1", "Titre_key_2", "Source"]]
    
    df_merged = df_merged.sort_values(by=["Source"], ascending=[True])
    
    df_merged = df_merged.drop_duplicates()  
    

    # On fusionne les données entre wikipedia et cine_directors
    df_w_tit = df_w[["Titre_key", "Titre", "Réalisateur", "Acteur Principal", "Acteur Secondaire", "Durée", "Studio de Production",
                     "Société de Distribution","Date de sortie", "Pays", "Budget", "Style"]].copy()
    
    df_cd_tit = df_cd[(df_cd['New'] == 1)]
    df_cd_tit = df_cd_tit[['Titre_key', 'Entrées', 'Budget', 'Nbre de copies']]
    
    new_df_w_tit = df_w_tit.merge(df_cd_tit, on='Titre_key', how='left')
    
    new_df_w_tit["Budget"] = new_df_w_tit["Budget_x"].fillna(new_df_w_tit["Budget_y"])
    new_df_w_tit = new_df_w_tit.drop(columns=["Budget_x", "Budget_y"])
    

    # La partie de vérification étant faite on peut envoyer les données dans input:
        
    df_w_tit = new_df_w_tit[["Titre_key", "Titre", "Réalisateur", "Acteur Principal", "Acteur Secondaire", "Durée", "Studio de Production",
                     "Société de Distribution","Date de sortie", "Pays", "Budget", "Entrées", "Nbre de copies", "Style"]].copy()
    
    df_w_tit["Date de sortie"] = pd.to_datetime(df_w_tit["Date de sortie"], errors="coerce")
    
    df_y_tit = df_y[["Titre_key_1", "Titre_key_2", "Vues", "Likes"]].copy()
    
    # Définition de Titre_key_2 pour wikipedia
    
    # Application de la transformation
    df_w_tit["Titre_key_1"] = (
        df_w_tit["Titre"]  # Sélectionner la colonne "Titre"
        .apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)  # Appliquer unidecode pour enlever les accents et convertir en minuscule
        .str.replace(r"\s*:\s*.*", "", regex=True)  # Supprimer tout après le premier ":" et ce qui suit
        .str.replace(r"\W+", " ", regex=True)  # Remplacer les caractères spéciaux par des espaces
        .str.replace(r"\s+", "", regex=True)  # Supprimer tous les espaces
        .str.strip()  # Enlever les espaces au début et à la fin
        .str.replace(r"\d+\s*$", "", regex=True)  # Supprimer les numéros à la fin de la chaîne
    )
    
    df_w_tit['Titre_key_1'] = df_w_tit['Titre_key_1']+df_w_tit['Date de sortie'].dt.year.astype(str)
    
    df_y_tit = df_y[["Titre_key_1", "Titre_key_2", "Titre", "Likes", "Vues"]].copy()
    
    # Statistiques par rapports aux données de films:
    # On regroupe les informations des films
    df_agg = df_y_tit.groupby('Titre_key_1').agg(
        Nb_Bandes_annonces=('Titre_key_1', 'count'),
        Moyenne_Vues=('Vues', 'mean'),
        Max_Vues=('Vues', 'max'),
        Max_Likes=('Likes', 'max'),
        Moyenne_Likes=('Likes', 'mean')
    ).reset_index()
    
    # Fusionner avec le DataFrame original pour avoir ces colonnes en parallèle
    df_y_tit = df_y_tit.merge(df_agg, on='Titre_key_1', how='left')
    
    # On créer les infos sur le nombre de vues et like maximum donc on garde la ligne du minimum
    
    df_y_tit = df_y_tit.sort_values(by = ['Titre_key_1', 'Vues'], ascending = [True, False])
    df_y_tit = df_y_tit.drop_duplicates(subset=['Titre_key_1'], keep='last')
    
    
    # Full join sur 'Titre_key_1'
    df_merged = pd.merge(df_w_tit, df_y_tit, on="Titre_key_1", how="left", suffixes=("_wiki", "_youtube"))
    
    df_merged = df_merged.rename(columns={"Titre_wiki": "Titre"})
    
    df_merged = df_merged[['Titre_key', 'Titre', 'Réalisateur', 'Acteur Principal', 'Acteur Secondaire', 'Durée', 'Studio de Production', 
                           'Société de Distribution', 'Date de sortie', 'Pays', 'Style', 'Budget', 'Entrées', 'Nbre de copies', 'Likes', 'Vues', 'Nb_Bandes_annonces', 
                           'Moyenne_Vues', 'Max_Vues', 'Max_Likes', 'Moyenne_Likes']]
    
    
    df_merged = df_merged[(~df_merged["Likes"].isna()) & (~df_merged["Nbre de copies"].isna())]
    
    
    df_merged = df_merged.sort_values(by = ['Date de sortie', 'Titre'], ascending = [True, True])
                          
    
    # On envoit les données qui ne sont pas déjà dans Films.xlsx ou Input
    
    # Récupérer toutes les valeurs de Titre_key dans une liste
    titre_keys = list(df_films["Titre_key"]) + list(df_input["Titre_key"])
    
    # Supprimer les lignes de df_merged qui ont un Titre_key dans cette liste
    df_merged = df_merged[~df_merged["Titre_key"].isin(titre_keys)]
    
    
    
    # On ajoute les données à l'input
    
    new_df_input = pd.concat([df_input, df_merged], ignore_index=True)
    new_df_input = new_df_input.sort_values(by=['Date de sortie', 'Titre'], ascending=[True, True])
    new_df_input = new_df_input.drop_duplicates(subset=['Titre_key'], keep='last')
    
    # Dans ces input 
    
    new_df_input.to_excel(os.path.join(dossier, file), index=False)
    
    # On ajoute un filtre sur les cellules avec des valeurs manquantes
    
    wb = load_workbook(os.path.join(dossier, file))
    ws = wb.active  # Sélectionne la feuille active
    
    # Style pour le fond jaune
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    
    # Appliquer le style aux cellules contenant des valeurs manquantes
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.value is None or cell.value == ' ' or cell.value == '0':  # Si la cellule contient une valeur manquante
                cell.fill = yellow_fill
    
    # Enregistrer le fichier avec le style appliqué
    wb.save(os.path.join(dossier, file)) 
    
    
    # Export
    
    if os.path.exists(os.path.join(output_folder_100, 'Films_160.xlsx')) == True:
        shutil.move(os.path.join(output_folder_100, 'Films_160.xlsx'), os.path.join(output_folder_100, r'Historique/Films_160'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
    new_df_input.to_excel(os.path.join(output_folder_100, 'Films_160.xlsx'), index=False)


    if os.path.exists(_0_file_keys_wy) == True:
        shutil.move(_0_file_keys_wy, os.path.join(data_folder, r'Historique/keys_w_y'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
    df_merged.to_excel(_0_file_keys_wy, index=False)

    
    
    
    
    
    
    
    
    
    
    
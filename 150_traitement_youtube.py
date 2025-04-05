# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 26/03/2025

-------------------------------------------------------------------------------
                    150_traitement_youtube
-------------------------------------------------------------------------------
"""

def etape150():
    
    
    global scraping_do
    
    
    etape = "150_traitement_youtube"
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.4.1: Import des données
    logging.info("1.4.1: Import des données")
    
    token_df = pd.read_excel(_0_file_param_variables, sheet_name = _0_sheet_token)
    df_y = pd.read_excel(_0_file_films_youtube)
    df = pd.read_excel(os.path.join(output_folder_100, 'Films_140.xlsx'))
    # On supprime les valeurs vides pour Vidéo ID lorsqu'il n'y a pas de données pour une semaine
    df = df.dropna(subset=['Vidéo ID'])
    
    old_len = len(df)
    
    #On vérifie que le nombre de token n'a pas été atteint:  
    df = df.dropna(subset=['Titre'])
    new_len = len(df)
    
    if old_len > new_len and old_len > 0: 
        
        print("Limite de Token atteinte")
        token_df['Nb Token'] = 0
        
        with pd.ExcelWriter(_0_file_param_variables, mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
            token_df.to_excel(writer, sheet_name=_0_sheet_token, index=False)

    # On vérifie que le scraping a été effectué
    if scraping_do == 1: 
    
        print("Scraping effectué: Lancement de l'étape 150")
        
        #Traitement des données
        # On enlève les séries
        df['Titre_Original'] = df['Titre'].str.replace(r'\s+', ' ', regex=True).str.strip()
        df = df[~df['Titre_Original'].str.contains(r'Saison \d+', regex=True)]

        
        df["Année"] = df["Titre"].str.extract(r"\((.*\d+.*)\)", expand=False)  # Extraire tout entre parenthèses
        df["Année"] = df["Année"].str.extract(r"(\d{4})")  # Extraire les 4 chiffres de l'année

        
        # Extraction du texte avant "Bande Annonce" (insensible à la casse)
        df['Titre_nettoye'] = df['Titre'].str.extract(r'^(.*?)(?=\s*[Bb][Aa][Nn][Dd][Ee][Ss]?\s*[Aa][Nn][Nn][Oo][Nn][Cc][Ee][Ss])', expand=True)
        # Remplace les NaN (cas où "Bande Annonce" n'est pas trouvé) par la valeur originale
        df['Titre_nettoye'] = df['Titre_nettoye'].fillna(df['Titre'])
        
        
        # Fonction pour extraire les mots entièrement en majuscules
        def extract_uppercase_words(text):
            pattern = (
                r'(?<![a-z])'                              # Pas de lettre minuscule avant
                r'('
                    r'[A-ZÉÈÊÎÔÛÀÄËÏÖÜÇ]+'                  # Un mot en majuscules
                    r'(?:'
                        r'(?:\s+(?!:)|\s*(?::)\s*)'         # Séparateur : soit espace(s) (qui ne précède pas directement un ":"), soit espace(s) + ":" + espace(s)
                        r'[A-ZÉÈÊÎÔÛÀÄËÏÖÜÇ]+'              # Un autre mot en majuscules
                    r')*'
                r')'
                r'(?![a-z])'                                # Pas de lettre minuscule après
            )
            words = re.findall(pattern, text)
            return ' '.join(words) if words else text
        
        # Appliquer la fonction à la colonne
        df['Titre'] = df['Titre_nettoye'].apply(extract_uppercase_words)
        df['Titre'] = df['Titre'].str.replace(' VF', '')
        df['Titre'] = df['Titre'].str.replace('EXCLU', '')
        
        
        # Application de la transformation
        df["Titre_key_2"] = (
            df["Titre"]  # Sélectionner la colonne "Titre"
            .apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)  # Appliquer unidecode pour enlever les accents et convertir en minuscule
            .str.replace(r"\s*:\s*.*", "", regex=True)  # Supprimer tout après le premier ":" et ce qui suit
            .str.replace(r"\W+", " ", regex=True)  # Remplacer les caractères spéciaux par des espaces
            .str.replace(r"\s+", "", regex=True)  # Supprimer tous les espaces
            .str.strip()  # Enlever les espaces au début et à la fin
            .str.replace(r"\d+\s*$", "", regex=True)  # Supprimer les numéros à la fin de la chaîne
        )
        
        df['Titre_key_1'] = df['Titre_key_2']+df['Année'].astype(str)
        
        
        df = df[['date_scraping', 'page_token', 'next_page_token', 'Chaine', 'StartDate', 'EndDate', 'Vidéo ID', 'Titre_key_1', 'Titre_key_2', 'Titre_Original', 'Titre', 'Vues', 'Likes']]
        
        
        # On créé les statistiques: 
        if os.path.exists(_0_file_films_youtube) == True:
            
            df_y = pd.read_excel(_0_file_films_youtube)
            
            df_y = df_y[['date_scraping', 'page_token', 'next_page_token', 'Chaine', 'StartDate', 'EndDate', 'Vidéo ID', 'Titre_key_1', 'Titre_key_2', 'Titre_Original', 'Titre', 'Vues', 'Likes']].copy()
            
            df_uniq = df.drop_duplicates(subset=['Chaine', 'Titre_Original', 'EndDate'], keep='first').copy()
    
            df_y = pd.concat([df_y, df_uniq], ignore_index=True)
            df_y = df_y.fillna("")
            df_y = df_y.drop_duplicates(subset=['Chaine', 'EndDate', 'Titre_Original'], keep='last')
            
            # On regroupe les informations des films
            df_agg = df_y.groupby('Titre_key_1').agg(
                Nb_Bandes_annonces=('Titre_key_1', 'count'),
                Moyenne_Vues=('Vues', 'mean'),
                Max_Vues=('Vues', 'max'),
                Max_Likes=('Likes', 'max'),
                Moyenne_Likes=('Likes', 'mean')
            ).reset_index()

            # Fusionner avec le DataFrame original pour avoir ces colonnes en parallèle
            df_y = df_y.merge(df_agg, on='Titre_key_1', how='left')

            shutil.move(_0_file_films_youtube, os.path.join(data_folder, 'Historique/films_youtube'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
            df_y = df_y.sort_values(by=["EndDate", "Vues"], ascending=[True, True])
            
            df_y.to_excel(_0_file_films_youtube, index=False)
            
        else: 
            
            df_uniq = df.drop_duplicates(subset=['Titre_Original', 'EndDate'], keep='first').copy()
            
            # On regroupe les informations des films
            df_agg = df_uniq.groupby('Titre_key_1').agg(
                Nb_Bandes_annonces=('Titre_key_1', 'count'),
                Moyenne_Vues=('Vues', 'mean'),
                Max_Vues=('Vues', 'max'),
                Max_Likes=('Likes', 'max'),
                Moyenne_Likes=('Likes', 'mean')
            ).reset_index()
            
            # Fusionner avec le DataFrame original pour avoir ces colonnes en parallèle
            df = df_uniq.merge(df_agg, on='Titre_key_1', how='left')
            
            df.to_excel(_0_file_films_youtube, index=False)
            
            
        
        # 1.3.4: Exportation Données étape 150:
        logging.info('Exportation Données étape 150')

        if os.path.exists(os.path.join(output_folder_100, 'Films_150.xlsx')) == True:
            shutil.move(os.path.join(output_folder_100, 'Films_150.xlsx'), os.path.join(output_folder_100, r'Historique/Films_150'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        df.to_excel(os.path.join(output_folder_100, 'Films_150.xlsx'), index=False)
        
        


    
    

        
        
        
        
        
        
        
        
        
        
        
        
        

# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 12/03/2025

-------------------------------------------------------------------------------
                    120 Traitement_cine_directors
-------------------------------------------------------------------------------
"""

def etape120():
    
    global scraping_do
    
    
    etape = "120_Traitement_cine_directors"
    
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.2.1: Import des données
    logging.info("1.2.1: Import des données")
    
    df = pd.read_excel(os.path.join(output_folder_100, 'Films_110.xlsx'))
    df_dates = pd.read_excel(_0_file_param_variables, sheet_name=_0_sheet_date_import_cd)
    
    date = last_wednesday()
    date = pd.to_datetime(date)
    
    # Si un scraping a été effectué alors on lance cette étape

    if scraping_do == 1:
        
        print("Scraping effectué: Lancement de l'étape 120")
        
        #Traitement des données
        
        # Titre
        df['Titre'] = df['Titre'].str.replace(r'\s+', ' ', regex=True).str.strip()
        
        def transform_variation(value):
            value = value.strip().lower()  # Supprime les espaces autour et met en minuscule
            if value == "new":
                return 1, np.nan  # 'New' -> new = 1, variation = NaN
            elif value == "-":
                return 0, np.nan  # '-' -> Pas de variation connue
            else:
                try:
                    return 0, float(value.replace('%', '').replace(' ', '').replace(',', '.')) / 100
                except ValueError:
                    return 0, np.nan  # Si une autre erreur survient
    
        # Variation hebdo
        df[['New', 'Variation hebdo']] = df['Variation hebdo'].apply(lambda x: pd.Series(transform_variation(x)))
            
        # Cumul (Millions)
        df['Cumul (Millions)'] = df['Cumul (Millions)'].astype(str).replace(',', '.', regex=True)
        df['Cumul (Millions)'] = df['Cumul (Millions)'].replace(r'[^0-9.]', '', regex=True)
        df['Cumul (Millions)'] = df['Cumul (Millions)'].astype(float)
        df['Cumul'] = df['Cumul (Millions)'] * 1000000
        
        # Budget
        def convert_budget(value):
            value = value.strip().replace(" ", "").lower()  # Supprime les espaces et met en minuscule
            
            if value in ["-m€", "-m$", "-m£", "-"]:
                return 0  # Gère le cas des valeurs manquantes
            
            try:
                num_part = value.replace("m$", "").replace("m€", "").replace("m£", "").replace(",", ".")
                return float(num_part) * 1_000_000  # Convertit en nombre et multiplie par 1M
            except ValueError:
                return np.nan  # Sécurité pour éviter les erreurs si autre chose apparaît
        
        df["Budget"] = df["Budget"].apply(convert_budget)
        
        # Nombre de copies, Moy / Copie
        
        # Convertir les colonnes en chaînes de caractères (si nécessaire)
        df["Nbre de copies"] = df["Nbre de copies"].astype(str).str.replace(" ", "", regex=True)
        df["Nbre de copies"] = df["Nbre de copies"].replace(r'[^0-9.]', '', regex=True)
        df["Moy / Copie"] = df["Moy / Copie"].astype(str).str.replace(" ", "", regex=True)
        df["Moy / Copie"] = df["Moy / Copie"].replace(r'[^0-9.]', '', regex=True)
        
        # Convertir en numérique
        df["Nbre de copies"] = pd.to_numeric(df["Nbre de copies"], errors='coerce')
        df["Moy / Copie"] = pd.to_numeric(df["Moy / Copie"], errors='coerce')
        
        #Variable Date de sortie:
        df.loc[df['New'] == 1, 'Date de sortie'] = df['Date']    
        
        # Variable clé
        df["Titre_key"] = (
            df["Titre"]  # Sélectionner la colonne "Titre"
            .apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)  # Appliquer unidecode pour enlever les accents et convertir en minuscule
            .str.replace(r"\W+", "", regex=True)  # Supprimer tous les caractères spéciaux
        )
        
        # Variable Entrées
        df['Entrées'] = df['Entrées'].astype(str)
        df['Entrées'] = df['Entrées'].str.replace(r'[()-]', '', regex=True)
        
        df['Wiki'] = 0
        
        # Séléction des variables transformés
        
        df = df[['Titre_key', 'Titre', 'Rang', 'New', 'Date', 'Date de sortie', 'Entrées', 'Cumul', 'Variation hebdo', 'Budget', 'Nbre de copies', 'Moy / Copie', 'Lien cd', 'Wiki']]
            
        # Ajout des variables binaires
        
        # 1.1.: Exportation Données étape 120:
        logging.info('Exportation Données étape 120')
        
        # Historisation des données
        if os.path.exists(os.path.join(output_folder_100, 'Films_120.xlsx')) == True:
            shutil.move(os.path.join(output_folder_100, 'Films_120.xlsx'), os.path.join(output_folder_100, r'Historique/Films_120'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        df.to_excel(os.path.join(output_folder_100, 'Films_120.xlsx'), index=False)

        
        # On complète la base de données ciné_directors
        
        df_c = pd.read_excel(_0_file_films_cd)
        
        df_uniq = df.drop_duplicates(subset=['Titre_key', 'Date'], keep='first').copy()
        
        
        if os.path.exists(_0_file_films_cd) == True:
            
            new_df_c = pd.concat([df_c, df_uniq], ignore_index=True)
            
            new_df_c = new_df_c.assign(
                is_boxbis=new_df_c['Lien cd'].str.contains('boxbis', na=False)
            ).sort_values(
                by=['Date', 'Titre_key', 'is_boxbis'],
                ascending=[True, True, True]
            ).drop(columns=['is_boxbis'])  # Supprime la colonne temporaire après tri
                
            new_df_c = new_df_c.assign(
                is_boxbis=new_df_c['Lien cd'].str.contains('boxbis', na=False)
            ).sort_values(
                by=['Date', 'Titre_key', 'is_boxbis'],
                ascending=[True, True, False]  # False pour mettre "boxbis" en premier
            ).drop(columns=['is_boxbis'])  # Supprime la colonne temporaire après tri

            new_df_c = new_df_c.drop_duplicates(subset=['Date', 'Titre_key'], keep='last')
            
            # Identifier les groupes où 'Date' contient au moins une ligne avec "boxbis" et une sans
            mask = new_df_c.groupby('Date')['Lien cd'].transform(lambda x: x.str.contains('boxbis', na=False).any() and not x.str.contains('boxbis', na=False).all())
            
            # Supprimer uniquement les lignes contenant "boxbis" dans ces groupes
            new_df_c = new_df_c[~(mask & new_df_c['Lien cd'].str.contains('boxbis', na=False))]
            

            # Maintenant on vérifie que le site a bien été mis à jour
            
            if len(df_uniq[df_uniq['Date'] == date]) > 0:
                
                date_m1 = date - timedelta(days=7)
                
                df_c_date = new_df_c[(new_df_c['Date'] == date) & (new_df_c['New'] == 1)]
                df_c_date_m1 = new_df_c[(new_df_c['Date'] == date_m1) & (new_df_c['New'] == 1)]
            
                # Fusionner les deux DataFrames sur 'Titre_key' et 'New'
                df_common = df_c_date.merge(df_c_date_m1, on=['Titre_key', 'New'], how='inner')

                if len(df_common) > 0:
                    
                    print("Le site n'a pas été mis à jour")
                    
                    new_df_c = new_df_c[new_df_c['Date'] != date]
                    
                    
            shutil.move(_0_file_films_cd, os.path.join(data_folder, 'Historique/films_cine_directors'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
            new_df_c = new_df_c.sort_values(by=["Date", "Titre_key"], ascending=[True, True])
            new_df_c.to_excel(_0_file_films_cd, index=False)
  
        
        else:
            
            df.to_excel(_0_file_films_cd)
            
            
    else:
        
        print('Pas de scraping effectué')

    
    
    
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
    
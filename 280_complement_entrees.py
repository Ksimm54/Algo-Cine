# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 04/04/2025

-------------------------------------------------------------------------------
                    280 Complement Entrées
-------------------------------------------------------------------------------
"""

def etape280():
    
    
    etape = "280_complement_entrees"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.8.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.8.1: Importation Données")
    
    df = pd.read_excel(_0_file_films)
    df_cd = pd.read_excel(_0_file_films_cd)
    
    
    # 2.8.2: Mise à jour des données avec le nombre d'entrées mis à jour
    
    df_na_entrees = df[df['Entrées'].isna()]
    
    
    if len(df_na_entrees) > 0:
            
        df_cd = df_cd[['Titre_key', 'Date', 'Entrées']].copy()
        df_cd.rename(columns = {'Date':'Date de sortie'}, inplace=True)
        
        new_df = df_na_entrees.merge(df_cd, on=['Titre_key', 'Date de sortie'], how='left')
        
        new_df["Entrées"] = new_df["Entrées_y"].fillna(new_df["Entrées_x"])
        
        new_df.drop(['Entrées_x', 'Entrées_y'], axis=1, inplace=True)
        
        
        # 2.8.3: Ajout des données dans films
        
        new_df = pd.concat([df, new_df], ignore_index=True)
        
        # Trier le DataFrame pour que les NaN dans 'Entrées' soient en dernier
        new_df = new_df.sort_values(by=['Titre_key', 'Date de sortie', 'Entrées'], ascending=[True, True, False])
        
        # Supprimer les doublons en gardant la première occurrence
        new_df = new_df.drop_duplicates(subset=['Titre_key', 'Date de sortie'], keep='first')
        
        new_df = new_df.sort_values(by=['Date de sortie', 'Titre_key'], ascending = [True, True])
        
        
        # 2.8.4: Export des données
        
        shutil.move(_0_file_films, os.path.join(data_folder, 'Historique/Films'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        new_df.to_excel(_0_file_films, index=False)
    
        print("Nombre d'entrées mis à jour")
        
    else:
        
        print("Données déjà complètent")
    
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
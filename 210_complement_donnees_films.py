# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 15/01/2025

-------------------------------------------------------------------------------
                    210 Ajouter des films aux données
-------------------------------------------------------------------------------
"""


def etape210():

    
    etape = "210_complement_donnees"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    
    # 2.1.1 Import des données: 
    logger.info("Import des données")
    print('Import des données')
    
    df = pd.read_excel(_0_file_films)
    df_real = pd.read_excel(_0_file_realisateurs)
    df_act = pd.read_excel(_0_file_acteurs)
        
    
    # 2.1.2 Import des données à ajouter
    
    if os.path.exists(_0_file_films_to_ad) == False:
       
        logger.info('Pas de nouvelles données à importer')
        print('Pas de nouvelles données à importer')
       
    else:
        
        logger.info("Import des données à ajouter")
        
        df_to_add = pd.read_excel(_0_file_films_to_ad)
        
        
        # 2.1.3 : On garde les lignes qui sont complètes et on les ajoute aux données, le reste est à compléter
        
        # Colonnes à ignorer dans la vérification des valeurs manquantes
        ignore_columns = ['Entrées', 'Budget']
        
        # Identifier les colonnes à vérifier pour les valeurs manquantes
        columns_to_check = [col for col in df_to_add.columns if col not in ignore_columns]
        
        # Lignes avec des valeurs manquantes (hors des colonnes ignorées)
        df_to_complete = df_to_add[(df_to_add[columns_to_check].isnull().any(axis=1)) 
                                   | (df_to_add[columns_to_check].isna().any(axis=1)) ]
        
        # Lignes complètes (hors des colonnes ignorées)
        df_to_add_full = df_to_add[(~df_to_add[columns_to_check].isnull().any(axis=1)) 
                                   | (~df_to_add[columns_to_check].isna().any(axis=1))]
        
        # Si le fichier 'films_a_completes.xlsx' existe alors on s'arrête on a déjà des données à corriger
        if os.path.exists(os.path.join(to_complete_folder, 'films_a_completes.xlsx')):
            
            logger.info("Il y a déjà des données à corriger")
            print('Déjà des données à corriger')
            
            # Arret du programme car des données sont à compléter
            
            # ---------- FIN DU JOURNAL
            logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
            print("Exécution du programme terminée car besoin d'intervention manuelle.")
            logging.shutdown()
            # ----------
            
            sys.exit()
                
        else: 
        
            # Sinon on historise les données qu'on a ajouté
            shutil.move(os.path.join(_0_file_films_to_ad), os.path.join(input_folder, 'Historique/films_to_ad'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        
            if len(df_to_complete) > 0:
                
                # On vérifie que les films à compléter ne sont pas déjà dans les données de départ
                
                df_vma_check = pd.concat([df, df_to_complete], axis=0).reset_index(drop=True)
                df_vma_check.drop_duplicates(subset='Titre_key', keep='first', inplace=True)
                
                if len(df_vma_check) == len(df):
                    
                    logger.info("Pas de nouveaux films à ajouter")
                    print('Pas de nouveaux films à ajouter')
                    
                else: 
                
                    logger.info("Des données sont à corriger")
                    print('Des données sont à corriger')
                    
                    os.makedirs(to_complete_folder, exist_ok=True)
                    
                    df_to_complete.to_excel(_0_file_to_complete, index=False)
                    
                    # On ajoute un filtre sur les cellules avec des valeurs manquantes
                    
                    wb = load_workbook(_0_file_to_complete)
                    ws = wb.active  # Sélectionne la feuille active
                    
                    # Style pour le fond jaune
                    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
                    
                    # Appliquer le style aux cellules contenant des valeurs manquantes
                    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                        for cell in row:
                            if cell.value is None:  # Si la cellule contient une valeur manquante
                                cell.fill = yellow_fill
                    
                    # Enregistrer le fichier avec le style appliqué
                    wb.save(_0_file_to_complete) 
                
                
            if len(df_to_add_full) > 0:
                
                
                # On vérifie qu'il n'y a pas de doublons    
                new_df = pd.concat([df, df_to_add_full], axis=0).reset_index(drop=True)
                new_df.drop_duplicates(subset='Titre_key', keep='first', inplace=True)
                
                if len(new_df) == len(df):
                    
                    logger.info("Pas de nouveaux films à ajouter")
                    print('Pas de nouveaux films à ajouter')
                    
                else:
                    
                    logger.info('Des nouvelles données ont été ajoutées')
                    print('Des nouvelles données ont été ajoutées')
                
                    # On historise l'ancien fichier
                    logger.info("Ancien fichier historisé: Films"+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx')
                    shutil.move(_0_file_films, os.path.join(data_folder, 'Historique/Films'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        
                    # On créé le nouveau
                    logger.info("Nouveau fichier créé: Films.xlsx")
                    new_df = new_df.sort_values(by = ['Date de sortie', 'Budget'], ascending = [True, False])
                    new_df.to_excel(_0_file_films, index=False)
        
       
        
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------






















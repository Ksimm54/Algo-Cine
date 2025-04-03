# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:00:27 2025

@author: User
"""

"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 15/01/2025

-------------------------------------------------------------------------------
                    220 Données réals/acteurs à compléter
-------------------------------------------------------------------------------
"""


def etape220():
    
    etape = "220_reals_acts_check"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.2.1: Importation des données créées dans l'étape 210
    logger.info("2.2.1: Importation des données créées dans l'étape 210")
    
    df = pd.read_excel(_0_file_films)
    df_real = pd.read_excel(_0_file_realisateurs)
    df_act = pd.read_excel(_0_file_acteurs)
    
    
    
    
    # 2.2.2: On vérifie qu'il n'y a pas déjà des données à corriger Réalisateurs
    logger.info("2.2.2: Check si des données ne sont pas à corriger Réalisateurs")
    
    real_vma = df_real[df_real.isna().any(axis=1)]
    
    # Variable binaire pour arrêter le programme si besoin
    to_stop=0
    
    
    if len(real_vma) > 0:
        
        logger.warning('Les données sont déjà incomplètes')
        logger.warning('\n')
        logger.warning("Compléter les données avant de faire l'étape 220")
        print('Les données sont déjà incomplètes')
        print('\n')
        print("Compléter les données avant de faire l'étape 220")
        
        # On arrête le programme car besoin d'intervention manuelle
        to_stop=1
        
    else:
        
        # 1.2.3 Vérification Réalisateurs
        logger.info("Données complètes")
        
        real_init = df['Réalisateur']
        real_init = real_init.unique()
        real_init = sorted(real_init)
        df_real_init = pd.DataFrame(real_init, columns=['Réalisateur'], index=None)
        
        real = df_real['Réalisateur']
        real = real.unique()
        real = sorted(real)
        df_real_check = pd.DataFrame(real, columns=['Réalisateur'], index=None)
        
        df_real_ajout = df_real_init[~df_real_init.isin(df_real_check.to_dict(orient='list')).all(axis=1)].copy()
        
        if len(df_real_ajout) != 0:
            
            logger.warning("Nouveaux réalisateurs à catégoriser !")
            print("Nouveaux réalisateurs à catégoriser !")
            print("\n")
            print("Catégorie de réalisateur:")
            print("- 1 : Inconnu")
            print("- 2 : Réalisateur")
            print("- 3 : Star")
            print("- 4 : Superstar")
            
            df_real_ajout.loc[:,'Catégorie réalisateur'] = ''
            
            for index, row in df_real_ajout.iterrows():
                categorie = float(input(f"Entrez la catégorie pour le réalisateur '{row['Réalisateur']}': "))
                df_real_ajout.at[index, 'Catégorie réalisateur'] = categorie  # Mettre à jour la catégorie

            df_real = pd.concat([df_real, df_real_ajout], axis=0)
            
            # On historise les anciennes données avant de créer les nouvelles
            
            shutil.move(_0_file_realisateurs, os.path.join(data_folder, 'Historique/Réalisateurs'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
            
            # On exporte les données de réalisateurs
            
            df_real = df_real.sort_values(by="Réalisateur", ascending=True)
            df_real.to_excel(_0_file_realisateurs, index=False)
            
        else:  
            
            logger.info("Pas de nouveaux réalisateurs à catégoriser")
            print("Pas de nouveaux réalisateurs à catégoriser")
    
 
    
    # 2.2.3: On vérifie qu'il n'y a pas déjà des données à corriger
    logger.info("2.2.3: Check si des données ne sont pas à corriger")
    
    act_vma = df_act[df_act.isna().any(axis=1)]
    
    
    if len(act_vma) > 0:
        
        logger.warning('Les données sont déjà incomplètes')
        logger.warning('\n')
        logger.warning("Compléter les données avant de faire l'étape 230")
        print('Les données sont déjà incomplètes')
        print('\n')
        print("Compléter les données avant de faire l'étape 230")
        
        # On arrête le programme car besoin d'intervention manuelle
        to_stop=1
        
    else:
        
        # 2.2.4 Vérification Acteurs
        logger.info("Données complètes")
        
        act_init = pd.concat([df['Acteur Principal'], df['Acteur Secondaire']])
        act_init = act_init.unique()
        act_init = sorted(act_init)
        df_act_init = pd.DataFrame(act_init, columns=['Acteur'], index=None)
        
        act = df_act['Acteur']
        act = act.unique()
        act = sorted(act)
        df_act_check = pd.DataFrame(act, columns=['Acteur'], index=None)
        
        df_act_ajout = df_act_init[~df_act_init.isin(df_act_check.to_dict(orient='list')).all(axis=1)].copy()
        
        if len(df_act_ajout) != 0:
            
            logger.warning("Nouveaux acteurs à catégoriser !")
            print("Nouveaux acteurs à catégoriser !")
            print("\n")
            print("Catégorie d'acteurs:")
            print("- 1 : Inconnu")
            print("- 2 : Acteur")
            print("- 3 : Star")
            print("- 4 : Superstar")
            
            df_act_ajout.loc[:,"Catégorie d'acteur"] = ''
            
            for index, row in df_act_ajout.iterrows():
                categorie = float(input(f"Entrez la catégorie pour l'acteur '{row['Acteur']}': "))
                df_act_ajout.at[index, "Catégorie d'acteur"] = categorie  # Mettre à jour la catégorie
            
            df_act = pd.concat([df_act, df_act_ajout], axis=0)
            
            # On historise les anciennes données avant de créer les nouvelles
            
            shutil.move(_0_file_acteurs, os.path.join(data_folder, 'Historique/Acteurs'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
            
            # On exporte les données d'acteurs'
            
            df_act = df_act.sort_values(by="Acteur", ascending=True)
            df_act.to_excel(_0_file_acteurs, index=False)
            
            
        else:  
            
            logger.info("Pas de nouveaux acteurs à catégoriser")
            print("Pas de nouveaux acteurs à catégoriser")
    
  
    if to_stop == 1: 
        
        # ---------- FIN DU JOURNAL
        logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
        logging.shutdown()
        # ----------
        
        sys.exit()
    
    

    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------



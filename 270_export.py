# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 10:07:37 2025

@author: User
"""

# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/01/2025

-------------------------------------------------------------------------------
                    270 Export
-------------------------------------------------------------------------------
"""

def etape270():
    
    
    etape = "270_date_infos"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.7.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.7.1: Importation Données")
    
    df = pd.read_excel(os.path.join(output_folder_200, 'Films_260.xlsx'))
    df_real = pd.read_excel(_0_file_realisateurs)
    df_act = pd.read_excel(_0_file_acteurs)
    df_date = pd.read_excel(_0_file_param_variables, sheet_name=_0_sheet_date_to_pred)
    logging.info('Données importées')


    # 2.7.2: Définition des environnements de TRAIN, TEST, VALIDATION:
    logging.info("2.7.2: Définition des environnements de TRAIN, TEST, VALIDATION:")    
    
    if not df_date.empty and pd.notna(df_date.iloc[0, 0]):
        
        max_train_date = '2024-11-01'
        max_valid_date = df_date.iloc[0,0]
        
        print("1 semaine avant les données de TEST :"+str(max_valid_date)) 

        df.loc[df['Date de sortie'] <= max_train_date, 'Data'] = 'Train'
        df.loc[(df['Date de sortie'] >= max_train_date) & (df['Date de sortie'] < max_valid_date), 'Data'] = 'Valid'
        df.loc[df['Date de sortie'] >= max_valid_date, 'Data'] = 'Test'        
        
    else:    
            
        today = datetime.today()

        # Vérifie si aujourd'hui est mercredi (2 = mercredi car lundi = 0)
        if today.weekday() == 2:
            dernier_mercredi = today
        else:
            dernier_mercredi = today - timedelta(days=(today.weekday() - 2) % 7)
            
        max_train_date = dernier_mercredi - relativedelta(months=3)
        max_valid_date = dernier_mercredi.strftime("%Y-%m-%d")
        
        print("1 semaine avant les données de TEST :"+str(max_valid_date)) 

        df.loc[df['Date de sortie'] <= max_train_date, 'Data'] = 'Train'
        df.loc[(df['Date de sortie'] >= max_train_date) & (df['Date de sortie'] < max_valid_date), 'Data'] = 'Valid'
        df.loc[df['Date de sortie'] >= max_valid_date, 'Data'] = 'Test'


    # 2.7.3: Export des données transformées
    logging.info("2.7.3: Export des données: df -> Films_270.xlsx")
    print('Export des données: df -> Films_270.xlsx')
    
    
    df.to_excel(os.path.join(output_folder_200, 'Films_270.xlsx'), index=False)
    
    count_train = df[df['Data'] == 'Train'].shape[0]
    count_valid = df[df['Data'] == 'Valid'].shape[0]
    count_test  = df[df['Data'] == 'Test' ].shape[0]
    percent_train = round((count_train / (count_train + count_valid + count_test))*100, 0)
    percent_valid = round((count_valid / (count_train + count_valid + count_test))*100, 0)
    percent_test = round((count_test / (count_train + count_valid + count_test))*100, 0)
    
    print('')
    print(f"Periode du jeu TRAIN:  - {max_train_date}")
    print(f"Periode du jeu VALID:  {max_train_date} - {max_valid_date}")
    print(f"Periode du jeu TEST:  {max_valid_date} - ")
    print('')
    print(f"Nombre de lignes dans le jeu TRAIN: {count_train}          ({percent_train}%)")
    print(f"Nombre de lignes dans le jeu VALID: {count_valid}          ({percent_valid}%)")
    print(f"Nombre de lignes dans le jeu TEST: {count_test}          ({percent_test}%)")
    
    logger.info('')
    logger.info(f"Periode du jeu TRAIN:  - {max_train_date}")
    logger.info(f"Periode du jeu VALID:  {max_train_date} - {max_valid_date}")
    logger.info(f"Periode du jeu TEST:  {max_valid_date} - ")
    logger.info('')
    logger.info(f"Nombre de lignes dans le jeu TRAIN: {count_train}          ({percent_train}%)")
    logger.info(f"Nombre de lignes dans le jeu VALID: {count_valid}          ({percent_valid}%)")
    logger.info(f"Nombre de lignes dans le jeu TEST: {count_test}          ({percent_test})%")   


    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
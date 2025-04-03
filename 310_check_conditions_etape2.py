# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/01/2024

-------------------------------------------------------------------------------
                    310 Check conditions étape 2
-------------------------------------------------------------------------------
"""

def etape310():

    etape = "310_check_conditions_etape2"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------


    # 3.1.1: Import des données
    # On va chercher les données de l'étape 2
    logger.info("3.1.1: Vérification de l'existence des données de l'étape 2")
    
    
    # Si le fichier 'Films_270.xlsx' existe alors on peut faire l'analyse
    if os.path.exists(os.path.join(output_folder_200, 'Films_270.xlsx')) == False:
        
        logger.critical("Le fichier de films n'existe pas")
        logger.critical("Faire tourner l'étape 2 avant de lancer l'analyse")
        print("Faire tourner l'étape 2 avant de lancer l'analyse")
        
        # ---------- FIN DU JOURNAL
        logging.info("Exécution du programme terminée.")
        logging.shutdown()
        # ----------
        
        sys.exit()
    
    else: 
        
        logger.info("Etape 2 a fonctionné correctement")
        
        df = pd.read_excel(output_folder_200+r"/Films_270.xlsx")
        
        df_manquantes = df[df['Entrées'].isna() & (df['Data'] != 'Test')]
        
        if len(df_manquantes) == 0:
        
            logger.info("Début de l'étape 3")
            print("Conditions réunis pour démarrer l'analyse")
            
            # On historise les analyses: 
                
            # Données de l'étape 3:
            if os.path.exists(os.path.join(output_folder_300, 'Films_320.xlsx')) == True:
                shutil.move(os.path.join(output_folder_300, 'Films_320.xlsx'), os.path.join(output_folder_300, 'Historique/Films_320'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
            # Analyses :
            if os.path.exists(os.path.join(output_folder_300, 'Analyses_variables_qualitatives_PDF.pdf')) == True:            
                shutil.move(os.path.join(output_folder_300, 'Analyses_variables_qualitatives_PDF.pdf'), os.path.join(output_folder_300, 'Historique/Analyses_variables_qualitatives_PDF'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.pdf'))
            if os.path.exists(os.path.join(output_folder_300, 'Analyses_variables_quantitatives_PDF.pdf')) == True:    
                shutil.move(os.path.join(output_folder_300, 'Analyses_variables_quantitatives_PDF.pdf'), os.path.join(output_folder_300, 'Historique/Analyses_variables_quantitatives_PDF'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.pdf'))
        
        
        else: 
            
            print(df_manquantes)
                
            logger.info("Conditions non réunis pour démarrer l'étape 3")
            print("Conditions non réunis pour démarrer l'étape 3")
            logger.info("Il manque des informations sur la variable explicative")
            print("Il manque des informations sur la variable explicative")
            logger.critical("Intervention manuelle nécessaire")
            print("Intervention manuelle nécessaire")
            
            # ---------- FIN DU JOURNAL
            logging.info("Exécution du programme terminée.")
            logging.shutdown()
            # ----------
            
            sys.exit()
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    

































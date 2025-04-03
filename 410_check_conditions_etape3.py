# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 20/01/2024

-------------------------------------------------------------------------------
                    410 Check conditions étape 3
-------------------------------------------------------------------------------
"""

def etape410():

    etape = "410_check_conditions_etape3"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------


    # 4.1.1: Import des données
    # On va chercher les données de l'étape 3
    logger.info("4.1.1: Vérification de l'existence des données de l'étape 3")
    
    
    # Si le fichier 'Films_320.xlsx' existe alors on peut faire l'analyse
    if os.path.exists(os.path.join(output_folder_300, 'Films_320.xlsx')) == False:
        
        logger.critical("Le fichier de films n'existe pas")
        logger.critical("Faire tourner l'étape 3 avant de lancer l'analyse")
        print("Faire tourner l'étape 3 avant de lancer l'analyse")
        
        # ---------- FIN DU JOURNAL
        logging.info("Exécution du programme terminée.")
        logging.shutdown()
        # ----------
        
        sys.exit()
    
    else: 
        
        logger.info("Etape 3 a fonctionné correctement")
        logger.info("Début de l'étape 4")
        print("Conditions réunis pour démarrer l'analyse")
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    

































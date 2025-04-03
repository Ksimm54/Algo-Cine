# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 20/01/2025

-------------------------------------------------------------------------------
                    250 Valeurs manquantes
-------------------------------------------------------------------------------
"""

def etape250():
    
    etape = "250_valeurs_manquantes"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.5.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.5.1: Importation Données")
    
    df = pd.read_excel(os.path.join(output_folder_200, 'Films_230.xlsx'))
    logging.info('Données importées')
    
    
    # Valeurs manquantes pour BUDGET
    
    # TEMPORAIRE : AJOUTER UNE ETAPE QUI REMPLACE LES VALEURS MANQUANTES DE BUDGET-----
    df['Budget'] = df['Budget'].fillna(4000000)
    # TEMPORAIRE ----------------------------------------------------------------------
    
    # TEMPORAIRE : AJOUTER UNE ETAPE QUI REMPLACE LES VALEURS MANQUANTES DE BUDGET-----
    df['Nbre de copies'] = df['Nbre de copies'].fillna(50)
    # TEMPORAIRE ----------------------------------------------------------------------
    
    
    
    # Valeurs manquantes pour NOTE PRESSE ALLOCINE
    
    
    # 2.3.8: Exportation Données étape 250:
    logging.info('Exportation Données étape 250')
    
    df.to_excel(os.path.join(output_folder_200, 'Films_250.xlsx'), index=False)
    
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
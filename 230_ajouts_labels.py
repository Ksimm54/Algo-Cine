# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 20:34:35 2025

@author: User
"""

"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 16/01/2025

-------------------------------------------------------------------------------
                    230 Ajout des labels
-------------------------------------------------------------------------------
"""

def etape230():
    
    etape = "230_ajouts_labels"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.3.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.3.1: Importation Données")
    df = pd.read_excel(_0_file_films)
    df_real = pd.read_excel(_0_file_realisateurs)
    df_act = pd.read_excel(_0_file_acteurs)
    logging.info('Données importées')
    
    
    # 2.3.2: Importation des données de labels
    logging.info("2.3.2: Importation Labels")
    
    df_real_lbl = pd.read_excel(_0_file_labels, sheet_name=_0_sheet_realisateurs)
    df_act_lbl = pd.read_excel(_0_file_labels, sheet_name=_0_sheet_acteurs)
    
    
    # 2.3.3: Labels Réalisateurs
    logging.info("2.3.3: Labels Réalisateurs")
    
    df = pd.merge(df, df_real, how='left', on='Réalisateur')
    df = pd.merge(df, df_real_lbl, how='left', on='Catégorie réalisateur')   
    
    
    # 2.3.4: Labels Acteurs
    logging.info("2.3.3: Labels Acteurs")
    
    df.rename(columns={'Acteur Principal': 'Acteur'}, inplace=True)
    df = pd.merge(df, df_act, how='left', on='Acteur')
    df = pd.merge(df, df_act_lbl, how='left', on="Catégorie d'acteur")
    df.rename(columns={'Acteur': 'Acteur Principal'}, inplace=True)
    df.rename(columns={"Catégorie d'acteur": "Catégorie d'acteur principal"}, inplace=True)
    df.rename(columns={"Label acteur": "Label acteur principal"}, inplace=True)
    
    
    df.rename(columns={'Acteur Secondaire': 'Acteur'}, inplace=True)
    df = pd.merge(df, df_act, how='left', on='Acteur')
    df = pd.merge(df, df_act_lbl, how='left', on="Catégorie d'acteur")
    df.rename(columns={'Acteur': 'Acteur Secondaire'}, inplace=True)
    df.rename(columns={"Catégorie d'acteur": "Catégorie d'acteur secondaire"}, inplace=True)
    df.rename(columns={"Label acteur": "Label acteur secondaire"}, inplace=True)
    
    

    # 2.3.8: Exportation Données étape 230:
    logging.info('Exportation Données étape 230')
    
    df.to_excel(os.path.join(output_folder_200, 'Films_230.xlsx'), index=False)
        
    
    logger.info('Labels ajoutés')
    print('Labels ajoutés')
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------

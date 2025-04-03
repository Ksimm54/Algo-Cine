# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 07/02/2025

-------------------------------------------------------------------------------
                    470 Historisation des résultats
-------------------------------------------------------------------------------
"""

def etape470():

    etape = "470_hist_preds"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    


    # Import des données
    # On va chercher les données de l'étape 4.1 et les données d'historique
    logger.info("Importation des données de l'étape 4.1")
    
    # Récupérer l'heure actuelle
    now = datetime.now()
    
    def ml_hist(model, Model):
        
        df_to_ad = pd.read_excel(output_folder_400+r"/"+model+"_Films_pred.xlsx")
        df_pred = pd.read_excel(output_folder_400+r"/Films_predictions_hist.xlsx")
        df = pd.read_excel(_0_file_films)
        
        # On historise les données
        df_to_ad.to_excel(os.path.join(output_folder_400, f'Historique/'+model+f'_Films_pred_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}.xlsx'), index=False)
        
        # On récupère des infos avant d'ajouter les prédictions
        df_to_ad['Modèle'] = Model
        df_to_ad['Date'] = now
        df_to_ad['Entrées'] = ''
        df_to_ad = df_to_ad.merge(df[['Titre', 'Date de sortie']], on='Titre', how='left')
        
        df_to_ad = df_to_ad[["Date de sortie", 
                             "Titre", 
                             "Modèle", 
                             "Date", 
                             "Prédiction", 
                             "Entrées", 
                             'Train R²', 
                             'Train MAE',
                             'Train RMSE',
                             'Valid R²',
                             'Valid MAE',
                             'Valid RMSE'
                             ]]
        
        df_pred = pd.concat([df_pred, df_to_ad], ignore_index=True)
        
        # On complète avec les vrais données des semaines précédentes
        
        df_pred = df_pred.drop('Entrées', axis=1)
        
        df_pred = df_pred.merge(df[['Titre', 'Entrées']], on='Titre', how='left')
        
        df_pred.to_excel(os.path.join(output_folder_400, f'Films_predictions_hist.xlsx'), index=False)
        
    
    ml_hist('RF', 'Random Forest')
    ml_hist('regressionLasso', 'Regression Lasso')
    ml_hist('regressionRidge', 'Regression Ridge')
    ml_hist('elasticNet', 'Elastic Net')
    ml_hist('reseauNeurones', 'Reseau de Neurones')
    
    
    # On garde la dernière prédiction pour chaque modèle et film
    
    df_pred = pd.read_excel(output_folder_400+r"/Films_predictions_hist.xlsx")
    
    df_pred_uniq = df_pred.loc[df_pred.groupby(['Titre', 'Modèle'])['Date'].idxmax()]
    df_pred_uniq = df_pred_uniq.sort_values(by=['Date de sortie', 'Titre', 'Modèle'], ascending=[False, True, True])
    
    df_pred_uniq.to_excel(os.path.join(output_folder_400, f'Films_predictions.xlsx'), index=False)
    
    largeur_colonne(os.path.join(output_folder_400, f'Films_predictions.xlsx'), 30)
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
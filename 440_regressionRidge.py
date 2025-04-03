# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 09/02/2025

-------------------------------------------------------------------------------
                    440 Régression Ridge
-------------------------------------------------------------------------------
"""

def etape440():

    etape = "440_regressionRidge"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------

    # Import des données
    # On va chercher les données de l'étape 3.2
    logger.info("Importation des données de l'étape 3.2")
    
    df = pd.read_excel(output_folder_300+r"/Films_320.xlsx")
    
    # On transforme les variables catégorielles en variables binaires
    
    vars_qual = df.select_dtypes(exclude=['number']).columns.to_list()
    vars_qual.remove('Titre')
    vars_qual.remove('Data')
    
    var_cible = 'Entrées'
    
    var_data = 'Data'
    
    var_id = 'Titre'
    
    
    df_encoded = pd.get_dummies(df, columns = vars_qual)
    
    
    train = df_encoded[df_encoded["Data"] == "Train"].copy()
    valid = df_encoded[df_encoded["Data"] == "Valid"].copy()
    test = df_encoded[df_encoded["Data"] == "Test"].copy()
    
        
    # Définir les colonnes des features et la cible
    features = [col for col in train.columns if col not in [var_cible, var_id, var_data]]
    X_train, y_train = train[features], train[var_cible]
    X_test, y_test = test[features], test[var_cible]
    X_val, y_val = valid[features], valid[var_cible]
    
    
    # Définition et entraînement du modèle Ridge
    alpha = 1.0  # Paramètre de régularisation à ajuster
    ridge = Ridge(alpha=alpha, random_state=123)
    ridge.fit(X_train, y_train)
    
    # Prédictions
    y_train_pred = np.round(ridge.predict(X_train)).astype(int)
    y_val_pred = np.round(ridge.predict(X_val)).astype(int)
    y_test_pred = np.round(ridge.predict(X_test)).astype(int)
    
    
    films_pred = test[["Titre"]].reset_index(drop=True)
    films_pred = pd.concat([films_pred, pd.DataFrame(y_test_pred, columns=['Prédiction'])], axis=1)
    
    
    # --- Calcul des métriques de performance ---
    
    eval_model(y_train, y_train_pred, "Train")
    
    films_pred['Train R²'] = round(r2, 2)
    films_pred['Train MAE'] = round(mae)
    films_pred['Train RMSE'] = round(rmse)
       
    eval_model(y_val, y_val_pred, "Validation")
    
    films_pred['Valid R²'] = round(r2, 2)
    films_pred['Valid MAE'] = round(mae)
    films_pred['Valid RMSE'] = round(rmse)
    

    # Export des résultats:    
    films_pred.to_excel(os.path.join(output_folder_400, 'regressionRidge_Films_pred.xlsx'), index=False)
    
    
    # Affichage des coefficients
    coef_df = pd.DataFrame({'Feature': features, 'Coefficient': ridge.coef_})
    coef_df = coef_df.sort_values(by="Coefficient", key=abs, ascending=False)
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ---------- 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

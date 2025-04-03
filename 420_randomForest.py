# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 20/01/2025

-------------------------------------------------------------------------------
                    420 Random Forest
-------------------------------------------------------------------------------
"""

def etape420():

    etape = "420_randomForest"
    
    
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
  
    
    # Créer un modèle Random Forest Regressor
    #rf = RandomForestRegressor(random_state=123, n_estimators=100, max_depth=10)
    
    rf = RandomForestRegressor(
        random_state=123,
        n_estimators=160,
        max_depth=10,
        max_features=6,
        min_samples_leaf=5,
        max_samples=0.5,  # 50% de l'échantillon utilisé par arbre
        #bootstrap=False   # Échantillonnage sans remplacement
    )
    
    # Entraîner le modèle sur les données d'entraînement
    rf.fit(X_train, y_train)
    
    # Faire des prédictions sur les ensembles de test et validation
    y_pred_train = np.round(rf.predict(X_train)).astype(int)
    y_pred_test = np.round(rf.predict(X_test)).astype(int)
    y_pred_val = np.round(rf.predict(X_val)).astype(int)
    
    
    films_pred = test[["Titre"]].reset_index(drop=True)
    films_pred = pd.concat([films_pred, pd.DataFrame(y_pred_test, columns=['Prédiction'])], axis=1)
    
        
    # --- Calcul des métriques de performance ---
    
    eval_model(y_train, y_pred_train, "Train")
    
    films_pred['Train R²'] = round(r2,2)
    films_pred['Train MAE'] = round(mae)
    films_pred['Train RMSE'] = round(rmse)
       
    eval_model(y_val, y_pred_val, "Validation")
    
    films_pred['Valid R²'] = round(r2, 2)
    films_pred['Valid MAE'] = round(mae)
    films_pred['Valid RMSE'] = round(rmse)
    
    # Export des résultats:
        
    films_pred.to_excel(os.path.join(output_folder_400, 'RF_Films_pred.xlsx'), index=False)
    
    
    
    # --- Visualisation des résultats ---
    
    # Comparaison des valeurs réelles et prédites pour le validation set
    # plt.subplot(1, 2, 2)
    # plt.scatter(y_val, y_pred_val, alpha=0.5)
    # plt.plot([min(y_val), max(y_val)], [min(y_val), max(y_val)], 'r--', lw=2)
    # plt.title("Prédictions vs Réelles (Validation)")
    # plt.xlabel("Valeurs réelles")
    # plt.ylabel("Valeurs prédites")
    
    # plt.tight_layout()
    # plt.show()
    
    # # Distribution des erreurs de prédiction pour validation set
    # plt.figure(figsize=(14, 7))
    
    # # Erreurs de prédiction sur le validation set
    # plt.subplot(1, 2, 2)
    # errors_val = y_pred_val - y_val
    # sns.histplot(errors_val, kde=True, color='orange')
    # plt.title("Distribution des erreurs de prédiction (Validation Set)")
    # plt.xlabel("Erreur de prédiction")
    # plt.ylabel("Fréquence")
    
    # plt.tight_layout()
    # plt.show()


    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
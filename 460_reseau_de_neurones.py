# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 09/02/2025

-------------------------------------------------------------------------------
                    460 Réseau de neurones
-------------------------------------------------------------------------------
"""

def etape460():

    etape = "460_reseau_de_neurones"
    
    
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
    
    
    # Standardisation des données (important pour les réseaux de neurones)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Définition du modèle
    model = Sequential([
        Input(shape=(X_train.shape[1],)),  
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    
    # Compilation du modèle
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    
    # Entraînement du modèle
    history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_data=(X_val_scaled, y_val), verbose=1)
    
    # Prédictions
    y_train_pred = np.round(model.predict(X_train_scaled).flatten()).astype(int)
    y_val_pred = np.round(model.predict(X_val_scaled).flatten()).astype(int)
    y_test_pred = np.round(model.predict(X_test_scaled).flatten()).astype(int)


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
    films_pred.to_excel(os.path.join(output_folder_400, 'reseauNeurones_Films_pred.xlsx'), index=False)
    

    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------











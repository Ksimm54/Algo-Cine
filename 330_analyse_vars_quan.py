# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/01/2025

-------------------------------------------------------------------------------
                    330 Analyse des variables quantitatives
-------------------------------------------------------------------------------
"""

def etape330():

    etape = "330_analyse_vars_quan"
    
    # A AJOUTER --------------
    # On fait tourner un modèle de regression linéaire pour analyser les variables
    # Il faut en faire tourner un deuxieme pour supprimer les variables qui ne sont pas significatives dans le premier
    # Donc ajouter une boucle
    #
    # Ajouter une étape de normalisation des données
    #
    # ------------------------
    
    
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
    df_param_variable = pd.read_excel(data_folder+"/param_variables.xlsx")
    
    # 3 ANALYSE
    logging.info("330_analyse_vars_quan")

    
    # 3.3.1: Définition de la table à analyser
    
    # On ne peut pas analyser les données test
    df_analyse = df[df['Data'] != 'Test'].copy()
    
    # Variables explicatives quantitatives:
    vars_quan = ['Durée',
                 'Budget',
                 'Nb entrées semaine année précédente',
                 'Nbre de copies',
                 'Likes', 
                 'Vues', 
                 'Nb_Bandes_annonces', 
                 'Moyenne_Vues', 
                 'Max_Vues', 
                 'Max_Likes', 
                 'Moyenne_Likes'
                 ]
    
    var_cible = 'Entrées'
    
    var_id = 'Titre'

    var_data = 'Data'
    
    global alpha, scatterplot_list, pearson_list, spearman_list, pearson_pvalue_list, spearman_pvalue_list, decision_pearson_list, decision_spearman_list, seuil_r, reg_lin_list             
    
    scatterplot_list = []
    pearson_list = []
    spearman_list = []
    pearson_pvalue_list = []
    spearman_pvalue_list = []
    decision_pearson_list = []
    decision_spearman_list = []
    reg_lin_list = []
    
    # Seuil de décision:
    alpha = 0.05
    seuil_r=0.3
    
    # Heat map 
    correlation_matrix = df_analyse[vars_quan].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Heatmap des corrélations")
    plt.savefig(os.path.join(images_folder, "heatmap_vars_quan.png"))
    plt.clf()  # Réinitialiser le graphique
    logger.info("Heatmap des corrélations créée")  
    

    # Analyse de régression:
        
    # Modèle de régression linéaire:
    X = df_analyse[vars_quan]  # Variables explicatives
    y = df_analyse[var_cible]       # Variable expliquée
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())   
    
    # Obtenir le résumé du modèle sous forme de texte
    summary = model.summary().as_text()
    
    # Calcul de la statistique Durbin-Watson
    dw_stat = durbin_watson(model.resid)
    print(f"Statistique de Durbin-Watson : {dw_stat:.3f}")
    
    # Interprétation du modèle:
    texte_interpretation = interpret_regression_results(model, dw_stat)
    
    # Créer une image avec ce texte
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.text(0, 1, summary, wrap=True, fontsize=12)
    ax.axis('off')  # Désactiver les axes
    
    # Sauvegarder l'image
    plt.savefig(os.path.join(images_folder, 'model_summary.png'), bbox_inches='tight')
    plt.close()
    
    # Créer un graphique des résidus
    plt.figure(figsize=(8, 6))
    sns.residplot(x=model.fittedvalues, y=model.resid, lowess=True, line_kws={'color': 'red', 'lw': 1})
    plt.xlabel('Prédictions')
    plt.ylabel('Résidus')
    plt.title('Graphique des Résidus')
    
    # Sauvegarder l'image
    plt.savefig(os.path.join(images_folder, 'residual_plot.png'))  # Vous pouvez spécifier un autre chemin et format
    plt.close() 
    
    
    # Calculer le VIF pour chaque variable
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]


    # Prédictions du modèle
    y_pred = model.fittedvalues
    
    for var in vars_quan:
        # Créer un graphique
        plt.figure(figsize=(8, 6))
        plt.scatter(df_analyse[var], y, label="Données réelles")
        plt.plot(df_analyse[var], y_pred, color='red', label="Prédictions")
        plt.xlabel(f"{var}")
        plt.ylabel(f"{var_cible}")
        plt.title(f"Régression Linéaire - {var} vs {var_cible}")
        plt.legend()
        
        # Sauvegarder l'image
        plt.savefig(os.path.join(images_folder, f"{var}_regression_plot.png"))
        reg_lin_list.append(os.path.join(images_folder, f"{var}_regression_plot.png"))
        plt.close()
    
    
    

    # 3.3.2: Analyse variables quantitatives
    logger.info("Scatter + Heatmap + Pearson + Spearman")
    for var in vars_quan:
        # Scatterplot + Heatmap pour visualiser la distribution de '1ere semaine' par variable quantitative
        logger.info(f"Analyse de la variable {var}")
        print(f"Analyse de la variable {var}")
        df_vars_quan_analyse(df_analyse, var, var_cible)
        print("\n")


    # 3.3.3: Création d'un PDF pour résumer l'analyse des variables
    create_analysis_vars_quan_pdf(output_folder_300, 
                                  'Analyses_variables_quantitatives_PDF.pdf', 
                                  os.path.join(images_folder, "heatmap_vars_quan.png"), 
                                  scatterplot_list, 
                                  pearson_list, 
                                  spearman_list, 
                                  decision_pearson_list, 
                                  decision_spearman_list, 
                                  vars_quan, 
                                  summary, 
                                  os.path.join(images_folder, 'residual_plot.png'),
                                  reg_lin_list,
                                  interpretation_reg_lin)
    


    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
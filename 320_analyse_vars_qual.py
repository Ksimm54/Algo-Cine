# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/01/2025

-------------------------------------------------------------------------------
                    320 Analyse des variables qualitatives
-------------------------------------------------------------------------------
"""

def etape320():

    etape = "320_analyse_vars_qual"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------

    # Import des données
    # On va chercher les données de l'étape 2
    logger.info("Importation des données de l'étape 2")
    
    df = pd.read_excel(output_folder_200+r"/Films_270.xlsx")

    
    # 3.2: Analyse des variables qualitatives
    logging.info("320_analyse_vars_qual")
    
    
    # 3.2.1: Définition de la table à analyser
    df_analyse = df[['Date de sortie',
                     'Titre_key',
                     'Titre', 
                     'Réalisateur',
                     'Label réalisateur', 
                     'Acteur Principal',
                     'Label acteur principal', 
                     'Acteur Secondaire',
                     'Label acteur secondaire', 
                     'Durée', 
                     'Studio de Production', 
                     'Société de Distribution', 
                     'Style',
                     'Pays', 
                     'Budget',
                     'Nb entrées semaine année précédente',
                     'Nbre de copies',
                     'Likes', 
                     'Vues', 
                     'Nb_Bandes_annonces', 
                     'Moyenne_Vues', 
                     'Max_Vues', 
                     'Max_Likes', 
                     'Moyenne_Likes',
                     'Entrées',
                     'Data'
                     ]].copy()
    
    # On ne peut pas analyser les données test
    df_analyse = df_analyse[df_analyse['Data'] != 'Test']
    
    # Variables explicatives qualitatives:
    vars_qual = ['Réalisateur', 
                 'Label réalisateur', 
                 'Acteur Principal', 
                 'Label acteur principal', 
                 'Acteur Secondaire',
                 'Label acteur secondaire',
                 'Studio de Production', 
                 'Société de Distribution',
                 'Style',
                 'Pays'
                 ]
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
    
    
    global vpvalue_list
    
    vpvalue_list = []
    
    # 3.2.2: Kruskall Wallis sur les variables qualitatives
    
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(output_folder_300):
        os.makedirs(output_folder_300)
    
    # Construire le chemin complet du fichier PDF
    output_file = os.path.join(output_folder_300, 'Analyses_variables_qualitatives_PDF.pdf')
    
    # Initialiser le PDF
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter  # Taille de la page


    i = 0
    
    logger.info("Kruskall Wallis sur les variables qualitatives")
    for var in vars_qual:
        
        i = i + 1
        
        # Boxplot + Kruskal pour visualiser la distribution de '1ere semaine' par variable qualitative
        logger.info(f"Analyse de la variable {var}")
        print(f"Analyse de la variable {var}")
        box_kruskal(df_analyse, var, var_cible)
        print("\n")
        
        # Titre de la page
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, f"Analyse pour la variable : {var}")  
        
        # Ajouter l'image du boxplot
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, "Boxplot :")
        boxplot_img = boxplot
        c.drawImage(ImageReader(boxplot_img), 50, height - 300, width=250, height=200)
        
        # Ajouter l'image du violon plot
        c.drawString(300, height - 100, "Violinplot :")
        violonplot_img = violonplot
        c.drawImage(ImageReader(violonplot_img), 300, height - 300, width=250, height=200)
        
        # Ajouter les résultats de Kruskal-Wallis
        c.drawString(50, height - 350, "Résultat Kruskal-Wallis :")
        c.drawString(50, height - 370, vkruskal)
        
        # Ajouter la p-value
        c.drawString(50, height - 400, "P-value :")
        c.drawString(50, height - 420, pvalue)
        
        # Passer à la page suivante si ce n'est pas la dernière variable
        if i < len(vars_qual):
            c.showPage()
        
    # Pour la dernière page on conclu sur les variables à garder
    c.showPage()

    # Titre de la page
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Conclusion: Variables à garder pour la prédiction")
    
    # Ajout des variables
    new_height = 100
        
    # 3.2.3: On garde les variables qui passent le test de Kruskall Wallis
    
    keep_var_qual = []
    
    for i, var in enumerate(vars_qual):
        
        if float(vpvalue_list[i]) < 0.05:
            
            keep_var_qual.append(var)
            
            c.setFont("Helvetica", 12)
            c.drawString(50, height - new_height, f"{var}")
            new_height = new_height + 20
            

    
    # Sauvegarder le PDF
    c.save()
    logger.info(f"PDF sauvegardé dans : {output_file}")
    print(f"PDF sauvegardé dans : {output_file}")
        
    
    
    # On exporte les données pour l'analyse dans l'étape 330
    keep_var_qual.append(var_id)
    keep_var_qual.append(var_cible)
    keep_var_qual.append(var_data)
    keep_var_qual = keep_var_qual + vars_quan
    df_analyse_320 = df[keep_var_qual].copy()
    
    df_analyse_320.to_excel(os.path.join(output_folder_300, 'Films_320.xlsx'), index=False)
    


    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    

































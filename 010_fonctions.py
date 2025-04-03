# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 14/01/2024

-------------------------------------------------------------------------------
                    Fonctions
-------------------------------------------------------------------------------
"""

# FONCTION DE LOG

# Fonction pour configurer un nouveau logger avec un fichier de log unique
def setup_logger(etape):
    # Récupérer l'heure actuelle
    now = datetime.now()

    log_folder = r"C:\Users\User\Documents\Algo Ciné\04_Log"  # Vérifie que cette variable est bien définie
    os.makedirs(log_folder, exist_ok=True)  # Crée le dossier 'Log' s'il n'existe pas

    log_file = os.path.join(log_folder, f'execution_log_{etape}_{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}.txt')

    # Créer un logger spécifique
    logger = logging.getLogger(etape)

    # Définir le niveau du logger principal sur DEBUG (pour tout capturer dans le fichier)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # 🔥 Empêche la propagation vers d'autres loggers (notamment root)

    # Supprimer tous les gestionnaires de log existants s'il y en a
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # --- Handler pour le fichier log (capture tout) ---
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # Capture tout
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # --- Handler pour la console (affiche uniquement WARNING et plus) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Afficher seulement WARNING et plus
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger, log_file


# Exemple de lof
#logging.debug('Ce message est de niveau DEBUG')
#logging.info('Exécution du programme démarrée')
#logging.warning('Ce qui suit pourrait être un avertissement')
#logging.error('Une erreur est survenue')
#logging.critical('Erreur critique, intervention nécessaire')



# FONCTION DE GRAPHIQUE

def graph_par_4(data, var):

    # Création de 4 graphiques pour chaque variable
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    
    # Graphique 1 : Minimum
    axs[0, 0].bar(data[var], data['Minimum'], color='skyblue')
    axs[0, 0].set_title(str('Minimum par '+var))
    axs[0, 0].set_ylabel('Minimum')
    
    # Graphique 2 : Maximum
    axs[0, 1].bar(data[var], data['Maximum'], color='orange')
    axs[0, 1].set_title('Maximum par '+var)
    axs[0, 1].set_ylabel('Maximum')
    
    # Graphique 3 : Moyenne
    axs[1, 0].bar(data[var], data['Moyenne'], color='green')
    axs[1, 0].set_title('Moyenne par '+var)
    axs[1, 0].set_ylabel('Moyenne')
    
    # Graphique 4 : Nombre d'occurrences
    axs[1, 1].bar(data[var], data['Nombre_de_film'], color='red')
    axs[1, 1].set_title("Nombre de film par "+'var')
    axs[1, 1].set_ylabel('Nb Films')
    
    # Ajustement de l'espacement
    plt.tight_layout()
    plt.show()    




# FONCTION ANALYSE BOXPLOT + TEST KRUSKAL WALLIS

def box_kruskal(data, exp, to_exp):
    
    
    global boxplot, violonplot, vkruskal, pvalue, vpvalue
    
    
    # Boxplot pour visualiser la distribution de '1ere semaine' par 'Label réalisateur'
    sns.boxplot(x=exp, y=to_exp, data=data)
    plt.title('Distribution de ' + to_exp + ' par ' + exp)
    plt.savefig(os.path.join(images_folder, "boxplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png'))
    plt.clf()  # Réinitialiser le graphique
    boxplot = os.path.join(images_folder, "boxplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png')
    logger.info(f"Boxplot variable: {exp} sur {to_exp} créé")
    
    # Violin plot
    sns.violinplot(x=exp, y=to_exp, data=data, bw_adjust=0.1)
    plt.title('Violin plot : ' + to_exp + ' par ' + exp)
    plt.savefig(os.path.join(images_folder, "violonplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png'))
    plt.clf()  # Réinitialiser le graphique
    violonplot = os.path.join(images_folder, "violonplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png')
    logger.info(f"Violonplot variable: {exp} sur {to_exp} créé")
    
    
    # Test de Kruskal-Wallis
    
    # Grouper les données par la variable à analyser
    groups = [group[to_exp].values for name, group in data.groupby(exp)]
    
    stat, p_value = kruskal(*groups)
    
    logger.info(f"Kruskal-Wallis: Statistique = {stat:.3f}, p-valeur = {p_value:.3f}")
    print(f"Kruskal-Wallis: Statistique = {stat:.3f}, p-valeur = {p_value:.3f}")
    vkruskal = f"Kruskal-Wallis: Statistique = {stat:.3f}, p-valeur = {p_value:.3f}"
    
    if p_value < 0.05:
        logger.info("Il existe une différence significative entre les groupes (test non paramétrique).")
        print("Il existe une différence significative entre les groupes (test non paramétrique).")
        pvalue = "Il existe une différence significative entre les groupes (test non paramétrique)."
        
    else:
        logger.info("Aucune différence significative entre les groupes.")
        print("Aucune différence significative entre les groupes.")
        pvalue = "Aucune différence significative entre les groupes."
        
        
    vpvalue = f"{p_value:.3f}"
    vpvalue_list.append(f"{p_value:.3f}")


# Fonction pour l'analyse des variables quantitatives
def df_vars_quan_analyse(data, exp, to_exp):
    
    # Scatterplot entre une variable explicative quantitative et la variable expliquée
    sns.scatterplot(x=exp, y=to_exp, data=data)
    plt.title(f"Scatterplot entre {exp} et {to_exp}")
    plt.savefig(os.path.join(images_folder, "scatterplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png'))
    plt.clf()  # Réinitialiser le graphique
    scatterplot_list.append(os.path.join(images_folder, "scatterplot_"+to_exp.replace(" ", "")+"_par_"+exp.replace(" ", "")+'.png'))
    logger.info(f"Scatterplot variable: {exp} sur {to_exp} créé")  


    # Corrélation de Pearson
    pearson_corr, pearson_pvalue = pearsonr(data[exp], data[to_exp])
    print(f"Corrélation de Pearson: {pearson_corr:.3f}, P-value: {pearson_pvalue:.3f}")
    logger.info(f"Corrélation de Pearson: {pearson_corr:.3f}, P-value: {pearson_pvalue:.3f}")
    pearson_list.append(f"Corrélation de Pearson: {pearson_corr:.3f}, P-value: {pearson_pvalue:.3f}")
    
    
    # Corrélation de Spearman
    spearman_corr, spearman_pvalue = spearmanr(data[exp], data[to_exp])
    print(f"Corrélation de Spearman: {spearman_corr:.3f}, P-value: {spearman_pvalue:.3f}")
    logger.info(f"Corrélation de Spearman: {spearman_corr:.3f}, P-value: {spearman_pvalue:.3f}")    
    spearman_list.append(f"Corrélation de Spearman: {spearman_corr:.3f}, P-value: {spearman_pvalue:.3f}")



    if pearson_pvalue < alpha and abs(pearson_corr) >= seuil_r:
            print("Relation forte et significative selon Pearson")
            logger.info("Relation forte et significative selon Pearson")
            decision_pearson_list.append("Relation forte et significative selon Pearson")
    elif pearson_pvalue < alpha:
        print("Relation significative mais faible selon Pearson")
        logger.info("Relation significative mais faible selon Pearson")
        decision_pearson_list.append("Relation significative mais faible selon Pearson")
    else:
        print("Aucune relation significative selon Pearson")
        logger.info("Aucune relation significative selon Pearson")
        decision_pearson_list.append("Aucune relation significative selon Pearson")
    
    if spearman_pvalue < alpha and abs(spearman_corr) >= seuil_r:
        print("Relation forte et significative selon Spearman")
        logger.info("Relation forte et significative selon Spearman")
        decision_spearman_list.append("Relation forte et significative selon Spearman")
    elif spearman_pvalue < alpha:
        print("Relation significative mais faible selon Spearman")
        logger.info("Relation significative mais faible selon Spearman")
        decision_spearman_list.append("Relation significative mais faible selon Spearman")
    else:
        print("Aucune relation significative selon Spearman")
        logger.info("Aucune relation significative selon Spearman")
        decision_spearman_list.append("Aucune relation significative selon Spearman")



# Fonction pour créer un pdf avec l'analyse des variables quantitatives
def create_analysis_vars_quan_pdf(output_dir, 
                                  filename, 
                                  heatmap_path, 
                                  scatterplot_list, 
                                  pearson_list, 
                                  spearman_list, 
                                  decision_pearson_list, 
                                  decision_spearman_list, 
                                  variables, 
                                  model_summary, 
                                  residual_plot_path, 
                                  reg_lin_list,
                                  interpretation_text):
    
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Construire le chemin complet du fichier PDF
    output_file = os.path.join(output_dir, filename)
    
    # Initialiser le PDF
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter  # Taille de la page
    
    # 1ère page : Résumé du modèle de régression
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Résumé du modèle de régression linéaire avec les variables quantitatives")
    c.setFont("Helvetica", 10)
    
    # Ajouter le résumé du modèle dans le PDF
    y_position = height - 100
    for line in model_summary.split('\n'):
        c.drawString(50, y_position, line)
        y_position -= 12  # Décalage vertical entre chaque ligne
        
    # Ajouter l'interprétation des résultats
    y_position -= 20  # Ajouter un espace entre les sections
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Interprétation des résultats :")
    y_position -= 15
    c.setFont("Helvetica", 10)
    
    for line in interpretation_text:
        if y_position < 50:  # Si la position verticale est trop basse, passer à une nouvelle page
            c.showPage()
            y_position = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y_position, line)
        y_position -= 12
    
    c.showPage()  # Passer à la page suivante
    
    # 2ème page : Graphique des résidus
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Graphique des Résidus")
    c.drawImage(ImageReader(residual_plot_path), 50, height - 400, width=500, height=300)
    c.showPage()  # Passer à la page suivante
    
    # Page des régressions linéaires
    for i, var in enumerate(variables):
        # Titre de la page
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, f"Régression linéaire pour la variable : {var}")
        
        # Ajouter la regression linéaire
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, "Regression linéaire :")
        reg_lin_image = reg_lin_list[i]
        c.drawImage(ImageReader(reg_lin_image), 50, height - 300, width=400, height=200)
        
        c.showPage()
        
    
    # Page : Heatmap des corrélations
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Heatmap des corrélations :")
    c.drawImage(ImageReader(heatmap_path), 50, height - 400, width=500, height=300)
    c.showPage()
    
    # Statistiques par variables
    for i, var in enumerate(variables):
        # Titre de la page
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, f"Analyse pour la variable : {var}")
        
        # Ajouter le scatterplot
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, "Scatterplot :")
        scatterplot_img = scatterplot_list[i]
        c.drawImage(ImageReader(scatterplot_img), 50, height - 300, width=400, height=200)
        
        # Ajouter le résultat de Pearson
        c.drawString(50, height - 350, "Résultat de la corrélation de Pearson :")
        c.drawString(50, height - 370, pearson_list[i])
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 390, decision_pearson_list[i])
        
        # Ajouter le résultat de Spearman
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 420, "Résultat de la corrélation de Spearman :")
        c.drawString(50, height - 440, spearman_list[i])
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 460, decision_spearman_list[i])
        
        # Passer à la page suivante si ce n'est pas la dernière variable
        if i < len(variables) - 1:
            c.showPage()
    
    # Sauvegarder le PDF
    c.save()
    print(f"PDF sauvegardé dans : {output_file}")



# Fonction pour interpréter les résultats de la regression linéaire:
def interpret_regression_results(model, durbin_watson_stat):
    
    global interpretation_reg_lin, var_quan_to_drop
    
    interpretation_reg_lin = []
    var_quan_to_drop = []
    
    # R-squared
    r_squared = model.rsquared
    adj_r_squared = model.rsquared_adj
    interpretation_reg_lin.append(f"Le modèle explique {r_squared:.1%} de la variance des données (R-squared).")
    interpretation_reg_lin.append(f"L'indicateur ajusté (Adj. R-squared) est de {adj_r_squared:.1%}.")
    
    # P-value du F-statistic
    if model.f_pvalue < 0.05:
        interpretation_reg_lin.append("Le modèle global est statistiquement significatif (P-value du F-statistic < 0.05).")
    else:
        interpretation_reg_lin.append("Le modèle global n'est pas statistiquement significatif (P-value du F-statistic >= 0.05).")
    
    # Coefficients
    for var, coef, pval in zip(model.params.index, model.params.values, model.pvalues.values):
        if pval < 0.05:
            interpretation_reg_lin.append(f"- {var} : effet significatif (P = {pval:.3f}), coefficient = {coef:.3f}.")
        else:
            interpretation_reg_lin.append(f"- {var} : effet non significatif (P = {pval:.3f}).")
            var_quan_to_drop.append(var)
    
    # Durbin-Watson
    interpretation_reg_lin.append(f"Statistique de Durbin-Watson : {durbin_watson_stat:.3f}.")
    if 1.5 <= durbin_watson_stat <= 2.5:
        interpretation_reg_lin.append("Les résidus ne montrent pas d'autocorrélation significative.")
    else:
        interpretation_reg_lin.append("Attention : il peut y avoir une autocorrélation des résidus.")
    



# Évaluation du modèle
def eval_model(y_true, y_pred, dataset_name):
    
    global mae, rmse, r2
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"📊 {dataset_name} - MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}")



def largeur_colonne(file, largeur):

    # Charger le fichier Excel avec openpyxl
    wb = load_workbook(file)
    ws = wb.active  # Sélectionne la feuille active
    
    # Définir une largeur de colonne par défaut
    default_width = largeur  # Ajustez cette valeur selon vos besoins
    
    for col in ws.columns:
        max_length = default_width
        col_letter = col[0].column_letter  # Obtenir la lettre de la colonne
        ws.column_dimensions[col_letter].width = max_length
        
    # Appliquer un filtre automatique sur toutes les colonnes
    ws.auto_filter.ref = ws.dimensions  # Applique le filtre sur toute la plage de données

    
    # Sauvegarder le fichier modifié
    wb.save(file)



# Fonction pour récupérer le dernier mercredi
def last_wednesday():

    today = datetime.today()
    
    # Vérifie si aujourd'hui est mercredi (2 = mercredi car lundi = 0)
    if today.weekday() == 2:
        dernier_mercredi = today
    else:
        dernier_mercredi = today - timedelta(days=(today.weekday() - 2) % 7)
        
    dernier_mercredi = dernier_mercredi.strftime("%Y-%m-%d")
    
    return dernier_mercredi


# Transformer l'url d'une image en base64
def url_to_base64(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            return base64.b64encode(image_data.read()).decode('utf-8')
        else:
            return None  # En cas d'échec du téléchargement
    except Exception as e:
        return None  # En cas d'erreur



# Mettre le premier mot en capital
def capitalize_first_non_excluded(title):
    
    #Titre avec des nouvelles majuscules
    exclusions = {
        # Prépositions françaises
        "de", "du", "des", "le", "la", "les", "un", "une", "et", "à", "au", "aux",
        "ma", "me", "mes", "te", "ta", "tes",
        "mais", "ou", "où", "donc", "or", "ni", "car", "sur", "sous", "avec",
        "par", "pour", "sans", "contre", "en", "vers", "chez", "dans", "ce", "cet", "cette", "ces", 
        "lorsque", "afin", "ainsi", "après", "avant", "depuis", "pendant", "jusqu'à", "tandis", "parmi",
    
        # Prépositions anglaises
        "the", "a", "an", "and", "or", "but", "nor", "for", "so", "yet", "of", "on", "in", "at", 
        "to", "by", "with", "about", "against", "between", "into", "through", "during", "before",
        "after", "above", "below", "from", "up", "down", "over", "under", "again", "further",
        "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "not", "only", "own", "same", "so",
        "than", "too", "very"
    }
    
    words = title.split()
    for i, word in enumerate(words):
        if word.lower() not in exclusions:  # Vérifie si le mot n'est pas une préposition
            words[i] = word.capitalize()  # Met en majuscule le premier mot non exclu
            break  # Arrête après la première modification
    return " ".join(words)


# Mettre tous les mots sans les prépositions en majuscule
def capitalize_title(title):
    
    #Titre avec des nouvelles majuscules
    exclusions = {
        # Prépositions françaises
        "de", "du", "des", "le", "la", "les", "un", "une", "et", "à", "au", "aux",
        "ma", "me", "mes", "te", "ta", "tes",
        "mais", "ou", "où", "donc", "or", "ni", "car", "sur", "sous", "avec",
        "par", "pour", "sans", "contre", "en", "vers", "chez", "dans", "ce", "cet", "cette", "ces", 
        "lorsque", "afin", "ainsi", "après", "avant", "depuis", "pendant", "jusqu'à", "tandis", "parmi",
    
        # Prépositions anglaises
        "the", "a", "an", "and", "or", "but", "nor", "for", "so", "yet", "of", "on", "in", "at", 
        "to", "by", "with", "about", "against", "between", "into", "through", "during", "before",
        "after", "above", "below", "from", "up", "down", "over", "under", "again", "further",
        "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "not", "only", "own", "same", "so",
        "than", "too", "very"
    }
    
    words = title.lower().split()  # Tout en minuscule puis split en mots
    capitalized_words = [word.capitalize() if word not in exclusions else word for word in words]
    return " ".join(capitalized_words)

# Mettre la première lettre en majuscule
def capitalize_first_letter(title):
    if not title:
        return title  # Gérer les valeurs vides ou None
    return title[0].upper() + title[1:]  # Mettre la première lettre en majuscule

















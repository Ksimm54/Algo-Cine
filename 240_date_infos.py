# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 20:34:35 2025

@author: User
"""

"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 17/01/2025

-------------------------------------------------------------------------------
                    240 Date infos
-------------------------------------------------------------------------------
"""

def etape240():
    
    etape = "240_date_infos"
    
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 2.4.1: Importation des Données mises à jours dans les étapes précédentes
    logging.info("2.4.1: Importation Données")
    df = pd.read_excel(os.path.join(output_folder_200, 'Films_230.xlsx'))
    df_real = pd.read_excel(_0_file_realisateurs)
    df_act = pd.read_excel(_0_file_acteurs)
    logging.info('Données importées')
    
    df['Date de sortie'] = pd.to_datetime(df['Date de sortie'])
    
    
    # 2.4.2: On créé un calendrier pour séléctionner seulement les mercredis ensuite
    
    # On se concentre sur les données de 2023 et 2024
    
    min_year = 2023
    max_year = 2024
    min_month = 1
    max_month = 12
    logger.info(f"min_year = {min_year}")
    logger.info(f"max_year = {max_year}")
    logger.info(f"min_month = {min_month}")
    logger.info(f"max_month = {max_month}")
    
    
    dates = pd.date_range(start=f"{min_year}-{min_month}-01", end=f"{max_year}-{max_month}-31")
    logger.info(f"Periode: {min_year}-{min_month}-01  -  {max_year}-{max_month}-31")
    
    
    df_calendrier = pd.DataFrame({
        "Date de sortie": dates,
        "Jour": dates.day,
        "Jour de la semaine": dates.day_name(),
        "Semaine de l'année": dates.isocalendar().week
        })
    
    
    df_cal_wed = df_calendrier[df_calendrier['Jour de la semaine'] == 'Wednesday']
    
    df_wed = pd.DataFrame(df[(df["Date de sortie"].dt.year >= min_year) & (df["Date de sortie"].dt.year <= max_year)].groupby("Date de sortie").size().reset_index(name='Nombre de film'))                                         
    
    
    # 2.4.3: Check données manquantes
    logger.info("2.4.3: Check données manquantes")
    
    df_wed_check = pd.merge(df_cal_wed, df_wed, on='Date de sortie', how='left')
    df_wed_check['Nombre de film'] = df_wed_check['Nombre de film'].fillna(0)
    
    df_wed_check = df_wed_check[df_wed_check['Nombre de film'] < 3]
    
    
    # Ajouter les films 1 et 2
    def add_films_for_date(row, df):
        # Filtrer df pour obtenir les films de cette date
        films_on_date = df[df['Date de sortie'] == row['Date de sortie']]['Titre'].tolist()
        
        # Assigner Film 1 et Film 2
        film_1 = films_on_date[0] if len(films_on_date) > 0 else None
        film_2 = films_on_date[1] if len(films_on_date) > 1 else None
        
        return pd.Series([film_1, film_2])
    
    # Appliquer cette fonction pour ajouter Film 1 et Film 2 à df_wed_check
    df_wed_check[['Film 1', 'Film 2']] = df_wed_check.apply(lambda row: add_films_for_date(row, df), axis=1)

    
    
    if len(df_wed_check) > 0:
        
        print('ATTENTION : Il manque des données pour certaines dates')
        print("Il est recommandé d'avoir au moins 3 films par date")
        logger.info('ATTENTION : Il manque des données pour certaines dates')
        logger.info("Il est recommandé d'avoir au moins 3 films par date")
              
        os.makedirs(to_complete_folder, exist_ok=True)
    
        df_wed_check[['Date de sortie', 'Nombre de film', 'Film 1', 'Film 2']].to_excel(_0_file_date_a_completer, index=False)
        logger.warning(f"Liste des dates à compléter: {to_complete_folder}/dates_a_completees.xlsx")
    
    else: 
        
        print(f"Assez de films sur la periode suivante: {min_year}-{max_year}")
        logger.info(f"Assez de films sur la periode suivante: {min_year}-{max_year}")
    
    
    
    
    
    
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
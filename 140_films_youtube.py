# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 26/03/2025

-------------------------------------------------------------------------------
                    140_youtube
-------------------------------------------------------------------------------
"""

def etape140():
    
    
    global scraping_do
    
    
    etape = "140_youtube"
    
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.4.1: Import des données
    logging.info("1.4.1: Import des données")
    
    df_y = pd.read_excel(_0_file_films_youtube)
    df_dates = pd.read_excel(_0_file_param_variables, sheet_name=_0_sheet_date_import_y)
    df_yt_id = pd.read_excel(_0_file_labels, sheet_name=_0_sheet_chaines_y)
    token_df = pd.read_excel(_0_file_param_variables, sheet_name = _0_sheet_token)
    
    # On définit en datetime les variables
    df_y["StartDate"] = pd.to_datetime(df_y["StartDate"])
    df_y["EndDate"] = pd.to_datetime(df_y["EndDate"])
    
    # Si du scraping a été effectué alors on lance l'étape 150
    scraping_do = 0
    
    # On vérifie qu'il y a bien les noms des chaines:
    if len(df_dates[~df_dates['Chaine'].isna()]) == 0:
        
        print('Aucune données de Youtube à importer')
        
    else:
        
        df_dates = df_dates[~df_dates['Chaine'].isna()]
        
        # S'il n'y a pas de dates alors on importe les données de la semaine en cours
        if len(df_dates[df_dates['StartDate'].isna() | df_dates['EndDate'].isna()]) > 0:
            
            date = last_wednesday()
            date = pd.to_datetime(date)
            #date_annee_precedente = date - timedelta(days=365)
            date_annee_precedente = date - timedelta(days=7)
            # POUR LES TESTS
            
            df_dates.loc[df_dates['StartDate'].isna(), 'StartDate'] = date_annee_precedente
            df_dates.loc[df_dates['EndDate'].isna(), 'EndDate'] = date
            df_dates.loc[df_dates['force'].isna(), 'force'] = 0
            df_dates.loc[df_dates['to_scrap'].isna(), 'to_scrap'] = 1
            
            df_dates["EndDate"] = pd.to_datetime(df_dates["EndDate"])
            df_dates['StartDate'] = pd.to_datetime(df_dates["StartDate"])
            
        else:
            
            #date_annee_precedente = df_dates['EndDate'].iloc[0] - timedelta(days=365)
            #POUR LES TESTS
            df_dates["EndDate"] = pd.to_datetime(df_dates["EndDate"])
            df_dates['StartDate'] = pd.to_datetime(df_dates["StartDate"])
            
    
        if len(df_dates[df_dates['to_scrap'] == 1]) == 0:
            
            logger.info("Youtube pas à scrapper")
            print("Youtube pas à scrapper")
            
            
        elif len(df_dates[df_dates["EndDate"].dt.dayofweek != 2]) > 0 or len(df_dates[df_dates["StartDate"].dt.dayofweek != 2]):
            
            logger.info("Erreur dans le fichier de paramétrage des dates: Veuillez rentrer un mercredi")
            print("Erreur dans le fichier de paramétrage des dates: Veuillez rentrer un mercredi")
            
            if len(df_dates[df_dates["EndDate"].dt.dayofweek != 2]) > 0:
                
                print("EndDate problématique(s)")
                for EndDate in df_dates[df_dates["EndDate"].dt.dayofweek != 2]['EndDate']:
                    print(EndDate)
                    
            if len(df_dates[df_dates["StartDate"].dt.dayofweek != 2]) > 0:
                
                print("StartDate problématique(s)")
                for StartDate in df_dates[df_dates["StartDate"].dt.dayofweek != 2]['StartDate']:
                    print(StartDate)
                    
            
            # ---------- FIN DU JOURNAL
            logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
            logging.shutdown()
            # ----------
            
            sys.exit()
            
            
        elif token_df["Nb Token"].iloc[0] == 0:
            
            logger.info("Plus de token disponibles")
            print("Plus de token disponibles")
            
            
        else:

            # Liste pour stocker tous les calendriers
            all_calendars = []
            
            # Générer un calendrier pour chaque chaîne
            for _, row in df_dates.iterrows():
                start_date = row["StartDate"]
                end_date = row["EndDate"]
                chaine = row["Chaine"]
            
                # Générer toutes les dates correspondant aux mercredis entre StartDate et EndDate
                wednesday_dates = pd.date_range(start=start_date, end=end_date, freq="W-WED")
            
                # Ne garder que les dates après le StartDate
                cal_df = pd.DataFrame({"EndDate": wednesday_dates})
                cal_df = cal_df[cal_df["EndDate"] > start_date]
            
                # Définir les StartDate
                cal_df["StartDate"] = cal_df["EndDate"] - pd.Timedelta(days=7)
            
                # Convertir au format RFC 3339
                cal_df["StartDate"] = cal_df["StartDate"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                cal_df["EndDate"] = cal_df["EndDate"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            
                # Ajouter le nom de la chaîne
                cal_df["Chaine"] = chaine
            
                # Réorganiser les colonnes
                cal_df = cal_df[['Chaine', 'StartDate', 'EndDate']]
            
                # Ajouter au résultat global
                all_calendars.append(cal_df)
            
            # Fusionner tous les calendriers
            calendrier_df = pd.concat(all_calendars, ignore_index=True)
            
            
            if len(calendrier_df) > 0:
            
                
                # On utilise l'API pour les informations dont on a besoin
                
                columns = ['Chaine',
                           'date_scraping', 
                           'page_token', 
                           'next_page_token', 
                           'StartDate', 
                           'EndDate', 
                           'Vidéo ID']
                
                df_films_id = pd.DataFrame(columns=columns)
                
                # On récupère les ID des vidéos
                
                # On calcule une estimation du nombre de token qui vont être utilisé:
                    
                # Nombre moyen de vidéo par semaine
                
                # Filtrer les lignes de calendrier_df qui ne sont pas dans df_y
                df_y_est = df_y.copy()
                calendrier_df_est = calendrier_df.copy()
                
                df_y_est['StartDate'] = pd.to_datetime(df_y_est['StartDate'], utc=True)
                df_y_est['EndDate'] = pd.to_datetime(df_y_est['EndDate'], utc=True)
                calendrier_df_est['StartDate'] = pd.to_datetime(calendrier_df_est['StartDate'], utc=True)
                calendrier_df_est['EndDate'] = pd.to_datetime(calendrier_df_est['EndDate'], utc=True)
                
                result_df = calendrier_df_est.merge(df_y_est, on=['Chaine', 'StartDate', 'EndDate'], how='left', indicator=True)
                result_df = result_df[result_df['_merge'] == 'left_only'].drop(columns=['_merge'])
                
                moyenne_id = round(df_y.groupby(["Chaine", "StartDate", "EndDate"])["Vidéo ID"].count().mean())
                
                nb_token = token_df['Nb Token'].iloc[0]
                
                estimation_token = round(len(result_df) * 100 + moyenne_id * 1.12) # 100 token par semaine + 1.12 token par vidéos
                
                print(f"Nb Token: {nb_token}")
                print(f"Estimation du nombre de token pour requêter l'API Youtube entre la periode: {start_date.date()} et {end_date.date()}")
                print(f"Estimation: {estimation_token}")
                
                input_reponse = input("Voulez-vous continuer (y/n) ? ").strip().lower()
                
                if input_reponse != "y":
                    
                    print("Pas d'utilisation de l'API")
                    
                else: 
                    
                    # On définit la limite de token
                    lim_token = 0
                    
                    for _, row in df_dates.iterrows():
                        
                        chaine = row["Chaine"]
                        calendrier_df_chaine = calendrier_df[calendrier_df["Chaine"] == chaine].copy()
                        start_dates = calendrier_df_chaine["StartDate"]
                        end_dates = calendrier_df_chaine["EndDate"]
                        
                        
                        for StartDate, EndDate in zip(start_dates, end_dates):
                            
                            ny_df = 0
                            
                            if row["force"] == 0:
                                
                                df_y["StartDate"] = pd.to_datetime(df_y["StartDate"])
                                df_y["EndDate"] = pd.to_datetime(df_y["EndDate"])

                                df_y_filter = df_y[(df_y["StartDate"] == StartDate) & (df_y["EndDate"] == EndDate) & (df_y['Chaine'] == chaine)]
                                
                                ny_df = len(df_y_filter)
                            
                                if ny_df > 0:
                                    print(f"[{chaine}] Déjà des données pour cet intervalle : {StartDate} - {EndDate}")
                                    continue
                                
                            if row["force"] == 1 or ny_df == 0:
                                
                                if len(df_yt_id[df_yt_id['Chaine'] == chaine]) > 0:
                                    
                                    # Utilisation de l'API YouTube  
                                    API_KEY = "AIzaSyAdoD0cKGGA75omqHrahS1t6Rh4765QR8g"
                                    CHANNEL_ID = df_yt_id.loc[df_yt_id['Chaine'] == chaine, 'ID'].iloc[0]  # FilmsActus
                                    
                                    page_token = None
                                    max_results = 50
                                    
                                    # Format des dates pour l'API YouTube
                                    start_date = pd.to_datetime(StartDate).strftime('%Y-%m-%dT%H:%M:%SZ')
                                    end_date = pd.to_datetime(EndDate).strftime('%Y-%m-%dT%H:%M:%SZ')
                                
                                    # Construire l'URL avec les filtres de date
                                    url_search = (
                                        f"https://www.googleapis.com/youtube/v3/search?"
                                        f"part=id&channelId={CHANNEL_ID}&maxResults={max_results}"
                                        f"&order=date&type=video&key={API_KEY}"
                                        f"&publishedAfter={start_date}&publishedBefore={end_date}"
                                    )
                                    
                                    print(f"[{chaine}] Scrapping URL: {url_search}")
                                
                                    # Ajouter le pageToken si on continue la pagination
                                    if page_token:
                                        url_search += f"&pageToken={page_token}"
                                
                                    # Initialisation des valeurs par défaut
                                    video_ids = []
                                    next_page_token = None
                        
                                    # Requête à l'API
                                    response = requests.get(url_search)
                                
                                    # Vérifier le statut HTTP de la réponse
                                    if response.status_code == 200:
                                        data = response.json()
                                        video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
                                        next_page_token = data.get("nextPageToken")
                                
                                    else:
                                        print(f"⚠️ [{chaine}] Erreur API ({response.status_code}) → Limite de token atteinte")
                                        lim_token = 1
                                        token_df['Nb Token'] = 0
                                        
                                        with pd.ExcelWriter(_0_file_param_variables, mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
                                            token_df.to_excel(writer, sheet_name=_0_sheet_token, index=False)
                                        
                                        break
                                
                                    now = datetime.now()
                                    if video_ids:  # Si la liste n'est pas vide
                                        df = pd.DataFrame({
                                            "Chaine": [chaine] * len(video_ids),
                                            "date_scraping": [now.date()] * len(video_ids),
                                            "page_token": [page_token] * len(video_ids),
                                            "next_page_Token": [next_page_token] * len(video_ids),
                                            "StartDate": [StartDate] * len(video_ids),
                                            "EndDate": [EndDate] * len(video_ids),
                                            "Vidéo ID": video_ids
                                        })
                                    else:  # Si la liste est vide, créer une ligne avec None
                                        df = pd.DataFrame({
                                            "Chaine": [chaine],
                                            "date_scraping": [now.date()],
                                            "page_token": [page_token],
                                            "next_page_Token": [next_page_token],
                                            "StartDate": [StartDate],
                                            "EndDate": [EndDate],
                                            "Vidéo ID": [None]
                                        })
                        
                                    df_films_id = pd.concat([df_films_id, df], ignore_index=True)
                                    
                                    
                                else:
                                    
                                    print(f"Chaine Youtube inconnue: {chaine}")
                            
                                            
                    if len(df_films_id) > 0:
                        
                        # On définit la variable scraping_do car des données ont été ajoutées
                        scraping_do = 1
                        
                        columns = ['Chaine', 'Vidéo ID', 'Titre', 'Vues', 'Likes']
                        df_films_stats = pd.DataFrame(columns=columns)
                        
                        video_data = []
                        
                        # Boucle sur chaque chaîne unique dans df_films_id
                        for chaine in df_films_id['Chaine'].unique():
                            
                            # Filtrer df_films_id pour cette chaîne
                            df_films_chaine = df_films_id[df_films_id['Chaine'] == chaine]
                            
                            # On récupère les stats des vidéos pour chaque chaîne
                            for video_id in df_films_chaine['Vidéo ID']:
                                
                                if video_id is not None:
                                    
                                    # Construire l'URL API pour récupérer les détails de la vidéo
                                    url_video = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}"
                                    print(url_video)
                                    response = requests.get(url_video)
                                    
                                    if response.status_code == 200:
                                        
                                        response_video = response.json()
                                        
                                        for item in response_video.get("items", []):
                                            title = item["snippet"]["title"]
                                            views = item["statistics"]["viewCount"]
                                            likes = item["statistics"].get("likeCount", "N/A")
                                            
                                            # Ajouter les données vidéo à la liste
                                            video_data.append({
                                                "Chaine": chaine,
                                                "Vidéo ID": video_id,
                                                "Titre": title,
                                                "Vues": views,
                                                "Likes": likes
                                            })
                                            
                                            print(f"[{chaine}] Vidéo scrapée: {title}")
                    
                                    else:
                                        print(f"⚠️ Erreur API ({response.status_code}) → Limite de token atteinte")
                                        token_df['Nb Token'] = 0
                                        
                                        with pd.ExcelWriter(_0_file_param_variables, mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
                                            token_df.to_excel(writer, sheet_name=_0_sheet_token, index=False)
                                        
                                        break
                                
                                else:
                                    # Si vidéo_id est None, ajouter des valeurs None dans les données
                                    video_data.append({
                                        "Chaine": chaine,
                                        "Vidéo ID": None,
                                        "Titre": None,
                                        "Vues": None,
                                        "Likes": None
                                    })
                        
                        # Création du DataFrame avec les données récupérées
                        df_temp = pd.DataFrame(video_data)
                        
                        # Concaténation avec le DataFrame existant
                        df_films_stats = pd.concat([df_films_stats, df_temp], ignore_index=True)
                        
                        # On regroupe nos données avec les informations de df_films_id
                        df_final = pd.merge(df_films_id, df_films_stats, on=["Chaine", "Vidéo ID"], how="left")
                        
                        # 1.3.4: Exportation Données étape 140:
                        logging.info('Exportation Données étape 140')
                        
                        if os.path.exists(os.path.join(output_folder_100, 'Films_140.xlsx')) == True:
                            shutil.move(os.path.join(output_folder_100, 'Films_140.xlsx'), os.path.join(output_folder_100, r'Historique/Films_140'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
                        
                        df_final.to_excel(os.path.join(output_folder_100, 'Films_140.xlsx'), index=False)
                        
                        # Mise à jour du nombre de token disponible
                        token_use = len(df_final)*20
                        token_df['Nb Token'] = token_df['Nb Token'].iloc[0] - token_use
                        
                        with pd.ExcelWriter(_0_file_param_variables, mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
                            token_df.to_excel(writer, sheet_name=_0_sheet_token, index=False)
                                
                
            else: 
                
                print("Pas de données Youtube à scraper")
        
    
 
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        




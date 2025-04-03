# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 11/03/2025

-------------------------------------------------------------------------------
                    110 Cine_directors
-------------------------------------------------------------------------------
"""

def etape110():
    
    
    
    global scraping_do
    
    
    etape = "110_Cine_directors"
    
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.1.1: Import des données
    logging.info("1.1.1: Import des données")
    
    df_dates = pd.read_excel(_0_file_param_variables, sheet_name=_0_sheet_date_import_cd)
    df_films = pd.read_excel(_0_file_films_cd)
    
    # Si du scraping a été effectué alors on lance l'étape 120
    scraping_do = 0
    
    # S'il n'y a pas de dates alors on importe les données de la semaine en cours
    
    
    # IMPORTANT: Le site est mis à jour le jeudi soir vers 18h30
    
    if len(df_dates) == 0:
        
        date = last_wednesday()
        date = pd.to_datetime(date)
        
        df_dates.loc[0, 'Date_to_import'] = date
        df_dates.loc[0, 'type'] = 'WEEK'
        df_dates.loc[0, 'force'] = 0
        df_dates.loc[0, 'to_scrap'] = 1
        
    
    if len(df_dates) >= 2:
        
        logger.info("Erreur dans le fichier de paramétrage des dates")
        print("Erreur dans le fichier de paramétrage des dates")
        
        # ---------- FIN DU JOURNAL
        logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
        logging.shutdown()
        # ----------
        
        sys.exit()
        
    elif df_dates['to_scrap'].iloc[0] == 0:
        
        logger.info("www.cinedirectors.html pas à scrapper")
        print("www.cinedirectors.html pas à scrapper")
        
    
    else:
        
        
        logger.info(f"Définition d'un calendrier")
        print(f"Définition d'un calendrier")
        
        # On créé un calendrier sur l'année d'import 
        
        # Spécifie l'année
        year = df_dates['Date_to_import'].iloc[0].year
        
        # Créer une liste de toutes les dates de l'année
        dates = pd.date_range(f'{year}-01-01', f'{year}-12-31', freq='D')
        
        # Créer un DataFrame à partir de ces dates
        calendar_df = pd.DataFrame(dates, columns=['date'])
        
        # Filtrer pour ne garder que les mercredis (weekday() == 2 pour mercredi)
        calendar_df['weekday'] = calendar_df['date'].dt.weekday
        calendar_df = calendar_df[calendar_df['weekday'] == 2]
        
        # Ajouter la colonne de numéro de semaine, numéro de mois et l'année
        calendar_df['week_number'] = calendar_df['date'].dt.isocalendar().week
        calendar_df['month_number'] = calendar_df['date'].dt.month
        calendar_df['year'] = calendar_df['date'].dt.year
        
        # Formater le numéro de semaine avec deux chiffres
        calendar_df['week_number'] = calendar_df['week_number'].apply(lambda x: str(x).zfill(2))
        
        # Sélectionner seulement les colonnes nécessaires
        calendar_df = calendar_df[['week_number', 'month_number', 'year', 'date']]
        
        # On définit en datetime la date
        date_to_import = pd.to_datetime(df_dates['Date_to_import'].iloc[0])
        
        if df_dates['type'].iloc[0].upper() == 'YEAR': 
            
            logger.info(f"Import de l'année: {df_dates['Date_to_import'].iloc[0].year}")
            print(f"Import de l'année: {df_dates['Date_to_import'].iloc[0].year}")
            
            if date_to_import.year == pd.to_datetime(last_wednesday()).year:
                
                date = pd.Timestamp(last_wednesday())
                
                calendar_df = calendar_df[calendar_df['date'] <= date]  
            
        
        elif df_dates['type'].iloc[0].upper() == 'MONTH': 
            
            logger.info(f"Import du mois: {df_dates['Date_to_import'].iloc[0].month} de l'année: {df_dates['Date_to_import'].iloc[0].year}")
            print(f"Import du mois: {df_dates['Date_to_import'].iloc[0].month} de l'année: {df_dates['Date_to_import'].iloc[0].year}")
        
            # Spécifie le mois
            month = date_to_import.month
            
            calendar_df = calendar_df[calendar_df['month_number'] == month]
            
        
        elif df_dates['type'].iloc[0].upper() == 'WEEK': 
            
            logger.info(f"Import de la semaine: {df_dates['Date_to_import'].iloc[0]}")
            print(f"Import de la semaine: {df_dates['Date_to_import'].iloc[0]}")


            if str(df_dates['Date_to_import'].iloc[0].date()) != last_wednesday():

                date = date_to_import
                
                calendar_df = calendar_df[calendar_df['date'] == date]
                
            else: 

                date = date_to_import
                date_semaine_precedente = date - timedelta(days=7)
                
                calendar_df = calendar_df[(calendar_df['date'] == date) | (calendar_df['date'] == date_semaine_precedente)]
                
        
        if len(calendar_df) == 0:
            
            logger.info("Erreur dans le fichier de paramétrage des dates: date séléctionnée pas un mercredi")
            print("Erreur dans le fichier de paramétrage des dates: date séléctionnée pas un mercredi")
            
            # ---------- FIN DU JOURNAL
            logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
            logging.shutdown()
            # ----------
            
            sys.exit()
                
        else:

            # On scrappe les informations dont on a besoin
            
            columns = ['Date', 'Rang', 'Titre', 'Entrées', 'Variation hebdo', 'Cumul (Millions)', 'Budget', 'Nbre de copies', 'Moy / Copie', 'Lien cd']
            df_films_to_ad = pd.DataFrame(columns=columns)
            
            for week_number, date in zip(calendar_df['week_number'], calendar_df['date']): 

                # Avant de scraper on vérifie que les données n'existent pas déjà:
                    
                nfilms_df = 0 
                    
                if df_dates['force'].iloc[0] == 0:
                    
                    df_films_filter = df_films[(df_films['Date'] == date) & ~(df_films['Entrées'].isna())]
                    nfilms_df = len(df_films_filter)
                    
                    if nfilms_df >= 1:
                        
                        print(f'Déjà des données pour cette date {date}')
                        continue
                
                if df_dates['force'].iloc[0] == 1 or nfilms_df == 0 or os.path.exists(os.path.join(data_folder, 'films_cine_directors.xlsx')) == False:

                    if df_dates['force'].iloc[0] == 1:
                        
                        print('Ré-import des données')

                    if str(date.date()) == last_wednesday():

                        url1 = 'http://www.cine-directors.net/box/'+ str(year) + '/boxbis.html'
                        url2 = 'http://www.cine-directors.net/box/'+ str(year) + '/boxbis.htm'
                        
                    else:
                        
                        url1 = 'http://www.cine-directors.net/box/'+ str(year) + '/boxoff' + str(week_number) + '.html'
                        url2 = 'http://www.cine-directors.net/box/'+ str(year) + '/boxoff' + str(week_number) + '.htm'
                        
                        
                    urls = [url1, url2]
                    urls0 = []
                    
                    for url in urls:

                        headers = {
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
                                    }

                        # Envoyer une requête HTTP et parser le contenu HTML
                        response = requests.get(url, headers = headers)
                        
                        if response.status_code == 200:
                        
                            print(f'Scraping date: {date}')
                            print(f'Scraping url: {url}')
                                
                            response.raise_for_status()
                            soup = BeautifulSoup(response.text, "html.parser")

                            # Trouver tous les tableaux dans la page
                            tables = soup.find_all("table")
                            target_table = None
                            
                            previ=0
                            for table in tables:
                                rows = table.find_all("tr")
                                if not rows:
                                    continue  # Ignorer les tables vides
                            
                                # Vérifier que la première ligne contient les bonnes colonnes
                                headers = [col.text.strip().lower() for col in rows[0].find_all("td")]
                                
                                for header in headers:
                                    # Nettoyage de l'élément : supprimer les espaces superflus et ignorer la casse
                                    cleaned_header = " ".join(header.split())  # Supprime les espaces multiples et les retours à la ligne
                                    if "box-office france" in cleaned_header.lower(): 
                                        target_table = table
                                        break
                                    if "box-office prévisionnel" in cleaned_header.lower():
                                        target_table = table
                                        previ=1
                                        break  # Sortir de la boucle dès que 'box-office' est trouvé 
                            
                            if not target_table:
                                raise ValueError("Tableau contenant les données introuvable !")
                            
                            # Extraire les noms de colonnes dynamiquement
                            header_rows = target_table.find_all("tr")
                            
                            # Parcourir chaque ligne et vérifier si elle contient l'attribut bgcolor avec la couleur spécifique
                            header_row = None  # Initialisation de la variable qui va contenir la ligne d'en-tête
                            
                            for row in header_rows:

                                if 'titre' in row.get_text().lower():
                                    header_row = row  # Si trouvé, on garde cette ligne
                                    break  # On sort de la boucle une fois qu'on a trouvé la ligne
                            
                            column_names = [re.sub(r'\s+', ' ', col.text.strip().lower()) for col in header_row.find_all("td")]
                            
                            # Normaliser les noms pour éviter les variations (ex: "variation hebdo" vs "variation")
                            column_mapping = {
                                "rang": "Rang",
                                "sem.": "Sem.",
                                "titre": "Titre",
                                "entrées": "Entrées",
                                "variation hebdo": "Variation hebdo",
                                "variation": "Variation hebdo",  # On normalise pour que les deux variations correspondent
                                "cumul (millions)": "Cumul (Millions)",
                                "budget": "Budget",
                                "nbre de copies": "Nbre de copies",
                                "moy / copie": "Moy / copie"
                            }
                            
                            # Associer les index aux noms normalisés
                            columns = {column_mapping.get(name, name): idx for idx, name in enumerate(column_names)}
                            
                            # Liste pour stocker les données
                            data = []
                            
                            # Extraire les données
                            rows = target_table.find_all("tr")[2:]  # Ignorer la ligne des headers et des colonnes
                            
                            for row in rows:
                                cols = row.find_all("td")
                                
                                # Dictionnaire avec valeurs vides par défaut
                                film = {col_name: "" for col_name in column_mapping.values()}
                            
                            # Remplir avec les valeurs disponibles
                                for col_name, col_idx in columns.items():
                                    if col_idx < len(cols):
                                        text_value = cols[col_idx].text.strip().replace("\xa0", "")  # Supprime les espaces insécables
                                        
                                        # Si la colonne est "Titre", on garde les espaces internes
                                        if col_name == "Titre":
                                            # Remplacer les espaces multiples par un seul espace
                                            text_value = re.sub(r'\s+', ' ', text_value)
                                            film[col_name] = text_value  # Conserve les espaces internes, mais supprime les multiples
                                        else:
                                            film[col_name] = text_value.replace(" ", "")  # Supprime tous les espaces ailleurs
                            
                                # Ajouter le dictionnaire à la liste
                                data.append(film)
                            
                            # Création du DataFrame pandas
                            columns = ['Rang', 'Titre', 'Entrées', 'Variation hebdo', 'Cumul (Millions)', 'Budget', 'Nbre de copies', 'Moy / Copie']
                            
                            df = pd.DataFrame(data)
                            # Harmonisation des colonnes : ajout des colonnes manquantes et réorganisation
                            df = df.reindex(columns=columns)      
                            # On supprime les lignes vides
                            df = df[df['Titre'] != ""]
                            # Ajout du lien
                            df['Lien cd'] = url
                        
                            df['Date'] = date
                            
                            if previ == 1:
                                df['Entrées'] = ''
                        
                            df_films_to_ad = pd.concat([df_films_to_ad, df], ignore_index=True)
            
                            # Attendre 5 secondes avant de passer au site suivant
                            time.sleep(5)
                            
                        else: 
                            
                            urls0.append(url)
                            
                            
                    if len(urls0) == 2:
                        
                        print(f'Scraping date: {date}')
                        print(f"Cette semaine n'existe pas: {urls0[0]}")
        
            
            # 1.1.4: Exportation Données étape 110:
            logging.info('Exportation Données étape 110')
            
            # Historisation des données
            
            if len(df_films_to_ad) > 0: 
                if os.path.exists(os.path.join(output_folder_100, 'Films_110.xlsx')) == True:
                    shutil.move(os.path.join(output_folder_100, 'Films_110.xlsx'), os.path.join(output_folder_100, r'Historique\Films_110'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
                df_films_to_ad.to_excel(os.path.join(output_folder_100, 'Films_110.xlsx'), index=False)
                
                scraping_do = 1
                

                
        
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
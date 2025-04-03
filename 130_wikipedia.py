# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 03/03/2025

-------------------------------------------------------------------------------
                    130 Wikipedia
-------------------------------------------------------------------------------
"""

def etape130():
    
    
    etape = "130_wikipedia"
    
    
    
    now = datetime.now()
    
    # ---------- DEBUT DU JOURNAL
    logging.shutdown()
    logger, log_file = setup_logger(etape)
    logger.info("Exécution du programme démarrée.")
    print(f"Le fichier de log a été créé : {log_file}")
    # ----------
    
    
    # 1.3.1: Vérification des données
    logging.info("1.3.1: Vérification des Données")
        
    if os.path.exists(os.path.join(data_folder, 'films_cine_directors.xlsx')) == True:
        
        dossier = data_folder
        file = 'films_cine_directors.xlsx'
        
    else:
        
        print("Pas de données en input")
        
        # ---------- FIN DU JOURNAL
        #logging.critical("Exécution du programme terminée car besoin d'intervention manuelle.")
        logging.shutdown()
        # ----------
        
        sys.exit()
        
     
    # 1.2.2: Définitions des variables
    logging.info("1.2.2: Importation Données")   
        
    df_cs = pd.read_excel(_0_file_films_cd)   
    
    # On envoie les nouvelles données dans la base de données wikipedia
    
    if os.path.exists(os.path.join(data_folder, 'films_wikipedia.xlsx')) == True:
        
        df_input = pd.read_excel(_0_file_films_w)
        
        df_uniq = df_cs.drop_duplicates(subset=['Titre_key'], keep='first').copy()
    
        df_input = pd.concat([df_input, df_uniq[["Titre_key", "Titre", 'Date', 'Wiki']]], ignore_index=True)
        df_input = df_input.fillna("")
        df_input = df_input.drop_duplicates(subset=['Titre_key'], keep='first')
        
        # Export des données:
        
        df_input = df_input.sort_values(by=["Date", "Titre_key", "Wiki"], ascending=[True, True, False])    
        
    else:
        
        df_input = df[['Titre_key', 'Titre', 'Wiki']]


    df_w3 = df_input[df_input['Wiki'] == 3]
    df_w2 = df_input[df_input['Wiki'] == 2]
    df_w1 = df_input[df_input['Wiki'] == 1]
    df_input = df_input[df_input['Wiki'] == 0]
    
    if len(df_input) == 0: 
        
        print("Pas de données wikipedia à scraper")
        
    else:
        
        df_input = df_input[["Titre_key", "Titre", "Date"]]
        
        df_input = df_input.drop_duplicates(subset=["Titre"], keep="first")
        
        # Conversion en dates
        df_input['Date'] = pd.to_datetime(df_input['Date'])
        
        df_input['Année'] = df_input['Date'].dt.year
        df_input['Année-1'] = df_input['Date'].dt.year - 1
        
        remplacements = str.maketrans({
            "'": "%27",
            "?": "%3F"
        })
        
        df_input['Titre_link'] = df_input['Titre'].str.translate(remplacements)
        df_input['Titre_link'] = df_input['Titre_link'].str.replace(r'\s*\([^)]*\)', '', regex=True)
        
        df_input['Titre_link2'] = df_input['Titre_link'].apply(capitalize_title).apply(capitalize_first_letter)
    
        df_input['Titre_link3'] = df_input['Titre_link'].apply(capitalize_first_non_excluded)
        
        df_input['Titre_link4'] = df_input['Titre_link'].str.replace('&','and')
        df_input['Titre_link5'] = df_input['Titre_link2'].str.replace('&','and')
        df_input['Titre_link6'] = df_input['Titre_link3'].str.replace('&','and')
        
        df_input['Titre_link7'] = df_input['Titre_link'].str.replace('&','et')
        df_input['Titre_link8'] = df_input['Titre_link2'].str.replace('&','et')
        df_input['Titre_link9'] = df_input['Titre_link3'].str.replace('&','et')
        
        df_input['Titre_link10'] = df_input['Titre_link'].str.replace('-',':')
        df_input['Titre_link11'] = df_input['Titre_link2'].str.replace('-',':')
        df_input['Titre_link12'] = df_input['Titre_link3'].str.replace('-',':')
        df_input['Titre_link10'] = df_input['Titre_link4'].str.replace('-',':')
        df_input['Titre_link11'] = df_input['Titre_link5'].str.replace('-',':')
        df_input['Titre_link12'] = df_input['Titre_link6'].str.replace('-',':')
        df_input['Titre_link10'] = df_input['Titre_link7'].str.replace('-',':')
        df_input['Titre_link11'] = df_input['Titre_link8'].str.replace('-',':')
        df_input['Titre_link12'] = df_input['Titre_link9'].str.replace('-',':')
        
        df_input['Titre_link13'] = df_input['Titre_link'].str.replace('-',':')
        df_input['Titre_link14'] = df_input['Titre_link2'].str.replace('-',':')
        df_input['Titre_link15'] = df_input['Titre_link3'].str.replace('-',':')
        df_input['Titre_link16'] = df_input['Titre_link4'].str.replace('-',':')
        df_input['Titre_link17'] = df_input['Titre_link5'].str.replace('-',':')
        df_input['Titre_link18'] = df_input['Titre_link6'].str.replace('-',':')
        df_input['Titre_link19'] = df_input['Titre_link7'].str.replace('-',':')
        df_input['Titre_link20'] = df_input['Titre_link8'].str.replace('-',':')
        df_input['Titre_link21'] = df_input['Titre_link9'].str.replace('-',':')
        df_input['Titre_link22'] = df_input['Titre_link10'].str.replace('-',':')
        df_input['Titre_link23'] = df_input['Titre_link11'].str.replace('-',':')
        df_input['Titre_link24'] = df_input['Titre_link12'].str.replace('-',':')
        

        
        def clean_company_name(text):
            """ Nettoie le nom de la société en supprimant les détails inutiles. """
            if pd.isna(text) or not isinstance(text, str):
                return None
        
            # Supprimer tout ce qui est entre parenthèses
            text = re.sub(r"\(.*?\)", "", text)
            
            # Garder uniquement la première valeur avant une virgule ou un deux-points
            text = re.split(r"[:,]", text)[0]
            
            return text.strip()
        
                 
        def scrape_movie_info(pre_urls, years):
            
            global results
            
            # Définition des expressions régulières pour les différentes catégories
            production_pattern = re.compile(r"Société[s]? de production[s]?\s*(?:\[\d+\])?:", re.IGNORECASE)
            production_pattern_alternate = re.compile(r"Production[s]?\s*(?:\[\d+\])?\s*:", re.IGNORECASE)
            distribution_pattern = re.compile(r"(?:Société[s]? de distribution|Distributeur[s]?|Distribution[s]?)\s*(?:\([^)]*\))?\s*.*\s*:", re.IGNORECASE)
            budget_pattern = re.compile(r"Budget\s*:", re.IGNORECASE)
            duration_pattern = re.compile(r"Durée\s*:", re.IGNORECASE)
            style_pattern = re.compile(r"Genre[s]?\s*:", re.IGNORECASE)
            real_pattern = re.compile(r"(?:Réalisation[s]?|Réalisateur).*:", re.IGNORECASE)
            country_pattern = re.compile(r"(?:Pays d[’']origine|Pays de production|Pays).*:", re.IGNORECASE)
        
            results = {
                "Réalisateur": None,
                "Acteur Principal": None,
                "Acteur Secondaire": None,
                "Durée": None,
                "Studio de Production": None,
                "Société de Distribution": "Non renseignée",
                "Budget": None,
                "Style": None,
                "Lien Wiki": None,
                "Pays": None,
                "Wiki": 2
            }
            
            urls = []
            
            for pre_url in pre_urls:
                
                for year in years:
                
                    urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().replace(' ', '_') + '_(film,_' + str(year) + ')#Fiche_technique')
                    urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().title().replace(' ', '_') + '_(film,_' + str(year) + ')#Fiche_technique')
                    
                urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().replace(' ', '_') + '_(film)#Fiche_technique')
                urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().title().replace(' ', '_') + '_(film)#Fiche_technique')            
                urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().replace(' ', '_') + '#Fiche_technique')  
                urls.append('https://fr.wikipedia.org/wiki/' + pre_url.strip().title().replace(' ', '_') + '#Fiche_technique')    
                
                
            # On supprime les doublons de la liste
            urls = list(dict.fromkeys(urls))          
            
            # Tester chaque lien jusqu'à en trouver un valide
            for url in urls:
                
                response = requests.get(url)
                if response.status_code == 200:
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Trouver toutes les balises <li>
                    li_tags = soup.find_all('li')
                    
                    # Extraire le texte de chaque balise <li> et les stocker dans une liste
                    li_textes = [li.get_text(strip=True) for li in li_tags]
                    
                    # Créer un DataFrame à partir de la liste
                    df_li = pd.DataFrame(li_textes, columns=['Texte des balises li']) 
                    
                    scrap=1
                    print(f"Scrapping : {url}")
                    
                    
                    # Société de production
                    companies = df_li[df_li['Texte des balises li'].str.contains(production_pattern, na=False, regex=True)]
                    
                    # Si aucun résultat, on teste avec le deuxième pattern
                    if len(companies) == 0:
                        companies = df_li[df_li['Texte des balises li'].str.contains(production_pattern_alternate, na=False, regex=True)]

                    if len(companies) > 0:
                        companies = companies.iloc[:1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.strip()
                        raw_text = companies.iloc[0, 0]
                        if pd.isna(raw_text):  # Vérifie si c'est NaN
                            raw_text = ""
                        if isinstance(raw_text, str):  # Vérifie si c'est une chaîne avant d'utiliser .split()
                            raw_text = raw_text.split(':', 1)[-1].strip()
                            clean_text = clean_company_name(raw_text)
                            clean_text = re.sub(r"\(.*?\)", "", clean_text).strip()
                            clean_text = re.split(r",|et|;", clean_text)[0].strip()
                            clean_text = clean_text.split('-')[0].strip()  # Ne garde que le premier élément avant "-"
                            results["Studio de Production"] = clean_text
                    
                    
                    # Société de distribution
                    companies = df_li[df_li['Texte des balises li'].str.contains(distribution_pattern, na=False)]
                    if len(companies) > 0:
                        companies = companies.iloc[:1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.strip()
                        raw_text = companies.iloc[0, 0]
                    
                        if pd.isna(raw_text):  # Vérifie si c'est NaN
                            raw_text = ""
                    
                        if isinstance(raw_text, str):  # Vérifie si c'est une chaîne avant d'utiliser .split()
                            raw_text = raw_text.split(':', 1)[-1].strip()
                    
                            # Recherche si "(France)" est avant la société
                            match = re.search(r"(.+?)\s*\(France\)", raw_text)
                            if match:
                                clean_text = match.group(1).strip()  # Prend la société juste avant "(France)"
                            else:
                                # Si "(France)" n'est pas trouvé, on prend la première société
                                clean_text = re.split(r",|et|;", raw_text)[0].strip()
                    
                            clean_text = clean_company_name(clean_text)
                            clean_text = re.sub(r"\(.*?\)", "", clean_text).strip()  # Supprime les parenthèses restantes
                            clean_text = clean_text.split('-')[0].strip()  # Ne garde que le premier élément avant "-"
                            results["Société de Distribution"] = clean_text
                    
                    # Durée
                    companies = df_li[df_li['Texte des balises li'].str.contains(duration_pattern, na=False)]
                    if len(companies) > 0:
                        companies = companies.iloc[:1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.strip()
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'\(.*?\)', '', regex=True)
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'\[.*?\]', '', regex=True)
                    
                        # Extraction de la durée avec différents formats
                        duration_text = companies.iloc[0, 0]
                    
                        # ✅ Solution : Convertir en string si nécessaire
                        duration_text = str(duration_text) if not pd.isna(duration_text) else ""
                    
                        # Cas "1h40" ou "2h 15"
                        match_hm = re.search(r'(\d+)h\s*(\d*)', duration_text)
                        if match_hm:
                            heures = int(match_hm.group(1))
                            minutes = int(match_hm.group(2)) if match_hm.group(2) else 0
                            duration = heures * 60 + minutes
                        else:
                            # Cas "100 minutes"
                            match_min = re.search(r'(\d+)\s*minutes?', duration_text, re.IGNORECASE)
                            if match_min:
                                duration = int(match_min.group(1))
                            else:
                                duration = None  # Valeur par défaut si la durée n'est pas trouvée
                    
                        results["Durée"] = duration
                    
                  # Budget
                    companies = df_li[df_li['Texte des balises li'].str.contains(budget_pattern, na=False)]
                    budget = None  # Initialisation de budget pour éviter une erreur
                    if len(companies) > 0:
                        companies = companies.iloc[:1]  # On prend uniquement la première ligne trouvée
                        
                        # Extraction du texte après ":"
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(';', n=1).str[0]
                        
                        # Vérification de la présence des mots-clés avec une expression régulière sans groupes de capture
                        million = 1  # Initialisation de la variable
                        if companies['Texte des balises li'].str.contains(r'(?:millions|million)', case=False).any():
                            million = 1000000  
                            
                        if companies['Texte des balises li'].str.contains(r'(?:M)', case=True).any():
                            million = 1000000         
                            
                        # Supprimer les parenthèses et leur contenu
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"\(.*?\)", "", regex=True)
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"\[.*?\]", "", regex=True)
                            
                        # On garde tout avant "million", "millions" ou "M", en excluant ces mots
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'(.*?)\s*(millions|million|M)\b.*', r'\1', regex=True, case=False)
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'(.*?)\s*M\b.*', r'\1', regex=True)    
                        
                        # On transforme "et", "à", "and","/" en "-"
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"et|and|à|a|/", "-", regex=True)
                        
                        # On transforme "un " en "1"
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"\bun\b", "1", regex=True)
                        
                        # Suppression des références et caractères non numériques (hors chiffres et virgules)
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'[^0-9,-]', '', regex=True)
                        
                        # Si une virgule est présente, on transforme les chiffres en format décimal
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(',', '.', regex=False)
                        
                        # Cas où il y a une plage de budget "X-Y millions" ou "X-Y millions $"
                        match = re.search(r'(\d+[,.]?\d*)\s*-\s*(\d+[,.]?\d*)', companies.iloc[0, 0])
                        if match:
                            # On fait la moyenne des deux valeurs
                            min_budget = float(match.group(1).replace(',', '.')) * million  # Remplacer la virgule par un point pour la conversion en float
                            max_budget = float(match.group(2).replace(',', '.')) * million  # Remplacer la virgule par un point pour la conversion en float
                            budget = (min_budget + max_budget) // 2  # Moyenne arrondie
                        else:
                            # Si pas de plage, on convertit directement la valeur restante en nombre
                            try:
                                value = float(companies['Texte des balises li'].iloc[0])
                                budget = int(value * million)  # Multiplier par 1 million si on parle en million
                            except ValueError:
                                pass  # Si la conversion échoue, le budget reste None
                    
                    results["Budget"] = budget  
                            
                        
                    # Style
                    companies = df_li[df_li['Texte des balises li'].str.contains(style_pattern, na=False)]
                    if len(companies) > 0:
                        companies = companies.iloc[:1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.strip()
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.lower()
    
                        mask_super_hero = companies['Texte des balises li'].str.contains(r'super[\s-]?héros', regex=True, na=False)
                    
                        companies.loc[mask_super_hero, 'Texte des balises li'] = "Super Héros"
                        companies.loc[~mask_super_hero, 'Texte des balises li'] = companies.loc[~mask_super_hero, 'Texte des balises li'].str.split(',').str[0]
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r'^\w', lambda x: x.group(0).upper(), regex=True)
                    
                        results['Style'] = companies.iloc[0,0]
                        
                    # Réalisation
                    companies = df_li[df_li['Texte des balises li'].str.contains(real_pattern, na=False)]
                    if len(companies) > 0:
                        companies = companies.iloc[:1]
                        companies.loc[:, 'Texte des balises li'] = companies['Texte des balises li'].str.split(':', n=1).str[1]
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.strip()
                    
                        # Supprimer les parenthèses et leur contenu
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"\(.*?\)", "", regex=True)
                        companies['Texte des balises li'] = companies['Texte des balises li'].str.replace(r"\[.*?\]", "", regex=True)
                    
                        # Séparation avec ",", " et ", ou " d'après "
                        clean_text = re.split(r"\s*(?:,|et|d'après)\s*", companies.iloc[0, 0])[0].strip()
                    
                        results["Réalisateur"] = clean_text
                        
                        
                    # Acteurs principaux et secondaires
                    actors_section = soup.find("h2", id="Distribution")
                    # Nettoyage des noms d'acteurs pour supprimer "(VBF)" et "(VB)"
                    clean_actor = lambda x: re.sub(r'\(.*', '', x).strip()
                    
                    if actors_section:
                        actors_list = actors_section.find_next("ul").find_all("li")
                        actors = [li.get_text(strip=True).split(":")[0] for li in actors_list if ":" in li.get_text()]
                        
                        if len(actors) > 0:
                            results["Acteur Principal"] = clean_actor(actors[0])  # Premier acteur
                            results["Acteur Secondaire"] = clean_actor(actors[1]) if len(actors) > 1 else None  # Deuxième acteur s'il existe
            
            
                    # Pays de production
                    production_country = df_li[df_li['Texte des balises li'].str.contains(country_pattern, na=False)]
                    if len(production_country) > 0:
                        production_country = production_country.iloc[0, 0]  # Prendre la première occurrence
                        production_country = production_country.split(":")[-1].strip()  # Extraire le pays après ":"
                        production_country = re.sub(r"\(.*?\)", "", production_country).strip()  # Supprimer les parenthèses et leur contenu
                        production_country = re.sub(r"\[.*?\]", "", production_country).strip()  # Supprimer les crochets et leur contenu
                        production_country = re.sub(r"\d+|%", "", production_country).strip()  # Supprimer les nombres et les %
                        production_country = re.split(r",|et|/|—|•|\s|\.", production_country)[0].strip()
                    
                        # Vérifier s'il y a un "-"
                        if "-" in production_country.lower() and production_country.lower() not in ["états-unis", "royaume-uni"]:
                            production_country = production_country.split("-")[0].strip()  # Prendre le premier mot avant "-"
                    
                        # Vérifier si le texte est entièrement en majuscules
                        if not production_country.isupper():
                            production_country = production_country.capitalize()  # Mettre uniquement la première lettre en majuscule
                            
                        results["Pays"] = production_country
                            
                        
                    results["Wiki"] = 1
            
                    results["Lien Wiki"] = url
                    
                    # Attendre 5 secondes avant de passer au site suivant
                    time.sleep(5)
                    
                    break
                
                
                    
            return results
            
        
        df_input.loc[:, ["Réalisateur", 
                         "Acteur Principal", 
                         "Acteur Secondaire", 
                         "Durée",
                         "Studio de Production", 
                         "Société de Distribution", 
                         "Budget",
                         "Style", 
                         "Lien Wiki", 
                         "Pays", 
                         "Wiki"]] = df_input.progress_apply(lambda row: pd.Series(scrape_movie_info(
                        [
                                row['Titre_link'], row['Titre_link2'], row['Titre_link3'], row['Titre_link4'], 
                                row['Titre_link5'], row['Titre_link6'], row['Titre_link7'], row['Titre_link8'],
                                row['Titre_link9'], row['Titre_link10'], row['Titre_link11'], row['Titre_link12'], 
                                row['Titre_link13'], row['Titre_link14'], row['Titre_link15'], row['Titre_link16'], 
                                row['Titre_link17'], row['Titre_link18'], row['Titre_link19'], row['Titre_link20'], 
                                row['Titre_link21'], row['Titre_link22'], row['Titre_link23'], row['Titre_link24']
                        ],
                        [
                            row['Année'],
                            row['Année-1']
                        ])), 
                    axis=1
                ) 
            
                      
        
    
        # Liste des colonnes à supprimer
        cols_to_drop = [f"Titre_link{i}" for i in range(2, 25)] + ["Titre_link","Année", "Année-1"]
                
        # Suppression des colonnes
        df = df_input.drop(cols_to_drop, axis=1)
        
        df = df[["Titre_key",
                 "Titre", 
                 "Réalisateur", 
                 "Acteur Principal", 
                 "Acteur Secondaire", 
                 "Durée", 
                 "Studio de Production", 
                 "Société de Distribution", 
                 "Style", 
                 "Date",
                 "Pays",
                 "Budget",
                 "Lien Wiki",
                 "Wiki"]]
        
        # A AMELIORER
        df['Date de sortie'] = df['Date']
    
        
        
    
        # 1.3.4: Exportation Données étape 130:
        logging.info('Exportation Données étape 130')
        
        if os.path.exists(os.path.join(output_folder_100, 'Films_130.xlsx')) == True:
            shutil.move(os.path.join(output_folder_100, 'Films_130.xlsx'), os.path.join(output_folder_100, r'Historique/Films_130'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        df.to_excel(os.path.join(output_folder_100, 'Films_130.xlsx'), index=False)
        
        
        # On complète la base de données wikipedia
        
        df_w = pd.concat([df_w1, df, df_w2, df_w3], ignore_index=True)
        df_w = df_w.sort_values(by=['Wiki', 'Date', 'Titre'], ascending=[False, True, True])
    
        if os.path.exists(_0_file_films_w) == True:
            shutil.move(_0_file_films_w, os.path.join(data_folder, r'Historique/films_wikipedia'+f'_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}'+'.xlsx'))
        df_w.to_excel(_0_file_films_w, index=False)
    
        
        
        logger.info('Données scrapées')
        print('Données scrapées')
        
        
    # ---------- FIN DU JOURNAL
    logging.info("Exécution du programme terminée.")
    logging.shutdown()
    # ----------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
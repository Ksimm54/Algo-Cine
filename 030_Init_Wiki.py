# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 03/03/2025

-------------------------------------------------------------------------------
                    030 Init_Wiki
-------------------------------------------------------------------------------
"""
   

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


etape = "030_Init_Wiki"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------



# Création de la base de données wikipedia à partir de la base de données des films:
    
# Import des données

df = pd.read_excel(os.path.join(data_folder, 'Films.xlsx'))

df_w = df[['Titre',
           'Réalisateur',
           'Acteur Principal',
           'Acteur Secondaire',
           'Durée',
           'Studio de Production',
           'Société de Distribution',
           'Style',
           'Date de sortie',
           'Pays',
           'Budget']].copy()

# Variable clé
df_w.loc[:, "Titre_key"] = (
    df_w["Titre"]
    .apply(lambda x: unidecode(x.lower()) if isinstance(x, str) else x)  
    .str.replace(r"\W+", "", regex=True)
)

df_w['Lien Wiki'] = ""
df_w['Wiki'] = 1
df_w['Date'] = df_w['Date de sortie']

df_w = df_w[['Titre_key',
           'Titre',
           'Réalisateur',
           'Acteur Principal',
           'Acteur Secondaire',
           'Durée',
           'Studio de Production',
           'Société de Distribution',
           'Style',
           'Date de sortie',
           'Date',
           'Pays',
           'Budget',
           'Lien Wiki',
           'Wiki']]

# Export de la base de données

df_w.to_excel(os.path.join(data_folder, 'films_wikipedia.xlsx'), index=False)

print("Base de données: films_wikipedia.xlsx générée")














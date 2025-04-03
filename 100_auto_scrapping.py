# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 14/02/2024

-------------------------------------------------------------------------------
                    100 Auto Scrapping
-------------------------------------------------------------------------------
"""

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



etape = "100_Auto_Scrapping"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------


with open(prog_folder+r"\110_cine_directors.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\120_traitement_cine_directors.py", encoding="utf-8") as file:
    exec(file.read())  

with open(prog_folder+r"\130_wikipedia.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\140_films_youtube.py", encoding="utf-8") as file:
    exec(file.read())
    
with open(prog_folder+r"\150_traitement_youtube.py", encoding="utf-8") as file:
    exec(file.read())
    
with open(prog_folder+r"\160_to_input.py", encoding="utf-8") as file:
    exec(file.read())


# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------



# Lancement de l'étape 110
etape110()
logger.info('Programme 110_cine_directors.py exécuté')
  
# Lancement de l'étape 120
etape120()
logger.info('Programme 120_traitement_cine_directors.py exécuté')

# Lancement de l'étape 130
etape130()
logger.info('Programme 130_wikipedia.py exécuté')

# Lancement de l'étape 140
etape140()
logger.info('Programme 140_films_youtube.py exécuté')

# Lancement de l'étape 150
etape150()
logger.info('Programme 150_traitement_youtube.py exécuté')

# Lancement de l'étape 160
etape160()
logger.info('Programme 160_to_input.py exécuté')







































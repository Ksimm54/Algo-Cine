# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/12/2024

-------------------------------------------------------------------------------
                    200 Import données
-------------------------------------------------------------------------------
"""

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



etape = "200_Auto_Import"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------


with open(prog_folder+r"\210_complement_donnees_films.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\220_reals_acts_check.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\230_ajouts_labels.py", encoding="utf-8") as file:
    exec(file.read())  

with open(prog_folder+r"\240_date_infos.py", encoding="utf-8") as file:
    exec(file.read())  

with open(prog_folder+r"\250_valeurs_manquantes.py", encoding="utf-8") as file:
    exec(file.read())  

with open(prog_folder+r"\260_ajout_donnees_freq.py", encoding="utf-8") as file:
    exec(file.read())  

with open(prog_folder+r"\270_Export.py", encoding="utf-8") as file:
    exec(file.read())  


# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------

# Lancement de l'étape 210: Ajouter des films aux données
etape210()
logger.info('Programme 210_complement_donnees_films.py exécuté')

# Lancement de l'étape 220: Données réals et acteurs à compléter
etape220()
logger.info('Programme 220_reals_acts_check.py exécuté')
  
# Lancement de l'étape 230: Ajout des labels
etape230()
logger.info('Programme 230_ajouts_labels.py exécuté')

# Lancement de l'étape 240: Date infos
etape240()
logger.info('Programme 240_date_infos.py exécuté') 

# Lancement de l'étape 250: Export
etape250()
logger.info('Programme 250_valeurs_manquantes.py exécuté') 

# Lancement de l'étape 260: Export
etape260()
logger.info('Programme 260_ajout_donnees_freq.py exécuté') 

# Lancement de l'étape 270: Export
etape270()
logger.info('Programme 270_Export.py exécuté') 
    







































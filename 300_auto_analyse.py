# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/01/2025

-------------------------------------------------------------------------------
                    300 Auto Analyse
-------------------------------------------------------------------------------
"""

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



etape = "300_Auto_Analyse"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------


with open(prog_folder+r"\310_check_conditions_etape2.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\320_analyse_vars_qual.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\330_analyse_vars_quan.py", encoding="utf-8") as file:
    exec(file.read())

    

# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------

# Lancement de l'étape 310: Check conditions étape 2
etape310()
logger.info('Programme 310_check_conditions_etape2.py exécuté')

# Lancement de l'étape 320: Analyse variables qualitatives
etape320()
logger.info('Programme 320_analyse_vars_qual.py exécuté')

# Lancement de l'étape 330: Analyse variables qualitatives
etape330()
logger.info('Programme 330_analyse_vars_quan.py exécuté')
  









































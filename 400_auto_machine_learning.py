# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 20/01/2025

-------------------------------------------------------------------------------
                    400 Auto Machine Learning
-------------------------------------------------------------------------------
"""

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



etape = "400_auto_machine_learning"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------


with open(prog_folder+r"\410_check_conditions_etape3.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\420_randomForest.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\430_regressionLasso.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\440_regressionRidge.py", encoding="utf-8") as file:
    exec(file.read())

with open(prog_folder+r"\450_elasticNet.py", encoding="utf-8") as file:
    exec(file.read())

#with open(prog_folder+r"\460_reseau_de_neurones.py", encoding="utf-8") as file:
#    exec(file.read())

with open(prog_folder+r"\470_hist_preds.py", encoding="utf-8") as file:
    exec(file.read())


# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------

# Lancement de l'étape 410: Check conditions étape 2
etape410()
logger.info('Programme 410_check_conditions_etape3.py exécuté')

# Lancement de l'étape 420: Random Forest
etape420()
logger.info('Programme 420_randomForest.py exécuté')

# Lancement de l'étape 430: Regression Lasso
etape430()
logger.info('Programme 430_regressionLasso.py exécuté')

# Lancement de l'étape 440: Regression Ridge
etape440()
logger.info('Programme 440_regressionRidge.py exécuté')

# Lancement de l'étape 450: Elastic Net
etape450()
logger.info('Programme 450_elasticNet.py exécuté')

# Lancement de l'étape 460: Réseau de Neuronnes
#etape460()
#logger.info('Programme 460_reseau_de_neurones.py exécuté')

# Lancement de l'étape 470: Historisation des prédictions
etape470()
logger.info('Programme 470_hist_preds.py exécuté')













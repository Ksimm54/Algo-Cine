# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 18/12/2024

-------------------------------------------------------------------------------
                    Init
-------------------------------------------------------------------------------
"""

etape = "000_init"


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import os
from pathlib import Path

from unidecode import unidecode

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import shutil

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.worksheet.filters import AutoFilter

import sys
import seaborn as sns

from scipy.stats import f_oneway
from scipy.stats import kruskal
from scipy.stats import pearsonr
from scipy.stats import spearmanr

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

#import tensorflow as tf
#from tensorflow import keras
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense
#from tensorflow.keras.optimizers import Adam
#from tensorflow.keras.layers import Input

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import requests
from io import BytesIO
import time
import base64
import codecs

from tqdm import tqdm
tqdm.pandas(desc='Traitement en cours')



now = datetime.now()


my_path = r"C:\Users\User\Documents\Algo Ciné"

prog_folder = os.path.join(my_path, '01_Programmes')
data_folder = os.path.join(my_path, '02_Data')
input_folder = os.path.join(my_path, '03_Input')
log_folder = os.path.join(my_path, '04_Log')
output_folder = os.path.join(my_path, '05_Output')
images_folder = os.path.join(my_path, '06_Images/300_images')

log_hist_folder = os.path.join(log_folder, 'Historique')
output_folder_100 = os.path.join(output_folder, '100_Scrapping')
output_folder_200 = os.path.join(output_folder, '200_Import')
output_folder_300 = os.path.join(output_folder, '300_Analyse')
output_folder_400 = os.path.join(output_folder, '400_Machine_Learning')
to_complete_folder = os.path.join(input_folder, 'A CORRIGER')

# Définition des fichiers

_0_file_param_variables = data_folder+"/param_variables.xlsx"
_0_sheet_importance_metier = "importance_metier"
_0_sheet_date_import_cd = "100_Date_Import_Cine_Directors"
_0_sheet_date_import_y = "100_Date_Import_Youtube"
_0_sheet_token = "100_Token"
_0_sheet_date_to_pred = "200_Date_to_pred"
_0_sheet_api_key = "100_API_KEY"

_0_file_films_youtube = data_folder + "/films_youtube.xlsx"

_0_file_films_cd = data_folder + "/films_cine_directors.xlsx"

_0_file_films_w = data_folder + "/films_wikipedia.xlsx"

_0_file_keys_wy = data_folder + "/keys_w_y.xlsx"

_0_file_acteurs = data_folder + "/Acteurs.xlsx"

_0_file_realisateurs = data_folder + "/Réalisateurs.xlsx"

_0_file_films = data_folder + "/Films.xlsx"

_0_file_films_images = data_folder + "/Films_Images.xlsx"

_0_file_frequentation_cinema = data_folder + "/Fréquentation et films dans les salles de cinéma.xlsx"

_0_file_labels = data_folder + "/Table de correspondance.xlsx"
_0_sheet_chaines_y = "100_Chaines_Youtubes"
_0_sheet_realisateurs = "200_Réalisateurs"
_0_sheet_acteurs = "200_Acteurs"
_0_sheet_nostalgie = "Nostalgique"
_0_sheet_hype = "Niveau de Hype"
_0_sheet_public_monde = "Public Monde"

_0_file_to_complete = to_complete_folder + "/films_a_completes.xlsx"

_0_file_films_to_ad = input_folder + "/films_to_ad.xlsx"

_0_file_date_a_completer = to_complete_folder + "/dates_a_completer.xlsx"


with open(prog_folder+r"\010_fonctions.py", encoding='utf-8') as file:
    exec(file.read())  
    

    
# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logging.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------


logger.info("Librairies importées")

logger.info(f"VAR : now = {now}")
logger.info(f"VAR : my_path = {my_path}")
logger.info(f"VAR : data_foler = {data_folder}")
logger.info(f"VAR : log_folder = {log_folder}")
logger.info(f"VAR : prog_folder = {prog_folder}")
logger.info(f"VAR : output_folder = {output_folder}")
logger.info(f"VAR : output_folder_100 = {output_folder_100}")
logger.info(f"VAR : output_folder_200 = {output_folder_200}")
logger.info(f"VAR : input_folder = {input_folder}")
logger.info(f"VAR : to_complete_folder = {to_complete_folder}")

logger.info("Fichier des fonctions importé")


# Avant de traiter les logs on historise les logs des anciens jours
logger.info('Historisation des logs des anciens jours')
# Parcourir les fichiers dans le dossier source
for filename in os.listdir(log_folder):
    # Vérifier si le fichier est un fichier texte
    if filename.endswith(".txt"):
        file_path = os.path.join(log_folder, filename)
        
        # Obtenir la date de modification du fichier
        file_mod_time = os.path.getmtime(file_path)
        file_mod_date = datetime.fromtimestamp(file_mod_time).date()

        # Si la date de modification est antérieure à la date du jour
        if file_mod_date < now.date():
            # Copier le fichier dans le dossier d'archive
            shutil.move(file_path, os.path.join(log_hist_folder, filename))
            logger.info(f"Fichier '{filename}' archivé.")
        else:
            logger.info(f"Fichier '{filename}' non archivé, date trop récente.")


# Si c'est la première éxécution de la journée alors le nombre de Token est réinitialisé
if len(os.listdir(log_folder)) < 3:
    
    token_df = pd.read_excel(_0_file_param_variables, sheet_name = _0_sheet_token)
    token_df['Nb Token'] = 10000

    with pd.ExcelWriter(_0_file_param_variables, mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
        token_df.to_excel(writer, sheet_name=_0_sheet_token, index=False)



# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------





















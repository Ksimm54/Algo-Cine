# -*- coding: utf-8 -*-
"""
Projet Ciné Portfolio
Créateur: Arthur BODY
Date : 12/02/2024

-------------------------------------------------------------------------------
                    999 Interface
-------------------------------------------------------------------------------
"""

my_path = r"C:\Users\User\Documents\Algo Ciné"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
with open(my_path+r"\01_Programmes\000_INIT.py", encoding="utf-8") as file:
    exec(file.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



etape = "999_Interface"



now = datetime.now()

# ---------- DEBUT DU JOURNAL
logging.shutdown()
logger, log_file = setup_logger(etape)
logger.info("Exécution du programme démarrée.")
print(f"Le fichier de log a été créé : {log_file}")
# ----------




import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

# Fonction pour exécuter les programmes et afficher la sortie
def run_program(command, output_widget, status_label):
    # Afficher le message d'exécution
    status_label.config(text="Le programme est en cours d'exécution...", fg="blue")
    status_label.update()  # Mettre à jour immédiatement l'affichage

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        output_widget.insert(tk.END, line)
        output_widget.yview(tk.END)
    process.wait()

    # Quand le programme est terminé, mettre à jour le message
    status_label.config(text="Le programme est terminé.", fg="green")
    status_label.update()

# Fonction pour démarrer un programme dans un thread pour ne pas bloquer l'interface
def start_program(command, output_widget, status_label):
    thread = threading.Thread(target=run_program, args=(command, output_widget, status_label))
    thread.start()

# Fonction pour créer et afficher l'interface graphique
def create_interface():
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Interface de Contrôle")

    # Zone de texte pour afficher les sorties
    output_box = scrolledtext.ScrolledText(root, width=80, height=20)
    output_box.pack(padx=10, pady=10)

    # Label pour afficher l'état de l'exécution
    status_label = tk.Label(root, text="Prêt à exécuter un programme", fg="black")
    status_label.pack(pady=5)

    # Commandes pour les programmes (à adapter avec vos propres commandes)
    program2 = ["python", prog_folder+r"\200_auto_import.py"]
    program3 = ["python", prog_folder+r"\300_auto_analyse.py"]
    program4 = ["python", prog_folder+r"\400_auto_machine_learning.py"]
    open_powerbi = [my_path+r"\ML Box Office France.pbix"]

    # Boutons pour lancer les programmes
    btn_program2 = tk.Button(root, text="Lancer Programme 2", command=lambda: start_program(program2, output_box, status_label))
    btn_program2.pack(pady=5)

    btn_program3 = tk.Button(root, text="Lancer Programme 3", command=lambda: start_program(program3, output_box, status_label))
    btn_program3.pack(pady=5)

    btn_program4 = tk.Button(root, text="Lancer Programme 4", command=lambda: start_program(program4, output_box, status_label))
    btn_program4.pack(pady=5)

    btn_open_powerbi = tk.Button(root, text="Ouvrir Power BI", command=lambda: subprocess.Popen(open_powerbi))
    btn_open_powerbi.pack(pady=5)

    # Lancer l'interface graphique
    root.mainloop()

# Lancer l'interface
if __name__ == "__main__":
    create_interface()



# ---------- FIN DU JOURNAL
logging.info("Exécution du programme terminée.")
logging.shutdown()
# ----------
    
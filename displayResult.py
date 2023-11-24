import tkinter as tk
from tkinter import ttk
import database

tree = None  # Global



def create_result_window():
    global tree  #pour definir global
    #cree nouvelle fenetre avec titre
    window = tk.Tk()
    window.title("TRAINING : AFFICHAGE")
    window.configure(bg='#8aded5')

    #pour gere la taille de fenetre
    window.geometry("1300x700")
    

    #titre
    lbl_title = tk.Label(window, text="TRAINING : AFFICHAGE", font=("Arial",16))
    lbl_title.grid(row=0,column=0, columnspan=8, pady=(0,20))

    #pour les inputs
    #Pseudo
    lbl_pseudo = tk.Label(window, text="Pseudo:")
    lbl_pseudo.grid(row=1,column=0 , sticky="e", padx=(0,60))
    entry_pseudo = tk.Entry(window)
    entry_pseudo.grid(row=1,column=1,sticky="w", padx=(0,60))

    # exercice
    lbl_exercice = tk.Label(window, text="Exercice:")
    lbl_exercice.grid(row=1,column=2, sticky="e", padx=(0,60))
    entry_exercice = tk.Entry(window)
    entry_exercice.grid(row=1,column=3,sticky="w", padx=(0,60))

    # date debut
    lbl_date_debut = tk.Label(window, text="Date debut:")
    lbl_date_debut.grid(row=1,column=4,sticky="e", padx=(0,60))
    entry_date_debut = tk.Entry(window)
    entry_date_debut.grid(row=1,column=5,sticky="w", padx=(0,60))

    # date fin
    lbl_date_fin = tk.Label(window, text="Date fin:")
    lbl_date_fin.grid(row=1,column=6,sticky="e", padx=(0,60))
    entry_date_fin = tk.Entry(window)
    entry_date_fin.grid(row=1,column=7,sticky="w", padx=(0,60))

    # button "voir result"

    btn_voir_resultat = tk.Button(window, text="Voir Resultat", command=lambda:voir_resultat())
    btn_voir_resultat.grid(row=2, padx=(0,5))

    btn_total = tk.Button(window, text="Total", command=lambda: voir_total())
    btn_total.grid(row=21, padx=(0,0))

    #les titre de tableau

    # pour cree Treeview
    tree = ttk.Treeview(window, height=20)
    tree["columns"] = ("Élevé", "Date Heure", "Temps", "Exercice", "NB OK", "Nb Trial", "% réussi")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column

    # definir les tittre et leur taille et styles
    for col in tree["columns"]:
        tree.column(col, width=150,anchor="center")
        tree.heading(col, text=col, anchor="center")

    tree.grid(row=3, column=0, columnspan=8)



    # partie total

    lbl_nblignes = tk.Label(window, text="NbLignes")
    lbl_nblignes.grid(row=22, column=0, padx=(0, 80))

    lbl_tempTotal = tk.Label(window, text="Temps total")
    lbl_tempTotal.grid(row=22, column=1, padx=(0, 100))

    lbl_nbOK = tk.Label(window, text="Nb OK")
    lbl_nbOK.grid(row=22, column=2, padx=(0, 100))

    lbl_nbTotal = tk.Label(window, text="Nb Total")
    lbl_nbTotal.grid(row=22, column=3, padx=(0, 100))

    lbl_pourcentageTotal = tk.Label(window, text="% Total")
    lbl_pourcentageTotal.grid(row=22, column=4, padx=(0, 100))






    window.mainloop()


def calculate_percentage(nb_ok, nb_trial):
    if nb_trial > 0:
        return round((nb_ok / nb_trial) * 100, 2)
    else:
        return 0



def colorize_percentage(percentage):
    #pour definir les coleurs avec %
    if percentage < 25:
        return 'red'
    elif percentage < 50:
        return 'orange'
    elif percentage < 75:
        return 'yellow'
    else:
        return 'green'


def insert_data_into_treeview(tree, values, percentage):
    color = colorize_percentage(percentage)
    row_id = tree.insert('', 'end', values=(*values, ''))
    tree.set(row_id, column="% réussi", value=f"{percentage} %")
    tree.tag_configure(row_id, background=color)
    tree.item(row_id, tags=(row_id,))

def voir_resultat():
    # connection de bd pour obtenir les donnees
    results = database.get_game_results()
    for result in results:
        nb_ok = result[4]
        nb_trial = result[5]
        percentage = calculate_percentage(nb_ok, nb_trial)
        insert_data_into_treeview(tree, result, percentage)



def voir_total():
    #...
    pass


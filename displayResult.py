import tkinter as tk
from tkinter import ttk
import database
from tkinter import messagebox  # Pour la fenêtre pop-up
from database import delete_game_result

tree = None  # Global
donnees_chargees = False  # Pour suivre si les données ont été chargées
entry_pseudo = None
entry_exercise = None



def create_result_window():
    global tree,entry_pseudo,entry_exercise,lbl_nblignes, lbl_tempTotal, lbl_nbOK, lbl_nbTotal, lbl_pourcentageTotal #pour definir global
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
    entry_exercise = tk.Entry(window)
    entry_exercise.grid(row=1,column=3,sticky="w", padx=(0,60))

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
    tree["columns"] = ("Éléve", "Date Heure", "Temps", "Exercice", "NB OK", "Nb Trial", "% réussi")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column

    # definir les tittre et leur taille et styles
    for col in tree["columns"]:
        tree.column(col, width=150,anchor="center")
        tree.heading(col, text=col, anchor="center")

    tree.grid(row=3, column=0, columnspan=8)

    # partie total

    # Toplam sonuçlar için başlık etiketleri
    tk.Label(window, text="NbLignes").grid(row=4, column=0, sticky='w')
    tk.Label(window, text="Temps total").grid(row=4, column=1, sticky='w')
    tk.Label(window, text="Nb OK").grid(row=4, column=2, sticky='w')
    tk.Label(window, text="Nb Total").grid(row=4, column=3, sticky='w')
    tk.Label(window, text="% Total").grid(row=4, column = 4, sticky="w")

    # Toplam sonuçlar için değer etiketleri
    lbl_nblignes = tk.Label(window, text="")
    lbl_nblignes.grid(row=5, column=0, sticky='w')

    lbl_tempTotal = tk.Label(window, text="")
    lbl_tempTotal.grid(row=5, column=1, sticky='w')

    lbl_nbOK = tk.Label(window, text="")
    lbl_nbOK.grid(row=5, column=2, sticky='w')

    lbl_nbTotal = tk.Label(window, text="")
    lbl_nbTotal.grid(row=5, column=3, sticky='w')

    lbl_pourcentageTotal = tk.Label(window, text="")
    lbl_pourcentageTotal.grid(row=5, column=4,sticky="w")

    # Bouton Supprimer
    btn_supprimer = tk.Button(window, text="Supprimer", command=supprimer_resultat)
    btn_supprimer.grid(row=2, column=1, padx=(0, 5))

    # Bouton Modifier
    btn_modifier = tk.Button(window, text="Modifier", command=modifier_resultat)
    btn_modifier.grid(row=2, column=2, padx=(0, 5))



    window.mainloop()



def insert_data_into_treeview(tree, values, percentage):
    color = colorize_percentage(percentage)
    row_id = tree.insert('', 'end', values=(*values, ''))
    tree.set(row_id, column="% réussi", value=f"{percentage} %")
    tree.tag_configure(row_id, background=color)
    tree.item(row_id, tags=(row_id,))

def supprimer_resultat():
    selected_item = tree.selection()[0]  # pour obtenir la selection

    pseudo = tree.item(selected_item, 'values')[0] #pour pseudo
    dateHour = tree.item(selected_item, 'values')[1] #pour date
    duration = tree.item(selected_item, 'values')[2] #pour temps
    exercise = tree.item(selected_item, 'values')[3] #pour exercise
    nbOk = tree.item(selected_item, 'values')[4] #pour nbOk
    nbTrials = tree.item(selected_item, 'values')[5] #pour nbTrials

    delete_game_result(pseudo,exercise,dateHour,duration,nbOk,nbTrials)
    tree.delete(selected_item)





def modifier_resultat():
    global update_window
    selected_item = tree.selection()[0]
    current_values = tree.item(selected_item, 'values')

    # pour ouvrir nouvelle fenetre
    update_window = tk.Toplevel()
    update_window.title("Modifier un résultat")

    update_window.geometry("400x200")

    # input pour Duration
    lbl_duration = tk.Label(update_window, text="Temps:")
    lbl_duration.pack()
    entry_duration = tk.Entry(update_window)
    entry_duration.pack()
    entry_duration.insert(0, current_values[2])  # par default value original

    # Ninput pour nbOk
    lbl_nb_ok = tk.Label(update_window, text="Nb d’essais réussi:")
    lbl_nb_ok.pack()
    entry_nb_ok = tk.Entry(update_window)
    entry_nb_ok.pack()
    entry_nb_ok.insert(0, current_values[4])  # par default value original

    # input pour NbTrials
    lbl_nb_trials = tk.Label(update_window, text="Nb total:")
    lbl_nb_trials.pack()
    entry_nb_trials = tk.Entry(update_window)
    entry_nb_trials.pack()
    entry_nb_trials.insert(0, current_values[5])  # par default value original

    # boutton mise a jour
    btn_update = tk.Button(update_window, text="Update", command=lambda: update_result(selected_item, entry_duration.get(), entry_nb_ok.get(), entry_nb_trials.get()))
    btn_update.pack()


def update_result(selected_item, new_duration, new_nb_ok, new_nb_trials):

    global update_window
    current_values = tree.item(selected_item, 'values')
    pseudo = tree.item(selected_item, 'values')[0]  # pour pseudo
    dateHour = tree.item(selected_item, 'values')[1]  # pour date
    duration = tree.item(selected_item, 'values')[2]  # pour temps
    exercise = tree.item(selected_item, 'values')[3]  # pour exercise
    nbOk = tree.item(selected_item, 'values')[4]  # pour nbOk
    nbTrials = tree.item(selected_item, 'values')[5]  # pour nbTrials


    # mise a jour de bd
    database.update_game_result(pseudo, exercise, dateHour, duration, nbOk,nbTrials, new_duration, new_nb_ok, new_nb_trials)

    # mise a jour de tkinter
    updated_values = (pseudo, exercise, dateHour, new_duration, new_nb_ok, new_nb_trials, calculate_percentage(int(new_nb_ok), int(new_nb_trials)))
    tree.item(selected_item, values=updated_values)

    refresh_treeview()

    update_window.destroy()

def refresh_treeview():
    # supprimer tous les donnees
    tree.delete(*tree.get_children())

    # mise a jour tous les donnees depuis bd
    resultats = database.get_game_results()
    for resultat in resultats:
        nb_ok = resultat[4]
        nb_essai = resultat[5]
        pourcentage = calculate_percentage(nb_ok, nb_essai)
        insert_data_into_treeview(tree, resultat, pourcentage)


def calculate_percentage(nb_ok, nb_trial):
    if nb_trial > 0:
        return round((nb_ok / nb_trial) * 100, 2)
    else:
        return 0

def convert_time_to_seconds(time_str):
    """ Convertir la chaine de temps donnée (HH:MM:SS) en secondes."""
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds



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




def voir_resultat():
    global donnees_chargees  # Déclarer la variable globale pour suivre si les données sont déjà chargées
    pseudo = entry_pseudo.get().strip()
    exercise = entry_exercise.get().strip()

    # Récupérer les résultats de la base de données en fonction des critères pseudo et exercise
    resultats = database.get_game_results(pseudo=pseudo, exercise=exercise)

    # Si aucun résultat n'est trouvé et que pseudo ou exercice est spécifié, afficher un message
    if not resultats:
        if pseudo or exercise:
            messagebox.showinfo("Information", "Aucun enregistrement trouvé pour les critères donnés.")
        else:
            # Si pseudo et exercice sont vides et que les données ont déjà été chargées, afficher un message
            if donnees_chargees:
                messagebox.showinfo("Information", "Les données sont déjà à jour.")
                return
        donnees_chargees = False
        return

    # Afficher les résultats dans le Treeview
    tree.delete(*tree.get_children())  # Nettoyer les données existantes dans le Treeview
    for resultat in resultats:
        nb_ok = resultat[4]
        nb_essai = resultat[5]
        pourcentage = calculate_percentage(nb_ok, nb_essai)
        insert_data_into_treeview(tree, resultat, pourcentage)

    donnees_chargees = True  # Marquer que les nouvelles données sont chargées




def voir_total():
    total_lignes = 0
    total_duration = 0
    total_nb_ok = 0
    total_nb_trials = 0
    total_pourcentage = 0

    for child in tree.get_children():
        values = tree.item(child, 'values')
        total_lignes += 1
        total_duration += convert_time_to_seconds(values[2])  # converdir la valauer de duration minute en second
        total_nb_ok += int(values[4])  # ajouter NbOk
        total_nb_trials += int(values[5])  # ajouter NbTrials

    # calculer la moyenne de reussit
    if total_nb_trials > 0:
        total_pourcentage = (total_nb_ok / total_nb_trials) * 100
    else:
        total_pourcentage = 0

    lbl_nblignes.config(text=f"{total_lignes}")
    lbl_tempTotal.config(text=f"{total_duration}")
    lbl_nbOK.config(text=f"{total_nb_ok}")
    lbl_nbTotal.config(text=f" {total_nb_trials}")
    lbl_pourcentageTotal.config(text=f"{total_pourcentage:.2f}")



create_result_window()
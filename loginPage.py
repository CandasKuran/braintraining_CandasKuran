import tkinter as tk
import tkinter.messagebox
import database
import hashlib

current_user = None
current_role = None
def hash_password(password):
    # avec algoritme de  SHA-256 on peut crypter le password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def login_func(window, on_success, entry_username, entry_password):
    global current_user, current_role
    # Vérifier le nom d'utilisateur et le mot de passe
    username = entry_username.get()
    password = entry_password.get()

    user_info = database.check_user(username, password)

    if user_info:
        current_user, role_id = user_info
        current_role = "Étudiant" if role_id == 1 else "Professeur"
        window.destroy()
        on_success()
    else:
        tk.messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")

def create_login_window(on_success):
    # Créer une nouvelle fenêtre pour le formulaire de connexion
    window = tk.Tk()
    window.title("Login")
    window.geometry("400x300+700+250")

    # on utilise "bind" pour continuer l'action. grace a bind on puet utiliser "enter" pour entre
    window.bind("<Return>", lambda event: login_func(window, on_success, entry_username, entry_password))

    # Configuration des couleurs
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color
    window.configure(bg=hex_color)

    # Création du titre
    lbl_title = tk.Label(window, text="        LOGIN", font=("Arial", 15), bg=hex_color)
    lbl_title.grid(row=0, column=0, columnspan=2, ipady=5, padx=20, pady=20)

    # Champ pour le nom d'utilisateur
    lbl_username = tk.Label(window, text="Nom d'utilisateur:", font=("Arial", 12), bg=hex_color)
    lbl_username.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_username = tk.Entry(window, font=("Arial", 12))
    entry_username.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Champ pour le mot de passe
    lbl_password = tk.Label(window, text="Mot de passe:", font=("Arial", 12), bg=hex_color)
    lbl_password.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_password = tk.Entry(window, font=("Arial", 12), show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Bouton pour se connecter
    btn_login = tk.Button(window, text="Connexion", command=lambda: login_func(window, on_success, entry_username, entry_password))
    btn_login.grid(row=3, column=0, padx=10, pady=20, sticky="e")

    # Bouton pour se registrer
    btn_login = tk.Button(window, text="Register",command=lambda:open_register_window())
    btn_login.grid(row=3, column=1, padx=10, pady=20, sticky="e")

    window.mainloop()

def open_register_window():
    global register_window
    # Ouvrir une nouvelle fenêtre pour le formulaire d'inscription
    register_window = tk.Toplevel()
    register_window.title("Inscription")
    register_window.geometry("450x350+700+250")

    # Configuration des couleurs
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color
    register_window.configure(bg=hex_color)
    register_window.grab_set()

    # Création des champs du formulaire
    lbl_username = tk.Label(register_window, text="Nom d'utilisateur:", font=("Arial", 12))
    lbl_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_username = tk.Entry(register_window, font=("Arial", 12))
    entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    lbl_password = tk.Label(register_window, text="Mot de passe:", font=("Arial", 12))
    lbl_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_password = tk.Entry(register_window, font=("Arial", 12), show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    lbl_password_confirm = tk.Label(register_window, text="Confirmer le mot de passe:", font=("Arial", 12))
    lbl_password_confirm.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_password_confirm = tk.Entry(register_window, font=("Arial", 12), show="*")
    entry_password_confirm.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Checkbox pour le rôle
    lbl_role = tk.Label(register_window, text="Rôle:", font=("Arial", 12))
    lbl_role.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    role_var = tk.StringVar()
    checkbox_student = tk.Radiobutton(register_window, text="Étudiant", variable=role_var, value="student", font=("Arial", 12))
    checkbox_student.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    checkbox_teacher = tk.Radiobutton(register_window, text="Professeur", variable=role_var, value="teacher", font=("Arial", 12))
    checkbox_teacher.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Bouton pour s'enregistrer
    btn_register = tk.Button(register_window, text="S'enregistrer", font=("Arial", 12),
                             command=lambda: process_registration(entry_username, entry_password,
                                                                  entry_password_confirm, role_var, register_window))
    btn_register.grid(row=5, column=1, padx=10, pady=20, sticky="e")


def process_registration(entry_username, entry_password, entry_password_confirm, role_var, register_window):
    username = entry_username.get()
    password = entry_password.get()
    password_confirm = entry_password_confirm.get()
    role = role_var.get()

    if password == password_confirm:
        register_user(username, password, role, register_window)
    else:
        tk.messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")


def register_user(username, password, role, register_window):

    if database.insert_user(username, password, role):
        tk.messagebox.showinfo("Succès", "Utilisateur enregistré avec succès!")
        register_window.destroy()
    else:
        tk.messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris ou erreur de base de données.")
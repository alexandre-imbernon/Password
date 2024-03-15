import tkinter as tk ; from tkinter import messagebox #1
import string 
import hashlib 
import json 
import random

# Fonction pour créer le mot de passe
def passwordgen(mdp): #2
    conditionsnotmet = [] #3
    if len(mdp) < 8:
        conditionsnotmet.append("Votre mot de passe doit contenir au moins 8 caractères")
    if not any(c.isupper() for c in mdp): #4
        conditionsnotmet.append("Votre mot de passe doit contenir au moins une lettre majuscule")
    if not any(c.islower() for c in mdp):
        conditionsnotmet.append("Votre mot de passe doit contenir au moins une lettre minuscule")
    if not any(c.isdigit() for c in mdp):
        conditionsnotmet.append("Votre mot de passe doit contenir au moins un chiffre")
    if not any(c in string.punctuation for c in mdp):
        conditionsnotmet.append("Votre mot de passe doit contenir au moins un caractère spécial")
    return conditionsnotmet

# Fonction pour prendre en compte les inputs de l'utilisateur
def function(event=None): #5
    mdp = entree.get()
    conditionsnotmet = passwordgen(mdp) 
    if conditionsnotmet: 
        message = "\n".join(conditionsnotmet) + "\n\nVeuillez entrer un mot de passe correct" 
        message_label.config(text=message, fg="red")
    else:
        message_label.config(text="Votre mot de passe est sécurisé", fg="green")
        hex_hash = crypt_password(mdp) #6
        result = save_password(hex_hash)
        if result == "Erreur : Mot de passe déjà existant":
            messagebox.showerror("Erreur", result)
        else:
            messagebox.showinfo("Succès", "Mot de passe crypté sauvegardé avec succès")

# Fonction pour générer un mdp aléatoire
def generer():
    longueur = 8
    caracteres = string.ascii_letters + string.digits + string.punctuation
    while True: #7
        mdp = "".join(random.choice(caracteres) for _ in range(longueur)) #8
        if (any(caractere.islower() for caractere in mdp) and
            any(caractere.isupper() for caractere in mdp) and 
            any(caractere.isdigit() for caractere in mdp) and 
            any(caractere in string.punctuation for caractere in mdp)):
            break
    entree.delete(0, tk.END)  # Supprime le contenu actuel de l'entrée
    entree.insert(0, mdp)  # Insère le nouveau mot de passe dans l'entrée
    return mdp
            
# Fonction pour crypter le mot de passe
def crypt_password(mdp):
    hash_object = hashlib.sha256()
    hash_object.update(mdp.encode())
    hex_hash = hash_object.hexdigest()
    return hex_hash

# Fonction pour sauvegarder le mot de passe dans un fichier JSON
def save_password(hex_hash):
    with open("user.json", "r") as f:
        data = json.load(f) #9
    mdp_list = data.setdefault("mdp", []) #10
    if hex_hash in mdp_list:
        return "Erreur : Mot de passe déjà existant"
    else:
        mdp_list.append(hex_hash)
    with open("user.json", "w") as f:
        json.dump(data, f)

# Fonction pour afficher les mdp sauvegardés dans JSON
def afficher_json():
    with open("user.json", "r") as fichier_json:
        loaded_json = json.load(fichier_json)
        json_str = json.dumps(loaded_json, indent=10) #11
        messagebox.showinfo("Mot de Passe Enregistrés", json_str)

# Fonction pour dissimuler et afficher le mdp
def afficher_mdp():
    if afficher.get():
        entree.config(show="")
    else:
        entree.config(show="*")

# Fenêtre Tkinter
fenetre = tk.Tk()
fenetre.geometry('500x500')
fenetre.title('Mon Générateur de Mot de Passe')

# Zone de saisie du mdp
entree = tk.Entry(fenetre, show="*")
entree.place(relx=0.5, rely=0.5, anchor="center")
entree.bind("<Return>", function) # Lie la touche <Entrée> à la zone de saisie afin de pouvoir valider sans passer par le bouton

# Label qui display les différentes erreurs liés au mdp
message_label = tk.Label(fenetre, text="")
message_label.place(relx=0.5, rely=0.35, anchor="center")

# Fonction pour dissimuler/apparaître le mdp via une checkbox
afficher = tk.IntVar()
check = tk.Checkbutton(fenetre, text="Afficher le mot de passe", variable=afficher, command=afficher_mdp)
check.place(relx=0.5, rely=0.6, anchor="center")

# Bouton pour Valider le mdp entré
bouton = tk.Button(fenetre, text="Valider le mot de passe", command=function)
bouton.place(relx=0.5, rely=0.7, anchor="center")

# Bouton pour générer aléatoirement un mdp
generate = tk.Button(fenetre, text="Génère moi un MDP", command=generer)
generate.place(relx=0.5, rely=0.8, anchor="center")

# Bouton pour afficher les entrées JSON
showme = tk.Button(fenetre, text="Afficher MDP enregistrés", command=afficher_json)
showme.place(relx=0.5, rely=0.9, anchor="center")

# Exécute la boucle principale Tkinter qui prend en compte les input utilisateurs, la boucle se termine à sa fermeture
fenetre.mainloop()

# 1: Importe le module tkinter sous l'appellation tk, et depuis le module importe les boites de message
# 2: Correspond plus loin à l'input de l'utilisateur
# 3: Initie une liste vide qui stockera les éventuelles erreurs liées au non respect du format de mdp (via append)
# 4:  # isX est une fonction pour intégrer respectivement toutes les maj/min/chiffres
        # (any) permet de faire valoir <true> n'importe quel caractère correspondant à la condition
# 5: Permet de faire fonctionner correctement <Return> sans quoi py renverrait "TypeError: function() missing 1 required positional argument: 'event'"
# 6: Si le MDP est sécurisé, le script commence automatique le cryptage du mdp et sa sauvegarde
# 7: while True oblige l'algorithme à répondre aux critères de vérificiations du mdp et ne procède pas tant qu'ils ne sont pas remplis
# 8: "".join permet de coller tous les paramètres de random choices sans espace à la suite
# 9: json.load permet de stocker en tant qu'objet json et sera reconnu comme tel
# 10: Permet de stocker un nouveau mdp si ce dernier n'est pas présent dans le dictionnaire, sans cette ligne l'ancien mdp serait écrasé par le nouveau
# 11: Converti l'objet json en chaîne de caractères et enfin, l'affiche dans la messagebox
import random
import string
import hashlib
import json

from tkinter import *
from tkinter import messagebox

fenetre = Tk()
fenetre.geometry('400x400')  # taille de la fenêtre
fenetre.title('Password')  # titre de la fenêtre
fenetre['bg'] = '#41B77F'  # couleur de fond

#ZONE DE TEXTE
label = Label(fenetre, text= "Saisir votre mot de passe", font=("Gill Sans MT", 13 , "italic bold", ),fg="white", bg="#41B77F")      #label: zone de texte qui prend en parametre la fenetre et le texte à ecrire
label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Champ mot de passe
mdp = Entry(fenetre, show="*")
mdp.pack(pady=10)
mdp.place(relx=0.5, rely=0.4, anchor=CENTER)

# Fonction qui vérifie le mot de passe
def verifier_mdp():
    mot_de_passe = mdp.get()
    caracteres_speciaux = ['!', '@', '#', '$', '%', '^', '&', '*', '.', '/', ':']

    # Liste pour stocker les types d'erreurs détectées
    message_erreurs = []

    if len(mot_de_passe) < 8:
        message_erreurs.append("Le mot de passe doit contenir au moins 8 caractères.")
    
    if not any(char.isupper() for char in mot_de_passe):
        message_erreurs.append("Le mot de passe doit contenir au moins une lettre majuscule.")
    
    if not any(char.islower() for char in mot_de_passe):
        message_erreurs.append("Le mot de passe doit contenir au moins une lettre minuscule.")
    
    if not any(char.isdigit() for char in mot_de_passe):
        message_erreurs.append("Le mot de passe doit contenir au moins un chiffre.")

    if not any(char in caracteres_speciaux for char in mot_de_passe):
        message_erreurs.append("Le mot de passe doit contenir au moins un caractère spécial.")

    # Affichage des messages d'erreur
    if message_erreurs:
        message_erreur = "\n".join(message for message in message_erreurs)
        message_label.config(text=message_erreur, fg="red")
    else:
        message_label.config(text="Mot de passe valide !", fg="green")

    return message_erreurs
        

 # Fonction pour Crypter le mdp
def crypt_mdp(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print("Mot de passe crypté :", hashed_password)  # Affiche le mot de passe crypté dans le terminal
    return hashed_password

def sauvegarde_mdp():
    # Vérifier si un mot de passe est saisi
    mot_de_passe = mdp.get()
    if not mot_de_passe:
        message_label.config(text="Veuillez saisir un mot de passe.", fg="red")
        return

    # Vérifier si le mot de passe satisfait les critères de validation
    erreurs = verifier_mdp()
    if erreurs:
        # Afficher les messages d'erreur
        message_erreur = "\n".join(erreurs)
        message_label.config(text=message_erreur, fg="red")
        return

    # Si le mot de passe est valide, procéder à son cryptage et à son enregistrement
    mot_de_passe_crypte = crypt_mdp(mot_de_passe)

    # Charger les mots de passe existants depuis le fichier JSON s'il existe
    try:
        with open("user.json", "r") as fichier:
            mots_de_passe = json.load(fichier)
    except FileNotFoundError:
        mots_de_passe = []

    # Vérifier si le mot de passe est déjà enregistré
    if mot_de_passe_crypte in mots_de_passe:
        message_label.config(text="Ce mot de passe est déjà enregistré.", fg="red")
    else:
        # Ajouter le nouveau mot de passe crypté à la liste
        mots_de_passe.append(mot_de_passe_crypte)

        # Enregistrer la liste mise à jour dans le fichier JSON
        with open("user.json", "w") as f:
            json.dump(mots_de_passe, f)

        message_label.config(text="Mot de passe sauvegardé avec succès !", fg="green")

# Zone de texte pour afficher les messages d'erreur ou de succès
message_label = Label(fenetre, text="", fg="black", bg="#41B77F")
message_label.place(relx=0.5, rely=0.85, anchor=CENTER)

# Créer un bouton valider
bouton = Button(fenetre, text="Sauvegarder", command=sauvegarde_mdp, bg="blue")
bouton.pack(pady=5)
bouton.place(relx=0.4, rely=0.5, anchor=CENTER)

                    #GENERER MOT DE PASSE 

#GENERER MOT DE PASSE 

def generer_mdp():
    minuscule="abcdefghijklmnopqrstuvwxyz"
    majuscule="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nombres="0123456789"
    symbole="?./§&#()[]-_%($')"

    total = minuscule+ majuscule + nombres + symbole
    longueur = 8
    password = "".join(random.sample(total, longueur))  

    # Mettre à jour le texte du label
    mdp.delete(0 , "end")
    mdp.insert(0 , password)

    return password

# Créer un bouton Génerer
bouton = Button(fenetre, text="Génerer", command=generer_mdp, bg="gray")
bouton.pack(pady=5)
bouton.place(relx=0.6, rely=0.5, anchor=CENTER)

# Afficher le mdp crypté sur une fenetre
def crypter_mot_de_passe():
    mot_de_passe = mdp.get()
    mot_de_passe_crypte = crypt_mdp(mot_de_passe)
    messagebox.showinfo("Mot de passe crypté", f"Le mot de passe a été crypté avec succès.\nMot de passe crypté : {mot_de_passe_crypte}")

#bouton pour enregistré et crypter le mot de passe
bouton_crypter = Button(fenetre, text="Affichez le mot de passe enregistré", command=crypter_mot_de_passe, bg="#41B77F")
bouton_crypter.pack(pady=5)
bouton_crypter.place(relx=0.5, rely=0.7, anchor=CENTER)

                #Boutton afficher / masquer mdp

# Fonction pour basculer entre l'affichage du mot de passe et son masquage
def mdp_affichage():
    if mdp["show"] == "":
        mdp["show"] = "*"
        bouton_affichage.config(text="Afficher le mot de passe")
    else:
        mdp["show"] = ""
        bouton_affichage.config(text="Masquer le mot de passe")

# Créer un bouton pour afficher ou masquer le mot de passe
bouton_affichage = Button(fenetre, text="Afficher le mot de passe", command=mdp_affichage, bg="Green")
bouton_affichage.pack(pady=5)
bouton_affichage.place(relx=0.5, rely=0.6, anchor=CENTER)

fenetre.mainloop()


#label.pack()              #place le texte tout en haut centré
#label.place(x='140' , y='70')  #x=horizentale, y=verticale                
#sub_label= Label(fenetre, text="")  sous label
#sub_label.pack()

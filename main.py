import hashlib          # pour crypté nos MDP
import json            #importe le module JSON qui permet par exemple de prendre un objet Python  et de le sauvegarde dans un fichier JSON spécifié
import random         #permet de genrer chiffre lettre et signe de ponctuation,ect.. de maniere aleatoire
import string           #permet d'importer la biblio de string (string.ascii_letters,ect...) Utilisé dans la fonction "generer_mot_de_passe"
import customtkinter  # importe le customtkinter 
 
 
 
 # Vérifie si le mot de passe respecte toutes les criteres
def mot_de_passe_valide(password):     #longueur du mdp
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):    #controle si il y'a une maj ( si dans tout les caracteres ne possede pas une majuscule on retourne "false")
        return False
    if not any(char.islower() for char in password):    #controle si il y'a une min
        return False
    if not any(char.isdigit() for char in password):    #controle si il y'a un chiffre
        return False
    if not any(char in string.punctuation for char in password):    #controle si il y'a un caractere special
        return False
    return True


# cette fonction nous retourne le message affiché si le mdp est valide ou non 
def valider_mot_de_passe():
    password = entree_password.get()
    if mot_de_passe_valide(password):
        label_result.configure(text="Mot de passe valide !", font=("Montserrat", 15), fg="green")
    else:
        label_result.configure(text="Le mot de passe ne respecte pas les criteres (Au moins une Maj,min,chiffres et caracteres speciaux. Reessayez.)", font=("Montserrat", 15), fg="red")


#fonction pour cacher ou le mot de passe en fonction du choix de l'utilisateur"
def affichage_mot_de_passe():
    if checkbutton_var.get():
        entree_password.configure(show="")
    else:
        entree_password.configure(show="*")


#fonction pour encrypter le mdp utilisateur avec l'algorithme SHA-256 et enregistré le mdp dans le fichier JSON
def cryptage_mdp():
    mot_de_passe = entree_password.get()                                        #Récupère le mot de passe saisi
    hashed_mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()   #methode utilisé pour haché le mdp
    try:
        with open("mdp_save.json", "r") as file:                                #ouvre et lit le fichier json danns lequel sont stovkés les mdp
            mots_de_passe = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        mots_de_passe = {}                                              #on demarre avec une liste vide de mdp
    if not mot_de_passe_valide(mot_de_passe):
        label_result.configure(text="Le mot de passe ne respecte pas les critères pour pouvoir être crypté.(Au moins une Maj,min,chiffres et caracteres speciaux. Reessayez.)", font=("Comic Sans MS", 15))
        return
    if hashed_mot_de_passe in mots_de_passe:
        label_result.configure(text="Ce mot de passe est déjà enregistré.", font=("Comic Sans MS", 15), fg="red")
        return           # si le mdp crypté est deja enregistré dans le fichier json alors on informe l'utilisateur que c'est deja le cas

    mots_de_passe[hashed_mot_de_passe] = mot_de_passe
    with open("mdp_save.json", "w") as file:                    #"w" ecrit le mdp dans le fichier json en normal et version crypté
        json.dump(mots_de_passe, file)
    label_result.configure(text="Mot de passe crypté et enregistré avec succès.", font=("Comic Sans MS", 15), fg="green")    #Si il n'est pas dans la liste alors on enregistre le mdp crypté dans le fichier json



#afficher les mdp enregistré dans JSON sur le customtkinter
def afficher_mdp():
    with open("mdp_save.json", "r") as file:                             #ouvre le fichier JSON pour y voir les mdp et les "lit"
        mots_de_passe = json.load(file)
    text_widget.insert("end", "Liste de mots de passe déjà enregistrés:")          #pour inserer le texte dans le widget text
    for hashed_mot_de_passe, mot_de_passe in mots_de_passe.items():
        text_widget.insert("end", f"{hashed_mot_de_passe}\n")



def generer_mot_de_passe():
    longueur = 8                    # Longueur du mot de passe
    caracteres = string.ascii_letters + string.digits + string.punctuation  #combine les lettres min et maj + chiffre + signe de ponctuation grave a l'import "string"
    while True:                                                              # crée une boucle infiniee qui signifie que le bloc de code à l'intérieur de la boucle sera exécuté en continu jusqu'à ce qu'une condition  soit rencontrée.
        mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))   #si la condition des lettres min et maj + chiffre + signe de ponctu est bonne alors mdp = choix de caractére au hasard + la longueur de 8 caractére demandé
       
        # Vérifier si le mot de passe respecte les conditions:
        if (any(caractere.islower() for caractere in mot_de_passe) and      # verifie si il y'a au moins un caractere en miniscule
            any(caractere.isupper() for caractere in mot_de_passe) and    # verifie si il y'a au moins un caractere en majuscule
            any(caractere.isdigit() for caractere in mot_de_passe) and     #verifie si il y'a au moins un chiffre
            any(caractere in string.punctuation for caractere in mot_de_passe)):     # verifie si il y'a au moins un signe de ponctuation
            return mot_de_passe                                                        #si toute les conditions sont remplies alors ca nous retourne un mdp au hasard  #si toute les conditions sont remplies alors ca nous retourne un mdp au hasard 



def generer_et_afficher_mot_de_passe():
    mot_de_passe = generer_mot_de_passe()                       #reprend la fonction ci dessus pour creer un mdp de maniere random
    entree_password.delete(0, "end")                              #supprime ce qu'il y avait d'ecrit dans le champ en demarrant de l'index "0" jusqu'a la fin (END)
    entree_password.insert(0, mot_de_passe)                         #Insert le mdp creer de maniere random grace a la fonction "generer_mot_de_passe" en commencant de l'index "0"



#######################################################CUSTOMTK####################################################

# Fenetre principal qui s'appellera "window"
window = customtkinter.CTk()

# Titre de la fenetre + personnalisation fenetre
window.title("Gestionnaire mot de passe")
window.geometry("1000x700")
window.iconbitmap("logo_tk.ico")
window.config(background="#727EC6")


# Ajouter titre
label_title = customtkinter.CTkLabel(window, text="Bienvenue sur le gestionnaire de mot de passe", font=("Comic Sans MS", 20), bg_color="#727EC6", fg_color="#727EC6")
label_title.pack()


# Ajouter phrase
label_title = customtkinter.CTkLabel(window, text="Entrez votre mot de passe ci dessous:", font=("Comic Sans MS", 15), bg_color="#727EC6", fg_color="#727EC6")
label_title.pack()


# Champ de saisie du mot de passe
entree_password = customtkinter.CTkEntry(window, font=("Comic Sans MS", 18), show="*")
entree_password.pack(pady=5)

# Bouton pour valider le mot de passe
bouton_valider = customtkinter.CTkButton(window, text="Valider", bg_color="white", font=("Comic Sans MS", 15), fg_color="green",command=valider_mot_de_passe)
bouton_valider.pack(pady=10)


# Résultat de la validation du mot de passe (affiche si le mdp a bien les conditions necessaire ou non)
label_result = customtkinter.CTkLabel(window, text="", font=("Comic Sans MS", 10), bg_color="#727EC6")
label_result.pack()


# Bouton/checkbox pour afficher ou non le mdp dans le tkinter
checkbutton_var = customtkinter.IntVar()
checkbutton = customtkinter.CTkCheckBox(window, text="Afficher/Cacher mon mot de passe ecrit ou généré", font=("Comic Sans MS", 15), bg_color="orange", fg_color="red", variable=checkbutton_var, command=affichage_mot_de_passe)
checkbutton.pack(pady=10)


# Bouton pour crypter le mot de passe
button_crypter = customtkinter.CTkButton(window, text="Crypter et enregistrer le mot de passe", font=("Comic Sans MS", 15), bg_color="blue", fg_color="blue", command=cryptage_mdp)
button_crypter.pack()


# Bouton pour afficher tous les mdp enregistrés
button_afficher = customtkinter.CTkButton(window, text="Afficher les mots de passe enregistrés", font=("Comic Sans MS", 15), bg_color="#d51b21", fg_color="red", command=afficher_mdp)
button_afficher.pack()
text_widget = customtkinter.CTkTextbox(window, font=("Comic Sans MS", 10), fg_color="black")
text_widget.configure(width=300, height=300)
text_widget.pack()


# Bouton pour générer et afficher le mot de passe
button_generer = customtkinter.CTkButton(window, text="Générer un mot de passe", font=("Comic Sans MS", 15), bg_color="#440f2b", fg_color="black", command=generer_et_afficher_mot_de_passe)
button_generer.pack(pady=10)

# Affichage du mot de passe généré
label_password = customtkinter.CTkLabel(window, text="", font=("Comic Sans MS", 10), bg_color="#727EC6")
label_password.pack(pady=10)



# Affichage pour lancer le tkinter
window.mainloop()


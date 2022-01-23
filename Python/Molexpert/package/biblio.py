"""
Projet Molexpert
Terminale S Spécialité ISN
NDA

biblio.py

Bibliothéques de fonctions utilisées dans le programme principal.

"""

__author__ = 'DEBOUVRIES Ryan STREMEZ Jordan'
__date_creation__ = 'May 2019'

# -*-coding:Utf8 -*
# Bibliothèque de fonctions
from Tkinter import*
from visual import*

origineatome=10
tailleatome=15

hydrogene = []
carbone = []
oxygene = []
azote = []
chlore = []

lignes = []

# ATOMES
def Atome (color, cancreate):
    def wrap ():
        global hydrogene,carbone,oxygene,azote,chlore,origineatome
        # Création des formes par types d'atomes
        if color == 'white' :
            hydrogene.append(cancreate.create_oval(origineatome,origineatome,origineatome+(tailleatome*2),origineatome+(tailleatome*2),fill=color))
        if color == 'gray' :
            carbone.append(cancreate.create_oval(origineatome,origineatome,origineatome+(tailleatome*2),origineatome+(tailleatome*2),fill=color))
        if color == 'red' :
            oxygene.append(cancreate.create_oval(origineatome,origineatome,origineatome+(tailleatome*2),origineatome+(tailleatome*2),fill=color))
        if color == 'blue' :
            azote.append(cancreate.create_oval(origineatome,origineatome,origineatome+(tailleatome*2),origineatome+(tailleatome*2),fill=color))
        if color == 'green' :
            chlore.append(cancreate.create_oval(origineatome,origineatome,origineatome+(tailleatome*2),origineatome+(tailleatome*2),fill=color)) 
    return wrap

# ATOMES EN 3D
def create_atome(cancreate, liste, color):
    for elt in liste:
        # Récupération des coordonnées des atomes
        coordonnees=cancreate.coords(elt)
        [x3,y3,x4,y4]=coordonnees
        print (coordonnees)
        # Verification que l'objet n'est pas supprimé
        if coordonnees != [0.0,0.0,0.0,0.0]:
            # Adaptation aux coordonnées 3D
            x_milieu=(x3+x4)/2
            y_milieu=(y3+y4)/2
            xf=x_milieu/10
            yf=y_milieu/10
            # Affichage de l'atome en 3D
            sphere(pos=(xf,yf,0),color=color,radius=2)

# BOUTONS
def Boutons_menu (canmenu, cancreate):
    # Bouton Hydrogene
    global bouton1
    bouton1=Button(canmenu)
    bouton1.configure(text="H hydrogène",height=2,width=20,activeforeground='gray',command=Atome('white', cancreate))
    bouton1.grid(row=1,column=1,padx=2,pady=2)
    # Bouton Carbone
    global bouton2
    bouton2=Button(canmenu)
    bouton2.configure(text="C carbone",height=2,width=20,activeforeground='gray',command=Atome('gray', cancreate))
    bouton2.grid(row=1,column=2,padx=2,pady=2)
    # Bouton oxygene
    global bouton3
    bouton3=Button(canmenu)
    bouton3.configure(text="O oxygène",height=2,width=20,activeforeground='gray',command=Atome('red', cancreate))
    bouton3.grid(row=1,column=3,padx=2,pady=2)
    # Bouton Azote
    global bouton4
    bouton4=Button(canmenu)
    bouton4.configure(text="N azote",height=2,width=20,activeforeground='gray',command=Atome('blue', cancreate))
    bouton4.grid(row=1,column=4,padx=2,pady=2)
    # Bouton chlore
    global bouton5
    bouton5=Button(canmenu)
    bouton5.configure(text="Cl chlore",height=2,width=20,activeforeground='gray',command=Atome('green', cancreate))
    bouton5.grid(row=2,column=1,padx=2,pady=2)
    

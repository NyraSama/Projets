"""
Projet Molexpert
Terminale S Spécialité ISN
NDA

Molexpert.py

Logiciel de création 3D de molécules.

"""

__author__ = 'DEBOUVRIES Ryan STREMEZ Jordan'
__date_creation__ = 'May 2019'

# -*-coding:Utf8 -*
from Tkinter import*
from package.biblio import*
from visual import*

# Affichage fenêtre
fenetre=Tk()
fenetre.title('Molexpert')
fenetre.iconbitmap("logo.ico")
fenetre.wm_state(newstate="zoomed")# mise en plein écran

#-------------------------Menu-------------------------

# Création du cadre de menu
frame_menu=LabelFrame(fenetre)
frame_menu.configure(text='Menu',bd=2,relief='groove')
frame_menu.grid(row=1,column=1,padx=10,pady=10)

# Creation de la zone de menu
canmenu=Canvas(frame_menu)
canmenu.configure(width=500,height=100,bg='white')
canmenu.pack()

#-------------------------Action Create Room-------------------------

# Création du cadre de choix des action
frame_createmenu=LabelFrame(fenetre)
frame_createmenu.configure(text='Menu Create Room',bd=2,relief='groove')
frame_createmenu.grid(row=2,column=1,padx=10,pady=10)

# Creation de la zone de choix des actions
cancreatemenu=Canvas(frame_createmenu)
cancreatemenu.pack()

# Menu gestion actions
action=StringVar()
action.set('deplace')
raction1=Radiobutton(cancreatemenu)
raction1.configure(variable=action,value='liaison',text='liaison')
raction1.grid(row=1,column=1)
raction2=Radiobutton(cancreatemenu)
raction2.configure(variable=action,value='deplace',text='déplacement')
raction2.grid(row=1,column=2)
raction3=Radiobutton(cancreatemenu)
raction3.configure(variable=action,value='delete',text='supprimer')
raction3.grid(row=1,column=3)
raction4=Radiobutton(cancreatemenu)
raction4.configure(variable=action,value='dbliaison',text='double liaison')
raction4.grid(row=1,column=4)
raction5=Radiobutton(cancreatemenu)
raction5.configure(variable=action,value='tpliaison',text='triple liaison')
raction5.grid(row=1,column=5)

#-------------------------Create Room-------------------------

# Création du cadre de création
frame_create=LabelFrame(fenetre)
frame_create.configure(text='Create Room',bd=2,relief='groove')
frame_create.grid(row=3,column=1,padx=10,pady=10)

# Creation de la zone de création
Largeur = 600
Hauteur = 450
cancreate=Canvas(frame_create)
cancreate.configure(width=Largeur,height=Hauteur,bg='white')
cancreate.pack()

# Appel de ce qu'il se passe lors du clic gauche de la souris
# Initialisation de l'état de la souris
clicsouris = False

# Fonction de reinitialisation
def reset():
    cancreate.delete(ALL)
    action.set('deplace')
    
# Fonction de gestion lors du clic gauche de la souris
def clic(event):
    global clicsouris,objet,x1,y1
    # Changement de l'état de la souris
    clicsouris = True
    # Conservation des coordonnées de la souris
    x1=event.x
    y1=event.y
    # Repérage de l'objet
    objet=cancreate.find_closest(x1,y1)
    # Gestion en fonction de l'action sélectionnée
    if (action.get()=='deplace'):
        cancreate.itemconfig(objet,width=1)
        cancreate.lift(objet)
    elif (action.get()=='delete'):
        # Création d'une apparence de suppression
        cancreate.coords(objet,0,0,0,0)
    print(clicsouris)

# Fonction de gestion lors du déplacement de la souris
def dragclic(event):
    global objet,x1,y1,x2,y2
    # Gestion en fonction de l'action sélectionnée
    if (action.get()=='deplace'):
        # Conservation des nouvelles coordonnées de la souris
        x2=event.x
        y2=event.y
        # Enregistrement de la différence des coordonnées de la souris
        dx,dy=x2-x1,y2-y1
        x1,y1=x2,y2
        # Actualisation des coordonnées de l'objet
        cancreate.coords(objet,x2,y2,x2+40,y2+40)
        x1,y1=x2,y2

# Fonction de gestion lors du déclic gauche de la souris 
def declic(event):
    global clicsouris,objet,x1,y1,x2,y2
    # Réinitialisation de l'état de la souris
    clicsouris = False
    # Gestion en fonction de l'action sélectionnée
    if (action.get()=='liaison') or (action.get()=='dbliaison') or (action.get()=='tpliaison'):
        # Conservation des nouvelles coordonnées de la souris
        x2=event.x
        y2=event.y
        # Repérage du 2ème objet
        objet2=cancreate.find_closest(x2,y2)
        # Récupération des coordonnées des 2 objets
        [xmin_objet1,ymin_objet1,xmax_objet1,ymax_objet1]=cancreate.coords(objet)
        [xmin_objet2,ymin_objet2,xmax_objet2,ymax_objet2]=cancreate.coords(objet2)
        # Gestion en fonction du type de liaison
        if (action.get()=='liaison'):
            # Adaptation des coordonnées au milieu des objets
            x1=(xmin_objet1+xmax_objet1)/2
            y1=(ymin_objet1+ymax_objet1)/2
            x2=(xmin_objet2+xmax_objet2)/2
            y2=(ymin_objet2+ymax_objet2)/2
            # Création d'une ligne
            lignes.append(cancreate.create_line(x1,y1,x2,y2,width=2))
        if (action.get()=='dbliaison'):
            # Adaptation des coordonnées de la liaison 1
            x1=((xmin_objet1+xmax_objet1)/2)
            y1=((ymin_objet1+ymax_objet1)/2)+((ymin_objet1-ymax_objet1)/4)
            x2=((xmin_objet2+xmax_objet2)/2)
            y2=((ymin_objet2+ymax_objet2)/2)+((ymin_objet2-ymax_objet2)/4)
            # Adaptation des coordonnées de la liaison 2
            x3=((xmin_objet1+xmax_objet1)/2)
            y3=((ymin_objet1+ymax_objet1)/2)-((ymin_objet1-ymax_objet1)/4)
            x4=((xmin_objet2+xmax_objet2)/2)
            y4=((ymin_objet2+ymax_objet2)/2)-((ymin_objet2-ymax_objet2)/4)
            # Création des deux lignes
            lignes.append(cancreate.create_line(x1,y1,x2,y2,width=2))
            lignes.append(cancreate.create_line(x3,y3,x4,y4,width=2))
        if (action.get()=='tpliaison'):
            # Adaptation des coordonnées de la liaison 1
            x1=((xmin_objet1+xmax_objet1)/2)
            y1=((ymin_objet1+ymax_objet1)/2)+((ymin_objet1-ymax_objet1)/3)
            x2=((xmin_objet2+xmax_objet2)/2)
            y2=((ymin_objet2+ymax_objet2)/2)+((ymin_objet2-ymax_objet2)/3)
             # Adaptation des coordonnées de la liaison 2
            x3=((xmin_objet1+xmax_objet1)/2)
            y3=((ymin_objet1+ymax_objet1)/2)
            x4=((xmin_objet2+xmax_objet2)/2)
            y4=((ymin_objet2+ymax_objet2)/2)
            # Adaptation des coordonnées de la liaison 3
            x5=((xmin_objet1+xmax_objet1)/2)
            y5=((ymin_objet1+ymax_objet1)/2)-((ymin_objet1-ymax_objet1)/3)
            x6=((xmin_objet2+xmax_objet2)/2)
            y6=((ymin_objet2+ymax_objet2)/2)-((ymin_objet2-ymax_objet2)/3)
            # Création des deux lignes
            lignes.append(cancreate.create_line(x1,y1,x2,y2,width=2))
            lignes.append(cancreate.create_line(x3,y3,x4,y4,width=2))
            lignes.append(cancreate.create_line(x5,y5,x6,y6,width=2))
    elif (action.get()=='deplace'):
        # Actualisation des coordonnées de l'objet
        cancreate.itemconfig(objet,width=1)
        cancreate.coords(objet,x2,y2,x2+30,y2+30)
    print(clicsouris)

# Détection des actions et appel des fonctions
cancreate.bind('<ButtonPress-1>',clic)
cancreate.bind('<B1-Motion>',dragclic)
cancreate.bind('<ButtonRelease-1>',declic)

# Bouton Reset
bouton6=Button(cancreatemenu)
bouton6.configure(text="Reset",height=1,width=10,activeforeground='gray',command=lambda: reset())
bouton6.grid(row=1,column=6)

# Creation des boutons du menu
Boutons_menu (canmenu, cancreate)

#-------------------------Affichage 3D-------------------------

# Bouton Résultat
bouton7=Button(cancreatemenu)
bouton7.configure(text="Resultat",height=1,width=10,activeforeground='gray',command=lambda: disp())
bouton7.grid(row=1,column=7)

# Mise en place de l'affichage 3D   
def disp():
    # Paramètrage de la fenêtre 3D
    scene.range=50
    scene.fullscreen=1
    scene.autocenter=1
    
    # Appel des fonctions de création
    create_atome(cancreate, hydrogene, color.white)
    create_atome(cancreate, carbone, color.gray(0.5))
    create_atome(cancreate, oxygene, color.red)
    create_atome(cancreate, azote, color.blue)
    create_atome(cancreate, chlore, color.green)
    
    # Création 3D des Liaisons
    for elt in lignes:
        # Récupération des coordonnées de la liaison
        coordonnees=cancreate.coords(elt)
        [x3,y3,x4,y4]=coordonnees
        print (coordonnees)
        if coordonnees != [0.0,0.0,0.0,0.0]:
            # Adaptation aux coordonnées 3D
            xf_pos=x3/10
            yf_pos=y3/10
            # Calcul des coordonnées du vecteur à suivre
            xf_axis=(x4/10)-xf_pos
            yf_axis=(y4/10)-yf_pos
            # Affichage de la laison en 3D
            cylinder(pos=(xf_pos,yf_pos,0),axis=(xf_axis,yf_axis,0),color=color.white,radius=0.2)
        
    # Actualisation de la fenêtre
    actualisation=sphere(pos=(0,0,0),color=color.red,radius=0.00001)
    while True:
        rate(100)
        actualisation.rotate(angle=0.1)

# Réactualisation de la fenêtre
fenetre.mainloop()


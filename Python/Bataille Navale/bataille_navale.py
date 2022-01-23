#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TP AP1
Licence SESI 1ère année
Univ. Lille 1

bataille_navale.py

Module pour le jeu de bataille navale.

Pour une description générale du jeu voir
http://fr.wikipedia.org/wiki/Bataille_navale_%28jeu%29

"""

__author__ = 'DEBOUVRIES Ryan TROGNEUX Laura'
__date_creation__ = '18/03/2020'


###############################################
# Modules utilisés
###############################################

# Pour la disposition aléatoire des navires
from random import randint

# Pour le fichier des scores
from datetime import datetime 

###############################################
# Constantes nommées utilisées
###############################################

# les deux dispositions possibles pour un navire
#  sur le plateau :
# - H : horizontale
# - V : verticale
DISPOSITIONS="HV"


# codes réponses d'analyse de tirs
RATE = 0
TOUCHE = 1
COULE = 2

# nom du fichier contenant les scores réalisés
FICHIER_RESULT = 'bataille_navale_scores.txt'

###############################################
# Procédure principale du jeu
###############################################

def jouer (nom,descr):
    """
    str, str -> ()
    procédure de jeu complet de bataille navale,
    le nom du joueur est donné par le paramètre nom, 
    et le jeu est décrit dans le fichier descr.

    CU : le fichier jeu doit exister et être conforme
    à un fichier de description.
    """
    jeu = cree_jeu(descr)
    decrire_le_jeu(jeu)
    nbre_tirs = 0
    while not tous_coules(jeu):
        tir = lire_un_tir (nom)
        nbre_tirs += 1
        nav,res = analyse_un_tir (jeu,tir)
        if res == RATE:
            print ("raté.")
        elif res == TOUCHE:
            print (nav + " touché.")
        else:
            print (nav + " coulé.")
    sauver_result (nom,descr,nbre_tirs)
    print ("Terminé en {0} tirs".format(nbre_tirs))

###############################################
# Opérations sur les fichiers
###############################################

def lire_donnees(num_descr):
    """
    str -> tuple
    renvoie un triplet dont les deux premières composantes sont 
    et la troisième une liste de couples (nature, taille) où
    nature est une chaîne de caractères décrivant la nature du navire
    et taille un entier désignant le nombre de cases occupées par ce navire.
    Toutes ces données sont lues dans un fichier nommé 'jeu'+num_descr+'.txt'.

    CU : le fichier 'jeu'+num_descr+'.txt' doit exister et être au bon format, 
    ie un  fichier texte contenant :
    larg : haut
    nature1 : taille1
    nature2 : taille2
    ...
    """
    fichier = open("jeu{}.txt".format(num_descr),"r")
    lignes = fichier.readlines()
    fichier.close()
    numbers='0123456789'
    
    #DETECTION DES SEPARATEURS :    
    spliters=[0]*len(lignes)
    for i in range(len(lignes)):
        spliter=0
        while spliter != len(lignes[i]) and lignes[i][spliter] != ':':
            spliter+=1
        spliters[i]=spliter
        
    #RECUPERATION DES DONNEES :
    largeur=''
    hauteur=''
    for i in range(spliters[0]):
        if lignes[0][i] in numbers:
            largeur+=lignes[0][i]
    for i in range(spliters[0]+1, len(lignes[0])):
        if lignes[0][i] in numbers:
            hauteur+=lignes[0][i]
    largeur=int(largeur)
    hauteur=int(hauteur)
    
    navires=[]
    for i in range(1,len(lignes)):
        nom=''
        taille=''
        for i2 in range(spliters[i]):
            if lignes[i][i2] != ' ':
                nom+=lignes[i][i2]
        for i2 in range(spliters[i]+1, len(lignes[i])):
            if lignes[i][i2] != ' ':
                taille+=lignes[i][i2]
        taille=int(taille)
        navires.append((nom, taille))
    
    return (largeur, hauteur, navires)


def sauver_result (nom, jeu, nbre):
    """
    str, str, int -> NoneType
    ajoute une ligne dans le fichier FICHIER_RESULT
    contenant le nom, le numéro du jeu joué et le nombre de tirs effectués 
    dans la partie.

    CU : aucune
    """
    with open(FICHIER_RESULT, "a") as f:
        f.write('{0}:{1}:{2}:{3}\n'.format(nom,jeu,nbre,str(datetime.today())))
        



###############################################
# Procédures de construction du jeu
###############################################
    
def cree_jeu (descr):
    """
    str -> dict
    renvoie un nouveau jeu de bataille navale construit à partir des données 
    lues dans le fichier descr.


    Le jeu est représenté par un dictionnaire à quatre clés :
    - 'plateau' pour représenter le plateau de jeu (l'espace maritime) avec ses navires
    - 'nb_cases_occupees' dont la valeur associée est le nombre de cases du plateau
                          occupées par les navires
    - 'touches' dictionnaire contenant deux champs :
                * l'un nomme 'nb_touches' contenant un entier 
                * l'autre nomme 'etats_navires' qui contient un dictionnaire
                  donnant pour chaque navire le nombre de tirs 
                  qu'ils peuvent encore recevoir avant d'être coulés
    - 'coups_joues' ensemble des coups joués depuis le début de la partie.

    CU : le fichier doit contenir une description correcte du jeu (cf lire_donnees)
    """
    #Initialisation et lecture des données
    data=lire_donnees(descr)
    jeu=dict()
    esp=dict()
    
    #Gestion du plateau
    esp['larg']=data[0]
    esp['haut']=data[1]
    for nav in data[2]:
        placer(esp,nav)
    jeu['plateau']=esp
    
    #Gestion des cases occupees
    cases_used=0
    for nav in data[2]:
        cases_used+=nav[1]
    jeu['nb_cases_occupees']=cases_used
    
    #Gestion des touchés en début de partie
    touches=dict()
    touches['nb_touches']=0
    etat_nav=dict()
    for nav in data[2]:
        etat_nav[nav[0]]=nav[1]
    touches['etats_navires']=etat_nav
    jeu['touches']=touches
    
    #Gestion des coups joués en début de partie
    jeu['coups_joues']=set()
    
    return jeu
    


def cree_plateau (l, h, l_nav):
    """
    int, int, list -> dict
    renvoie un plateau de largeur l et de hauteur h occupé par les navires 
    de l_nav.
    La disposition est aléatoire.

    CU : les dimensions doivent permettre le placement de tous les navires
    """
    esp={'larg':l,'haut':h}
    for nav in l_nav:
        placer(esp, nav)
    return esp

def est_placable (esp, nav, pos, disp):
    """
    dict, tuple, tuple, str -> bool
    
    CU : disp = 'H' ou 'V'
    """
    #Initialisation
    cases_bateau=[]
    res=True
    #Gestion des cases utilisées par le bateau
    if disp == 'H':
        for i in range(nav[1]):
            cases_bateau.append((pos[0]+i,pos[1]))
    else:
        for i in range(nav[1]):
            cases_bateau.append((pos[0],pos[1]+i))
    #Gestion des cas
    for case in cases_bateau:
        if (case[0]<1 or case[0]>esp['larg'] or case[1]<1 or case[1]>esp['haut']) or (case in esp):
            res=False
    return res

def placer (esp, nav):
    """
    dict, tuple -> NoneType
    place le navire nav dans l'espace maritime esp.
    Choix de l'emplacement aléatoire.

    CU : il doit rester de la place
    """
    #Premier tirage aléatoire d'une position
    case_depart=(randint(1,esp['larg']),randint(1,esp['haut']))
    disp=DISPOSITIONS[randint(0,1)]
    #Recherche d'une position aléatoire possible
    while not est_placable(esp,nav,case_depart,disp):
        case_depart=(randint(1,esp['larg']),randint(1,esp['haut']))
        disp=DISPOSITIONS[randint(0,1)]
    #Gestion des cases utilisées par le bateau
    cases_bateau=[]
    if disp == 'H':
        for i in range(nav[1]):
            cases_bateau.append((case_depart[0]+i,case_depart[1]))
    else:
        for i in range(nav[1]):
            cases_bateau.append((case_depart[0],case_depart[1]+i))
    #Ajout à l'espace maritime
    for case in cases_bateau:
        esp[case]=nav[0]
    


###############################################
# Procédures de déroulement du jeu
###############################################
    
def decrire_le_jeu (jeu):
    """
    dict -> ()
    imprime une description du jeu.
    
    CU : aucune
    """
    print('Dimensions du plateau de jeu :')
    print('- largeur : ',jeu['plateau']['larg'])
    print('- hauteur : ',jeu['plateau']['haut'])
    print('Navires :')
    for nav in jeu['touches']['etats_navires']:
        print('- ',nav,' : ',jeu['touches']['etats_navires'][nav],' case(s)')
    print('A vous de jouer en répondant à l\'invite .- par deux nombres séparés par une virgule')
    


def lire_un_tir (nom):
    """
    str -> tuple
    renvoie un couple d'entiers lus sur l'entrée standard

    CU : l'entrée doit être de la forme xxx,yyy avec xxx et yyy
         une représentation décimale de deux nombres entiers
    """
    x=''
    y=''
    conforme=False
    while (not conforme):
        tir=input('Case visée: ')
        if ',' not in tir:
            print('Je ne détecte pas de virgule, il faut un tir de la forme: x,y ou x et y sont deux entiers')
        else:
            [x,y]=tir.split(',')
            test_x=True
            test_y=True
            for c in x:
                if c not in '0123456789':
                    test_x=False
                    print('Il semble qu\'il n\'y a pas que ou pas du tout de chiffres avant la virgule')
            for c in y:
                if c not in '0123456789':
                    test_y=False
                    print('Il semble qu\'il n\'y a pas que ou pas du tout de chiffres après la virgule')
            if test_x and test_y:
                conforme=True
    return (int(x),int(y))

def analyse_un_tir (jeu,tir):
    """
    dict, tuple -> str,int
    renvoie 
      - ("",RATE) si tir raté
      - (nav,TOUCHE) si nav touché
      - (nav,COULE) si nav coulé
    et modifie l'état du jeu en conséquence.

    CU : aucune 
    """
    if (tir not in jeu['plateau']) or (tir in jeu['coups_joues']):
        return ('',RATE)
    else:
        jeu['coups_joues'].add(tir)
        nav=jeu['plateau'][tir]
        jeu['touches']['nb_touches']+=1
        if jeu['touches']['etats_navires'][nav]==1:
            jeu['touches']['etats_navires'][nav]=0
            return (nav,COULE)
        else:
            jeu['touches']['etats_navires'][nav]-=1
            return (nav,TOUCHE)


def tous_coules (jeu):
    """
    dict -> bool
    renvoie True si tous les navires du plateau de jeu ont été coulés
            et False dans le cas contraire.

    CU : aucune
    """
    res=True
    for elt in jeu['touches']['etats_navires']:
        if jeu['touches']['etats_navires'][elt]!=0:
            res=False
    return res
    

    
###############################################
# Pour une utilisation du module depuis un terminal
###############################################    

if __name__ == '__main__':
    import sys

    if len (sys.argv) != 3:
        jouer (input('NAME:'),input('VERSION:'))
    else:
        jouer (sys.argv[1],sys.argv[2])




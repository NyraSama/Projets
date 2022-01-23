#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Interface graphique pour le jeu de bataille navale.
"""

__author__ = 'DEBOUVRIES Ryan'
__date_creation__ = '18/03/2020'

from tkinter import *
import bataille_navale as BN

class Plateau (Frame):
    """
    """
    def __init__ (self, boss, jeu):
        Frame.__init__(self)
        self.jeu = jeu
        self.nlig = jeu['plateau']['haut']
        self.ncol = jeu['plateau']['larg']
        self.can = Canvas (self, bg = "blue", borderwidth = 0,
                           highlightthickness = 1, highlightbackground = "white")
        self.bind ("<Configure>", self.redim)
        self.can.bind ("<Button-1>", self.clic)
        self.can.pack ()
        self.gagne = False
        self.boss = boss
        self.nbre_tirs = 0
        
    def redim (self, event):
        """
        """
        self.width, self.height = event.width - 4, event.height - 4
        self.tracerGrille ()

    def tracerGrille (self):
        """
        """
        lmax = self.width / self.ncol
        hmax = self.height / self.nlig
        self.cote = min (lmax, hmax)
        larg, haut = self.cote * self.ncol, self.cote * self.nlig
        self.can.configure (width = larg, height = haut)
        self.can.delete (ALL)
        s = self.cote
        for l in range (self.nlig - 1):
            self.can.create_line (0, s, larg, s, fill = "white")
            s += self.cote
        s = self.cote
        for c in range (self.ncol - 1):
            self.can.create_line (s, 0, s, haut, fill = "white")
            s += self.cote
        for coup in self.jeu['coups_joues']:
            i,j = coup
            # les coordonnées d'un coup sont dans un intervalle [1,LARG] et [1,HAUT]
            i -= 1
            j -= 1
            x1 = i * self.cote + 5
            x2 = (i+1) * self.cote - 5
            y1 = j * self.cote + 5
            y2 = (j+1) * self.cote - 5
            if coup in self.jeu['plateau']:
                nav = self.jeu['plateau'][coup]
                if self.jeu['touches']['etats_navires'][nav] == 0:
                    self.can.create_oval (x1,y1,x2,y2,outline="grey",width=1,fill="black")
                else:
                    self.can.create_oval (x1,y1,x2,y2,outline="grey",width=1,fill="red")
            else:
                self.can.create_oval (x1,y1,x2,y2,outline="grey",width=1,fill="blue")
        if self.gagne:
            self.boss.conclure (self.nbre_tirs)
            
    def clic (self, event):
        """
        """
        self.nbre_tirs += 1
        lig, col = 1 + event.y // self.cote, 1 + event.x // self.cote
        BN.analyse_un_tir (self.jeu, (col,lig))
        self.gagne =  BN.tous_coules (self.jeu)
        self.tracerGrille()

class Jeu(Frame):
    """
    """
    def __init__(self, nom, version):
        Frame.__init__(self)
        self.master.geometry ("400x400")
        self.master.title (nom + " joue à la bataille navale")
        jeu = BN.cree_jeu(version)
        self.plateau = Plateau (self, jeu)
        self.plateau.pack (expand = YES, fill=BOTH, padx=8, pady=8)
        self.pack ()
        self.nom = nom
        self.version = version


    def conclure (self,nbre_tirs=1000):
        BN.sauver_result (self.nom, self.version, nbre_tirs)
        conclusion = Toplevel (self)
        conclusion.title ('Score')
        Label (conclusion, text = 'Bravo {0} !\nTu as gagné en {1} tirs'.format(self.nom,nbre_tirs)).grid ()
        Button (conclusion, text = 'OK', command = quit).grid ()
        
if __name__ == '__main__':
    import sys

    if len (sys.argv) != 3:
        jeu = Jeu (input('NAME:'),input('VERSION:')).mainloop ()
    else:
        jeu = Jeu (sys.argv[1],sys.argv[2]).mainloop ()

# eof

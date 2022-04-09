"""
Puissance 4, par Axel Tissinier et Clement LeVert
Un simple jeu de puissance 4 avec interface graphique utilisant la souris, un detecteur de victoire, ainsi qu'un bouton restart.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


root = Tk() #creation de la fenetre principale
root.title("Puissance 4")
jeu = ttk.Frame(root) #creation de la fenetre contenant le visuel
jeu.pack(fill=BOTH,expand=YES)
#Canvas qui contiendras les autres elements
can1 = Canvas(jeu,bg='black',height=700, width=840,highlightthickness=0)
can1.pack(fill=BOTH,expand=YES)



def click(event): #reaction a un clic gauche de l'utilisateur dans la fenetre
    global end, limite
    #Pour qu'on ne puisse pas joueur avant la fin de l'animation/temps entre les tours (voir move())
    if limite[2]<limite[1]:
        return
    #recuperation des coordonees de la souris relative a la fenetre
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    if x>55 and x<145 and y>33 and y<67:    #cadre du boutton restart
        if end==1:
            Restart()
        else:
            if messagebox.askyesno("Restart", "La partie n'est pas terminÃ©e, voulez vous vraiment recommencer ?"):
                Restart()
            return
    if y<665 and y>125 and x>68 and x<825: #verification que le cadre du p4 est touche
        if end==1:
            return
        #Pour eviter les erreurs si on clique trop proche des bords des colonnes
        d = (x-68)%100
        if d<10 or d>90:
            return
        #calcul de la colonne pour le placement a partir de la position au moment du clic
        colonne = (x-70)//100
        Placement(colonne)

def win(joueur, colonne, ligne): #test de victoire ou de match nul
    global end, tour, texte, T
    tour += 1
    #Pour reduire les calculs necessaires, on ne peut gagner avant le tour 7
    if tour<7:
        return
    #Test de 4 elements identique d'affile
    C=0                 #compteur de jetons
    i=0
    L = [colonne,ligne]
    if joueur == 'X':
        joueur = 'O'
    else:
        joueur = 'X'
        
    while C<4 and i<7:              #vérification horizontale
        if T[(i,L[1])]==joueur:
            C+=1
        else:
            C=0
        i+=1
        
    if C<4:
        C=0
    i=0
    while C<4 and i<6:              #vérification verticale
        if T[(L[0],i)]==joueur:
            C+=1
        else:
            C=0
        i+=1

    if C<4:
        C=0
    i=0
    while C<4 and i<7:              #vérification diagonale décroissante (code)
        try:
            if T[(L[0]-3+i,L[1]-3+i)]==joueur:
                C+=1
            else:
                C=0
            i+=1
        except:
            i+=1
    
    if C<4:
        C=0
    i=0
    while C<4 and i<7:              #vérification diagonale croissante (code)
        try:
            if T[(L[0]-3+i,L[1]+3-i)]==joueur:
                C+=1
            else:
                C=0
            i+=1
        except:
            i+=1
    
    if C==4:
        end=1
        can1.itemconfig(texte, text='Victoire du joueur '+joueur, fill='white')
    
    #Si toutes les cases sont remplies, soit 42 tours en tout
    if tour==42:
        end=1
        can1.itemconfig(texte, text='Match nul !', fill='white')
    return
        

def Restart():  #creation ou recreation du jeu
    global joueur, T, end, tour, texte, limite
    can1.create_rectangle(10,10,800,686,fill='black')
    can1.create_text(100,50, text='Restart',fill='white',activefill='red', font=('Times New Roman', 20, 'bold'))
    can1.create_line(70,130,70,680,width=2, fill="white")
    can1.create_line(170,130,170,680,width=2, fill="white")
    can1.create_line(270,130,270,680,width=2, fill="white")
    can1.create_line(370,130,370,680,width=2, fill="white")
    can1.create_line(470,130,470,680,width=2, fill="white")
    can1.create_line(570,130,570,680,width=2, fill="white")
    can1.create_line(670,130,670,680,width=2, fill="white")
    can1.create_line(770,130,770,680,width=2, fill="white")
    can1.create_line(70,680,770,680,width=2, fill="white")
    texte = can1.create_text(400,50, text='Tour du joueur 1',fill='blue',font=('Times New Roman', 20, 'bold'))
    joueur = 'X'
    end=0
    tour=0
    T={}                     #(re)creation du dictionnaire qui contient le tableau
    for x in range(7):
        for y in range(6):
            T[(x,y)]="_"
    limite = [0,0,0]
    return

def move():#animation des pions
    global limite, pion
    limite[2] = limite[2]+10
    can1.coords(pion, limite[0],limite[2],limite[0]+80,limite[2]+80)
    #repetition du deplacement
    if limite[2]<limite[1]:
        root.after(16,move)
    return

def Placement(colonne): #placement des pions
    global joueur, T, texte, limite, pion
    n=0
    while T[(colonne,n)]!="_":
        n+=1
        if n==6:
            return
    T[(colonne,n)]=joueur
    #definition des limites pour l'animation
    limite = [80+colonne*100,590-n*90,100]
    
    if joueur=='X': #Creation du pion pour l'animation
        pion = can1.create_oval(80+colonne*100, 670-n*90, 160+colonne*100, 590-n*90, width=2, fill='blue')
        move()#animation puis changement de joueur et de texte
        joueur='O'
        can1.itemconfig(texte, text='Tour du joueur 2', fill='red')
    else:
        pion = can1.create_oval(80+colonne*100, 670-n*90, 160+colonne*100, 590-n*90, width=2, fill='red')
        move()
        joueur = 'X'
        can1.itemconfig(texte, text='Tour du joueur 1', fill='blue')
    #test de victoire apres chaque tour
    win(joueur,colonne,n)

Restart()
root.bind("<Button-1>", click)

root.mainloop()
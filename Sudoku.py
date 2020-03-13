"""Rémi Guillon Bony et Poupet Vincent"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model
import random



##################### Résoudre grille initialisée à la main #####################
def Programme_Init_grille_a_la_main(grille):
    
    model = cp_model.CpModel()
    
    #Variables
    for i in range(0,len(grille)):
        for j in range(0,len(grille)):
            if (grille[i][j]==0):
                grille[i][j]=model.NewIntVar(1, 9,"")
    
    #Contraintes sur les lignes
    for i in range(0,len(grille)):
        model.AddAllDifferent(grille[i]);
        
    #Contraintes sur les colonnes
    for j in range(0,len(grille)):
        liste_temp=[]
        for i in range(0,len(grille)):
            liste_temp.append(grille[i][j])
        model.AddAllDifferent(liste_temp)
        
    #Contraintes dans les carrés
    for i in range(0,len(grille),3):
        for j in range(0,len(grille),3):
            liste_temp=[]
            liste_temp.append(grille[i][j])
            liste_temp.append(grille[i][j+1])
            liste_temp.append(grille[i][j+2])
            liste_temp.append(grille[i+1][j])
            liste_temp.append(grille[i+1][j+1])
            liste_temp.append(grille[i+1][j+2])
            liste_temp.append(grille[i+2][j])
            liste_temp.append(grille[i+2][j+1])
            liste_temp.append(grille[i+2][j+2])
            model.AddAllDifferent(liste_temp)
    
    #Call solver
    solver=cp_model.CpSolver();
    status=solver.Solve(model);
    if status == cp_model.FEASIBLE:
        for i in range (len(grille)):
            for j in range (len(grille)):
                grille[i][j] = solver.Value(grille[i][j])
                
    #Affichage
    for i in range(len(grille)):
        for j in range (len(grille)):
            print(grille[i][j], end=' ')
            if((j+1)%3==0): print('',end='  ')
        if((i+1)%3==0) : print()
        print()
   
    
    
    
##################### Résoudre grille initialisée automatiquement #####################  
class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
        self.sudoku=[]

    def on_solution_callback(self):
        self.__solution_count += 1
        if self.__solution_count >= self.__solution_limit:
            for v in self.__variables:
                self.sudoku.append(self.Value(v))
            
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count       
        
        
def Programme_Init_grille_auto():
    
    difficulté = input('Entrer le chiffre correspondant à la difficulté voulue: \n 1:débutant \n 2:facile \n 3:moyen \n 4:difficile \n 5:très difficile \n')
    
    model = cp_model.CpModel()
        
    #grille vide
    grille=[[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    
    sudokuresolu=grille[:][:] #va être remplie plus tard d'une solution de sudoku
    
    #Création grille
    for i in range(0,len(grille)):
        for j in range(0,len(grille)):
            grille[i][j]=model.NewIntVar(1,9,"")
    
    #Contraintes sur les lignes
    for i in range(0,len(grille)):
        model.AddAllDifferent(grille[i]);
        
    #Contraintes sur les colonnes
    for j in range(0,len(grille)):
        liste_temp=[]
        for i in range(0,len(grille)):
            liste_temp.append(grille[i][j])
        model.AddAllDifferent(liste_temp)
        
    #Contraintes dans les carrés
    for i in range(0,len(grille),3):
        for j in range(0,len(grille),3):
            liste_temp=[]
            liste_temp.append(grille[i][j])
            liste_temp.append(grille[i][j+1])
            liste_temp.append(grille[i][j+2])
            liste_temp.append(grille[i+1][j])
            liste_temp.append(grille[i+1][j+1])
            liste_temp.append(grille[i+1][j+2])
            liste_temp.append(grille[i+2][j])
            liste_temp.append(grille[i+2][j+1])
            liste_temp.append(grille[i+2][j+2])
            model.AddAllDifferent(liste_temp)
    
    #Create a solver and solve.
    solver = cp_model.CpSolver()
    liste_temp = []
    for element in grille:
        for i in element:
            liste_temp.append(i)
    solution_limit=random.randint(1,1000)
    solution_printer = VarArraySolutionPrinterWithLimit(liste_temp, solution_limit)
    solver.SearchForAllSolutions(model, solution_printer)
       
    #Remplissage de la grille de sudoku contenant une solution possible
    index=0
    for i in range(0,len(sudokuresolu)):
        for j in range(0,len(sudokuresolu)):
            sudokuresolu[i][j]=solution_printer.sudoku[index]
            index+=1
            
    #Prendre en compte la difficulté et créer des cases "vides" dans la solution trouvée
    compteur=0
    liste_ij=[]    
    #très difficile
    if (difficulté=="5"):
        while(compteur<81-17):
            i=random.randint(0,8)         
            j=random.randint(0,8)
            if ([i,j] not in liste_ij):
                liste_ij.append([i,j])
                sudokuresolu[i][j]=0
                compteur+=1
                
    #difficile
    if (difficulté=="4"):
        while(compteur<81-26):
            i=random.randint(0,8)         
            j=random.randint(0,8)
            if ([i,j] not in liste_ij):
                liste_ij.append([i,j])
                sudokuresolu[i][j]=0
                compteur+=1
    
    #moyen
    if (difficulté=="3"):
        while(compteur<81-33):
            i=random.randint(0,8)         
            j=random.randint(0,8)
            if ([i,j] not in liste_ij):
                liste_ij.append([i,j])
                sudokuresolu[i][j]=0
                compteur+=1
            
    #facile
    if (difficulté=="2"):
        while(compteur<81-40):
            i=random.randint(0,8)         
            j=random.randint(0,8)
            if ([i,j] not in liste_ij):
                liste_ij.append([i,j])
                sudokuresolu[i][j]=0
                compteur+=1
            
    #très difficile
    if (difficulté=="1"):
        while(compteur<81-50):
            i=random.randint(0,8)         
            j=random.randint(0,8)
            if ([i,j] not in liste_ij):
                liste_ij.append([i,j])
                sudokuresolu[i][j]=0
                compteur+=1
            
            
    #Affichage grille à remplir
    for i in range(len(sudokuresolu)):
        for j in range (len(sudokuresolu)):
            print(sudokuresolu[i][j], end=' ')
            if((j+1)%3==0): print('',end='  ')
        if((i+1)%3==0) : print()
        print()
    
    #Affichage solution
    question="n"
    while(question=="n"):
        question = input("Do you want to see the solved Sudoku ? (y/n) \n")
        if(question=="y"):
            Programme_Init_grille_a_la_main(sudokuresolu)
        
        
if __name__=='__main__' :
    
    #initialisation de la grille à la main
    grille=[[0,1,5,6,3,8,9,7,0],
            [3,0,2,4,7,9,1,0,5],
            [7,8,0,2,1,5,0,6,4],
            [9,2,6,0,4,0,7,5,8], 
            [1,3,8,7,0,6,4,2,9], 
            [5,7,4,0,8,0,6,3,1], 
            [2,5,0,1,6,4,0,9,3], 
            [8,0,3,5,9,7,2,0,6], 
            [0,9,1,8,2,3,5,4,0]]
    #Programme_Init_grille_a_la_main(grille)
    
    
    Programme_Init_grille_auto()
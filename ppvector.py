#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__='Eduardo dos Santos Pereira'
__version__='1.0'
__date__='15/03/2011'

"""
    This file is part of PyGraWC.
    copyright : Eduardo dos Santos Pereira
    31 mar. 2011.

    PyGraWC is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyGraWC is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
    
Aplicativo: ppvector
versao: 1.0
Autor : Eduardo dos Santos Pereira (Pereira; E. S.)
data: 31/05/2011

obs.:
Parte do Projeto de Doutoramento em Astrofísica pelo Instituto Nacional
de Pesquisas Espaciais -INPE.

Objetivo do modulo corrente:
ppvector: Parallel Processing Vector
Modulo que calcula vetores em multiprocessos.

Exemplo:

import multiprocessing as mpg

#Inicializa-se os vetores da funcao e da variavel

fbt2= mpg.Array('d',[0 for i in range(self.np)]) #o d indica precisao 
dupla
zFB= mpg.Array('d',[self.zmax-i*deltaz for i in range(self.np)])  

#Defini-se a funcao que ira calcular os pontos do vetor fbt2 em paralelo
#k e o ponto do vetor onde se inicia o calculo
#E e o tamanho do subintervalo do vetor a ser calculado
#n e o numero do processo

def CalculusRenais(k,E,n):
                
    for i in range(E):
        z=zFB[k]
        fbt2[k]=self.fbstruc(z)
        k+=1
        
Dmatriz=self.np  # Tamanho do vetor fbt2
C1= ppvector(Dmatriz,CalculusRenais) #Cria-se uma instacia
C1.runProcess() #Ativa o metodo que calcula em paralelo.
"""

import multiprocessing as mpg


##@file ppvector.py
##@author  Eduardo dos Santos Pereira <pereira.somoza@gmail.com>
##@version 1.0
##@section LICENSE
# This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License as
#published by the Free Software Foundation; either version 2 of
#the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#General Public License for more details at
#http://www.gnu.org/copyleft/gpl.html
##@section DESCRIPTION
#This program is used to calculate, in parallel, by python module 
#multiprocessing, points in vector. Optimization for multicore machines.

class ppvector:
    """      
    ppvector: Parallel Processing Vector
    This program is used to calculate, in parallel, by python module 
    multiprocessing, points in vector. Example:
    
    import multiprocessing as mpg
    #Start the vector of result an the vector with valuer of variables
    fbt2= mpg.Array('d',[0 for i in range(self.np)]) 
    zFB= mpg.Array('d',[self.zmax-i*deltaz for i in range(self.np)])  
    #Define the function that will run in parallel.
    #k is a point of vector that start the caculation
    #E  is the range of the vector
    #n is the processor
    
    def fun(x):
        return x*x
        
    def Calcula(k,E,n):
        for i in range(E):
            z=zFB[k]
            fbt2[k]=fun(z)
            k+=1
        
    Dmatriz=self.np  # The dimension of the vector
    C1= ppvector(Dmatriz,Calcula) 
    C1.runProcess() #run the calculus in parallel   
    """
      
    def __init__(self,Dmatriz,func):
        '''
        Dmatiz: The dimension of the vector
        func:  function that will run in parallel
        '''
        self.Dmatriz=Dmatriz
        self.func=func
    
    def __CalculusRenais(self,func,k,E,n):
        func(k,E,n)
        
                
                
    def __acaoParalera(self,n,q,Dmatriz,func,n_process):     
        E=Dmatriz/n_process
        k=n*E
        q.put(self.__CalculusRenais(func,k,E,n))
    
    def runProcess(self):   
        '''
        Calculate, in sub range, points of vector in parallel. For 
        multicore machines.
        
        '''
        
        n_process=2*mpg.cpu_count()
        subprocess=[]
        
        
        for i in range(n_process):
            q = mpg.Queue()
            p=mpg.Process(target=self.__acaoParalera,\
                args=(i,q,self.Dmatriz,self.func,n_process))
            p.start()
            subprocess.append(p)
            
        while subprocess:
            subprocess.pop().join()

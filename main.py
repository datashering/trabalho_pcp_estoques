import numpy as np
import math
from functions import *

if __name__ == "__main__":

    #Dicionário que vai conter todos os parâmetros do problema
    dados = {}

    #parâmetros deterministicos
    dados['H'] = 96         #horizonte de tempo (em semanas) 
    dados['h0'] = 3000      #estoque inicial
    dados['Cp'] = 50        #custo de compra de uma unidade
    dados['Cs'] = 500       #custo de pedido (setup)
    dados['Cf'] = 10000     #custo fixo de faltante
    dados['Cv'] = 100       #custo variavel de faltante
    dados['i'] = 0.2        #taxa de interesse

    #parâmetros de variáveis estocásticas
    # X -> demanda semanal ~ N(mux,sx)
    dados['mux'] = 1000
    dados['sx'] = 50
    # L -> lead-time ~ N(mul,sl)
    dados['mul'] = 5
    dados['sl'] = 1

    ######### Otimização do custo total ###########
    
    melhor_E = 0    # E*
    melhor_T = 0    # T*
    melhor_custo = 100000000000000  # custo*

    #testamos todos valores possiveis de T
    for T in range(1,97):
        #dado um T calculamos o E*
        E = otimiza_E(dados,T)
        if E == False:
            break
        
        #dados T e E* calculamos os custos
        custo = custo_total(dados,E,T)
        
        if custo < melhor_custo:
            #atualizamos E*, T* e custo*
            melhor_E = E
            melhor_T = T
            melhor_custo = custo

    print(melhor_E, melhor_T, melhor_custo)



    ######### Simulação da poítica encontrada ########## 

    # TO BE CONTINUE

    

       


    




    


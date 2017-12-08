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
    dados['Cf'] = 100000    #custo fixo de faltante
    dados['Cv'] = 100       #custo variavel de faltante
    dados['i'] = 0.2        #taxa de interesse

    #parâmetros de variáveis estocásticas
    # X -> demanda semanal ~ N(mux,sx)
    dados['mux'] = 100
    dados['sx'] = 50
    # L -> lead-time ~ N(mul,sl)
    dados['mul'] = 5
    dados['sl'] = 1

    ######### Otimização do custo total ###########
    
    melhor_E = 0    # E*
    melhor_T = 0    # T*
    melhor_custo = 100000000000000  # custo*

    #testamos todos valores possiveis de T
    for T in range(1, dados['H']+1):
        
        #dado um T calculamos o E*
        E = otimiza_E(dados,T)
        custo, RF = custo_total(dados,E,T)
        if E == False:
            break

        if custo < melhor_custo:
            #atualizamos E*, T* e custo*
            melhor_E = E
            melhor_T = T
            melhor_custo = custo
    ######### Simulação dos resultados ##########
    
    #>>>>> Cenário - 1: Situação normal
    custos = []
    for i in range(100):
        demanda = gera_demanda(1, dados)
        ct = simula(dados, melhor_E+1000, melhor_T, demanda)
        custos.append(ct)
    
    print("Otimização: {:f}".format(melhor_custo))
    print("Simulação: {:f}".format(np.mean(custos)))

    print(melhor_T, melhor_E)

    #>>>>> Cenário - 2: A média da demanda pode aumentar
    #demanda = gera_damanda(2, dados)
    #custos = []
    #for i in range(100):
    #    ct = simula(dados, E, T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))
   
    #>>>>> Cenário - 3: A média da demenda pode diminuir
    #demanda = gera_damanda(3, dados)
    #custos = []
    #for i in range(100):
    #    ct = simula(dados, E, T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))
  
    #>>>>> Cenário - 4: A média da demanda pode alterar para cima ou para baixo
    #demanda = gera_damanda(4, dados)
    #custos = []
    #for i in range(100):
    #    ct = simula(dados, E, T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))

       


    




    


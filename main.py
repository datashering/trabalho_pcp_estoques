import numpy as np
import math
from functions import *

if __name__ == "__main__":
    #Dicionário que vai conter todos os parâmetros do problema
    dados = {}

    #parâmetros deterministicos
    dados['H'] = 96         #horizonte de tempo (em semanas) 
    dados['h0'] = 2000      #estoque inicial
    dados['Cp'] = 800        #custo de compra de uma unidade
    dados['Cs'] = 5000       #custo de pedido (setup)
    dados['Cf'] = 100000    #custo fixo de faltante
    #dados['Cv'] = 100       #custo variavel de faltante
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
    #custos = []
    #for i in range(100):
    #    demanda = gera_demanda(1, dados)
    #    ct = simula(dados, melhor_E, melhor_T, demanda)
    #    custos.append(ct)

    testa_custo, testa_E, testa_T = modifica(dados,melhor_E,melhor_T,1)

    print("Otimização: {:f}, {:f}, {:f}".format(melhor_custo, melhor_T, melhor_E))
    print("Modifica: {:f}, {:f}, {:f}".format(testa_custo, testa_T, testa_E))

    #>>>>> Cenário - 2: A média da demanda pode aumentar
    #custos = []
    #for i in range(100):
    #    demanda = gera_demanda(2, dados)
    #    ct = simula(dados, melhor_E, melhor_T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))
   
    #>>>>> Cenário - 3: A média da demenda pode diminuir
    #custos = []
    #for i in range(100):
    #    demanda = gera_demanda(3, dados)
    #    ct = simula(dados, melhor_E, melhor_T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))
   
    #>>>>> Cenário - 4: A média da demanda pode alterar para cima ou para baixo
    #custos = []
    #for i in range(100):
    #    demanda = gera_demanda(4, dados)
    #    ct = simula(dados, melhor_E, melhor_T, demanda)
    #    custos.append(ct)
    #print(np.mean(custos))
 
   
   

       


    




    


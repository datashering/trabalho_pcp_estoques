import numpy as np
import math

def simula(dados, E, T, demanda):

    #Entradas do dicionario
    h = [0 for i in range(H+1)] 
    
    mux = dados['mux']                                                            #Media da demanda durante 1 semana (Periodo t)
    sx = dados['sx']                                                         #Desvio padrao da demanda durante 1 semana (Periodo t)
    H = dados['H']
    mul = dados['mul']
    sl = dados['sl']
    muv = dados['muv']
    sv = dados['sv']
    Cf = dados['Cf']
    Cp = dados['Cp']
    Cs = dados['Cs']
    h[0] = dados['h0']
    i_rate = dados['i']

    custos_totais = []  
    faltante = [0 for i in range(H+1)]
    
    for t in range(H):                                                      #Loop que define quanto sera pedido e se havera faltante
        
        pedido = 0
        
        if (demanda[t] > h[t]):
            faltante[t] = demanda[t]-h[t]
            h[t] = 0
        else:
            h[t] -= demanda[t]

        if t % T == 0:
            lead_time = round(np.random.normal(mul, sl))
            pedido = max(0, E - h[t])
            #print("pediu: {:d}".format(pedido))
            if t + lead_time <= H:
                h[t+lead_time] += pedido
        
        custos = (pedido*Cp, min(faltante[t]*Cf, Cf))                       #Tupula contendo os custos que variam com t
        custos_totais.append(custos)                                        #Valor dos custos totais que variam com t

        #print("iteração: {:d}".format(t))
        #print("demanda: {:d}".format(demanda[t]))
        #print("estoque: {:d}".format(h[t]))
        #print("faltante: {:d}".format(faltante[t]))
        #print("custos:{0}".format(custos,))
        #print("--------------------------------------------")
        h[t+1] += h[t]

    custo_estoque = (sum(h)/len(h))*Cp*i
    custo_pedido = math.ceil(H/T)*Cs
    custos_totais_sum = (sum([v[0] for v in custos_totais]), sum([v[1] for v in custos_totais]))

    CT = custo_estoque + custo_pedido + sum(custos_totais_sum)
    #print(CT)
    #print(custos_totais_sum)

    return (CT)


    

       


    




    


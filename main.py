import numpy as np
import math

if __name__ == "__main__":
    
    #Vetor de demandas
    mu_d = 10000                                                            #Media da demanda durante 1 semana (Periodo t)
    sigma_d = 520                                                           #Desvio padrao da demanda durante 1 semana (Periodo t)
    demanda = [int(v) for v in np.random.normal(mu_d, sigma_d, 100)]          #Funcao que gera a demanda para o periodo H
    mu_dv = 12000                                                           #Media da demanda durante 1 semana (Periodo t)
    sigma_dv = 580                                                          #Desvio padrao da demanda durante 1 semana (Periodo T)
    
    #parametros lead time
    mu_l = 6                                                                #Media do lead time
    sigma_l = 2                                                             #Desvio padrao do lead time
    
    #parametros
    PV = 3                                                                  #Período no qual a demanda varia
    cff = 100000                                                            #Custo fixo por atraso
    cvf = 100                                                               #Custo variavel por unidade atrasada
    cp = 50                                                                 #Custo de pedido de uma peca
    i_rate = 0.2                                                            #Taxa de oportunidade de investimento
    coin = 0                                                                #Numero aleatorio que definira se a demanda de 3 meses sera alte                                                                            rada ou nao

    custos_totais = []  
    H = 96                                                                  #Intervalo total da simulacao
    faltante = [0 for i in range(H+1)]                  
    h = [0 for i in range(H+1)] 
    h[0] = 60000                                                            #Estoque inicial
    T = 6                                                                   #Periodo que e realizado o pedido
    E = 100000                                                              #Teto ideal para se alcancar ao realizar o pedido
    
    for t in range(H):                                                      #Loop que define quanto sera pedido e se havera faltante
        
        pedido = 0
        coin = math.ceil(np.random.normal(0,1))
        print(coin)
        if coin >= 2:
            demanda[t+PV] = int(np.random.normal(mu_dv, sigma_d))
            print ("mudou", demanda[t+PV])
        
        if (demanda[t] > h[t]):
            faltante[t] = demanda[t]-h[t]
            h[t] = 0
        else:
            h[t] -= demanda[t]

        if t % T == 0:
            lead_time = round(np.random.normal(mu_l,sigma_l))
            pedido = max(0, E - h[t])
            print("pediu: {:d}".format(pedido))
            if t + lead_time <= H:
                h[t+lead_time] += pedido
        
        custos = (pedido*cp, min(faltante[t]*cff, cff), faltante[t]*cvf)    #Tupula contendo os custos que variam com t
        custos_totais.append(custos)                                        #Valor dos custos totais que variam com t

        print("iteração: {:d}".format(t))
        print("demanda: {:d}".format(demanda[t]))
        print("estoque: {:d}".format(h[t]))
        print("faltante: {:d}".format(faltante[t]))
        print("custos:{0}".format(custos,))
        print("--------------------------------------------")
        h[t+1] += h[t]

    custo_estoque = (sum(h)/len(h))*cp*i_rate
    custo_pedido = math.ceil(H/T)
    custos_totais_sum = (sum([v[0] for v in custos_totais]), sum([v[1] for v in custos_totais]), sum([v[2] for v in custos_totais]))

    CT = custo_estoque + custo_pedido + sum(custos_totais_sum)
    print(CT)
    print(custos_totais_sum)


    

       


    




    


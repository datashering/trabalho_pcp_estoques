import numpy as np
import math

if __name__ == "__main__":
    
    #Vetor de demandas
    mu_d = 10000
    sigma_d = 520
    demanda = [int(v) for v in np.random.normal(mu_d, sigma_d, 96)]
    
    #parametros lead time
    mu_l = 6
    sigma_l = 2
    
    #parametros
    cff = 100000
    cvf = 100
    cp = 50
    i_rate = 0.2
    
    custos_totais = []
    H = 96
    faltante = [0 for i in range(H+1)]
    h = [0 for i in range(H+1)]
    h[0] = 60000
    T = 6
    E = 100000
    
    for t in range(H):
        pedido = 0
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
        
        custos = (pedido*cp, min(faltante[t]*cff, cff), faltante[t]*cvf)
        custos_totais.append(custos)

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


    

       


    




    


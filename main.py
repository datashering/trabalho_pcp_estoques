import numpy as np

if __name__ == "__main__":
    
    #Vetor de demandas
    mu_d = 10000
    sigma_d = 520
    demanda = np.random.normal(mu_d, sigma_d, 96)
    
    #parametros lead time
    mu_l = 6
    sigma_l = 2
    
    #parametros
    faltante = [0 for i in range(96)]
    h = [0 for i in range(104)]
    h[0] = 60000
    T = 6
    Q = 100000
    
    for t in range(96):
        if (demanda[t] > h[t]):
            faltante[t] = demanda[t]-h[t]
            h[t] = 0
        else:
            h[t] -= demanda[t]

        if (t+1)%8 == 0:
            lead_time = round(np.random.normal(mu_l,sigma_l))
            h[t+lead_time] += Q - h[t]

        h[t+1] += h[t]

    print(faltante)
       


    




    


#===============================================
#        Funções Trabalho de pcp
#===============================================
import scipy.stats as st
import numpy as np
from math import sqrt, log, pi, ceil

def otimiza_E(dados,T):
    """ 
    Função que utiliza a formula obtida após derivar o custo total em relação e E
    e igualar a 0, para calular o E* 
    
    argumentos:
    dados: Parametros do problema presentes na formula do custo total
    T: Período de revisão definido
    """    

    #W -> demanda no T + L ~ Normal(muw,sw)
    muw = (T + dados['mul'])*dados['mux']
    sw = sqrt(dados['mul']*dados['sx']**2 + dados['mux']**2 * dados['sl']**2 ) 
    
    if log((2*dados['H']*dados['Cf'])/(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw)) < 0:
        return False 

    E = sqrt(2 * sw**2 * log((2*dados['H']*dados['Cf'])/(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw))) + muw

    return E

def custo_total(dados, E, T):
    """ 
    Função que calcula os custos totais de acordo com o estoque alvo e período
    de rerisão determinados
    
    argumentos:
    dados: Parametros do problema presentes na formula do custo total
    E: Nível de estoque alvo
    T: Período de revisão definido
    """
    #W -> demanda no T + L ~ Normal(muw,sw)
    muw = (T + dados['mul'])*dados['mux']
    sw = ( (T + dados['mul'])*dados['sx']**2 + dados['mux']**2 * dados['sx']**2 )**(1/2)

    #Rísco de faltante -> P(W > E)
    RF = 1 - st.norm.cdf(E, muw, sw)
    #print(RF)

    CT = (dados['H']*dados['mux'] - dados['h0'])*dados['Cp'] + (E - dados['mux']*dados['mul'])/2 * dados['Cp']*dados['i'] + \
          ceil(dados['H']/T)*(dados['Cs'] + RF*dados['Cf'])
    
    
    return CT, RF

def simula(dados, E, T, demanda):

    #Entradas do dicionario
    
    mux = dados['mux']                                                            #Media da demanda durante 1 semana (Periodo t)
    sx = dados['sx']                                                         #Desvio padrao da demanda durante 1 semana (Periodo t)
    H = dados['H']
    mul = dados['mul']
    sl = dados['sl']
    #muv = dados['muv']
    #sv = dados['sv']
    Cf = dados['Cf']
    Cp = dados['Cp']
    Cs = dados['Cs']
    i = dados['i']

    custos_totais = []  
    faltante = [0 for i in range(H+1)]
    h = [0 for i in range(H+1)] 
    h[0] = dados['h0']
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
            
            if t + lead_time <= H:
                h[t+lead_time] += pedido
        
        custos = (pedido*Cp, min(faltante[t]*Cf, Cf))                       #Tupula contendo os custos que variam com t
        custos_totais.append(custos)                                        #Valor dos custos totais que variam com t

        h[t+1] += h[t]

    custo_estoque = (sum(h)/len(h))*Cp*i
    custo_pedido = ceil(H/T)*Cs
    custos_totais_sum = (sum([v[0] for v in custos_totais]), sum([v[1] for v in custos_totais]))

    CT = custo_estoque + custo_pedido + sum(custos_totais_sum)

    return (CT)

def gera_demanda(cenario, dados):

    prob = 0.10
    mux_1 = dados['mux']
    mux_2 = 1.15 * dados['mux']
    mux_3 = 0.85 * dados['mux']
    demanda = [0 for t in range(dados['H'])]

    if cenario == 1:

        demanda = [int(v) for v in np.random.normal(dados['mux'], dados['sx'], dados['H'])]

    elif cenario == 2:
        for t in range(dados['H']):
            coin = np.random.binomial(1, prob)
            if(coin == 1):
                demanda[t] = np.random.normal(mux_2, dados['sx'])
                mux_aux = mux_1
                mux_1 = mux_2
                mux_2 = mux_aux
            else:
                demanda[t] = np.random.normal(mux_1, dados['sx'])

    
    elif cenario == 3:
        for t in range(dados['H']):
            coin = np.random.binomial(1, prob)
            if(coin == 1):
                demanda[t] = np.random.normal(mux_3, dados['sx'])
                mux_aux = mux_1
                mux_1 = mux_3
                mux_3 = mux_aux
            else:
                demanda[t] = np.random.normal(mux_1, dados['sx'])

    elif cenario == 4:
        for t in range(dados['H']):

            coin = np.random.multinomial(1, [1-prob] + [prob] + [prob])

            if(coin[0] == 1):
                demanda[t] = np.random.normal(mux_1, dados['sx'])

            elif(coin[1] == 1):
                demanda[t] = np.random.normal(mux_2, dados['sx'])
                mux_aux = mux_1
                mux_1 = mux_2
                mux_2 = mux_aux

            elif(coin[2] == 1):
                demanda[t] = np.random.normal(mux_3, dados['sx'])
                mux_aux = mux_1
                mux_1 = mux_3
                mux_3 = mux_aux
        


    return demanda

def simula_100(dados,E,T, cenario):
    
    custos = []
    for i in range(1000):
        demanda = gera_demanda(cenario,dados)
        custo = simula(dados,E,T,demanda)
        custos.append(custo)
    
    return sum(custos)/len(custos)
    

def modifica(dados,E,T, cenario):
    
    var_T = list(range(1,96))
    var_E = [round(0.05*i,2) for i in range(-10,11)]
    
    melhor_T = T
    melhor_E = E
    melhor_custo = simula_100(dados, E, T, cenario)
    for i in range(1000):
        change = False

        for i in range(95):
            T_teste = var_T[i]
            custo_medio = simula_100(dados, melhor_E, T_teste, cenario)
            if custo_medio < melhor_custo:
                print('T')
                melhor_custo = custo_medio
                melhor_T = T_teste
                change = True

        for  i in range(21):
            E_teste = E + E*var_E[i]
            custo_medio = simula_100(dados, E_teste, melhor_T, cenario)
            if custo_medio < melhor_custo:
                print('E')
                melhor_custo = custo_medio
                melhor_E = E_teste
                change = True
        
        if change == False:
            break
    
    return melhor_custo, melhor_E, melhor_T


















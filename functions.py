#===============================================
#        Funções Trabalho de pcp
#===============================================
import scipy.stats as st
import numpy as np
from math import sqrt, log, pi

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
    
    print("-----------------------------------------------------")
    print(T)
    print("Cp: {:f}     i: {:f}     T: {:f}     sqrt(2*pi): {:f}     sw: {:f}".format(dados['Cp'], dados['i'], T, sqrt(2*pi), sw))
    print("Numerador: {:f}".format(2*dados['H']*dados['Cf']))
    print("Denominador: {:f}".format(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw))            
    print("log calculado: {:f}".format(log((2*dados['H']*dados['Cf'])/(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw)))) 
    if log((2*dados['H']*dados['Cf'])/(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw)) < 0:
        return False 
    E = sqrt(2 * sw**2 * log((2*dados['H']*dados['Cf'])/(dados['Cp']*dados['i']*T*sqrt(2*pi)*sw))) + muw
    print(E)
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

    CT = (dados['H']*dados['mux'] - dados['h0'])*dados['Cp'] + (E - dados['mux']*dados['mul'])*dados['Cp']*dados['i']/2 + \
          (dados['H']/T)*(dados['Cs'] + RF*dados['Cf'])

    
    return CT

def simula(dados, E, T, demanda):

    #Entradas do dicionario
    h = [0 for i in range(H+1)] 
    
    mux = dados['mux']                                                            #Media da demanda durante 1 semana (Periodo t)
    sx = dados['sx']                                                         #Desvio padrao da demanda durante 1 semana (Periodo t)
    H = dados['H']
    mul = dados['mul']
    sl = dados['sl']
    #muv = dados['muv']
    sv = dados['sv']
    cff = dados['Cf']
    cp = dados['Cp']
    cs = dados['Cs']
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

def gera_demanda(cenario, dados):

    coin = [int(v) for v in np.random.binomial(1, dados['p'], dados['H'])]

    if cenario == 1:
        demanda = [int(v) for v in np.random.normal(dados['mux'], dados['sx'], H)]

    elif cenario == 2:
        demanda = [int(v) for v in (np.random.normal(dados['mux'], dados['sx'], H) + coin[v]*dados['pena'])]

    elif cenario == 3:
        demanda = [int(v) for v in (np.random.normal(dados['mux'], dados['sx'], H) - coin[v]*dados['pena'])]

    return demanda

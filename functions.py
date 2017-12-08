#===============================================
#        Funções Trabalho de pcp
#===============================================
import scipy.stats as st
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





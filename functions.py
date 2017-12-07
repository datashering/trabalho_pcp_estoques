#===============================================
#        Funções Trabalho de pcp
#===============================================
import scipy.stats as st

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
    sw = ( (T + dados['mul'])*dados['sx']**2 + dados['mux']**2 * dados['sx']**2 )**(1/2)
    
    prob = 1 - (T*dados['Cp']*dados['i'])/(dados['H']*dados['Cv'])
    E = st.norm.ppf(prob,muw,sw)

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

    #Número médio de faltantes ->
    NMF = (st.norm.pdf(E, muw, sw) - 1 + st.norm.cdf(E, muw, sw))*sw

    CT = (dados['H']*dados['mux'] - dados['h0'])*dados['Cp'] + (E - dados['mux']*dados['mul'])*dados['Cp']*dados['i']/2 + \
          (dados['H']/T)*(dados['Cs'] + RF*dados['Cf'] + NMF*dados['Cv'])
    
    return CT





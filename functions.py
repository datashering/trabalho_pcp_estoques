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
    muw = (T + data['mul')]*data['mux']
    sw = ( (T + data['mul'])*data['sx']**2 + data['mux']**2 * data['sx']**2 )**(1/2)
    
    prob = 1 - (T*data['Cp']*data['i'])/(data['H']*data['Cv'])
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
    
    CT = (H*data['mux'] - data['h0'])*data['Cp'] + (E - data['mux']*data['mul'])*data['Cp']*data['i']/2 + \
          data['H']/T*(data['Cs'] + RF*data['Cf'] + NMF*data['Cv'])

    return CT





'''
Funções genéricas para uso em scripts
que gerem dashboards streamlit
'''

import streamlit as st

@st.cache(allow_output_mutation=True)
def load_data(nrows:int = None, date_f:str=None) -> pd.DataFrame:
    '''
    Função para carregar o conjunto de dados
    :rtype: pd.Dataframe
    :param nrows: número de linhas a ser lida do conjunto de dados
    :return: DataFrame
    '''

    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(str.lower, axis='columns', inplace=True)
    data.rename(columns={'lat': 'latitude', 'long': 'longitude'}, inplace=True)
    data[date_f] = pd.to_datetime(data[date_f])
    return data
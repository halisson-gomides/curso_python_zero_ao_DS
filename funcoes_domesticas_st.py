'''
Funções genéricas para uso em scripts
que gerem dashboards streamlit
'''

from streamlit import cache


@cache(allow_output_mutation=True)
def load_data(data_url: str, date_f: str = None, nrows: int = None) -> 'DataFrame':
    '''
    Função para carregar o conjunto de dados
    :rtype: pd.Dataframe
    :param nrows: número de linhas a ser lida do conjunto de dados
    :return: DataFrame

    Args:
        date_f (None): campo data para ser convertido em datetime
    '''

    import pandas as pd
    import dateutil.parser

    data = pd.read_csv(data_url, nrows=nrows)
    data.rename(str.lower, axis='columns', inplace=True)
    data.rename(columns=dict(lat='latitude', long='longitude'), inplace=True)
    if date_f is not None:
        data[date_f] = data[date_f].apply(lambda x: dateutil.parser.parse(x).strftime("%d/%m/%Y"))
        # data[date_f] = pd.to_datetime(data[date_f], format="%d/%m/%Y")
    return data

'''
### Exercícios da Aula 05
---

Author : Halisson S. Gomides - halisson.gomides@gmail.com

Date : 09/02/2021

---

### Conjunto de dados House Sales in King County, USA
>https://www.kaggle.com/harlfoxem/housesalesprediction
'''

import pandas as pd
import streamlit as st


DATA_URL = 'dados/originais/kc_house_data.csv.zip'
DATE_F = 'date'

@st.cache(allow_output_mutation=True)
def load_data(nrows:int = None) -> pd.DataFrame:
    '''
    Função para carregar o conjunto de dados
    :rtype: pd.Dataframe
    :param nrows: número de linhas a ser lida do conjunto de dados
    :return: DataFrame
    '''

    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(str.lower, axis='columns', inplace=True)
    data.rename(columns={'lat': 'latitude', 'long': 'longitude'}, inplace=True)
    data[DATE_F] = pd.to_datetime(data[DATE_F]).tz_convert("America/New_York")
    return data


def show_dimensions(df):
    '''
    Imprime as Dimensões do dataframe
    Keyword arguments:
    df -- dataframe

    '''
    st.write(f'Numero de linhas: {df.shape[0]}', end='\n')
    st.write(f'Numero de colunas: {df.shape[1]}', end='\n\n')
    return None


st.title('Aula #05 - Funções e Organização de Código')
st.header('House Rocket Company')
st.markdown(f"<span style='color: blue;font-size: 24px;font-weight: bold;'>Welcome to House Rocket Data Analisys</span>", unsafe_allow_html=True)


# Carregando o conjunto de dados
dfhouses = load_data(100000)

if st.checkbox('visualizar dados'):
    st.subheader('Dados Crus')
    st.dataframe(dfhouses)

# Verificando o Formato do Dataframe
st.subheader('Verificando o formato do DataFrame')
show_dimensions(dfhouses)

# Filtro de Quartos
bedrooms = st.sidebar.multiselect(
    'Numero de Quartos',
    dfhouses['bedrooms'].sort_values().unique()
)

st.write('Filtros aplicados:', bedrooms)

# plotar mapa
st.subheader('House Rocket Map')
is_check = st.checkbox('visualizar mapa')

# Filtros
price_min = int(dfhouses['price'].min())
price_max = int(dfhouses['price'].max())
price_mean = int(dfhouses['price'].mean())

price_slider = st.slider('Range de Preço',
                         price_min,
                         price_max,
                         price_mean)

if is_check:
    # select rows
    houses = dfhouses.query('price <= @price_slider &'
                            'bedrooms in @bedromms')[['id', 'latitude', 'longitude', 'price']]

    st.dataframe(houses)

    # desenha mapa
    st.map(houses)

# Verificando se existem dados nulos
st.subheader('Verificando se existem dados nulos')
st.write(dfhouses.isnull().sum())

# Verificando se existem dados duplicados
st.subheader('Verificando se existem dados duplicados')
st.write(dfhouses['id'].value_counts())
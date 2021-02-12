'''
### Exercícios da Aula 06
Curso de Zero ao DS: https://www.youtube.com/watch?v=3kWM5Q4CYnw
---

Author : Halisson S. Gomides - halisson.gomides@gmail.com

Date : 11/02/2021

---

### Conjunto de dados House Sales in King County, USA
>https://www.kaggle.com/harlfoxem/housesalesprediction

# Requisição do CEO
1. Gostaria de ter um lugar único onde eu possa observar o portfolio da House Rocket. Nesse portfólio, eu tenho interesse:
    1.1- Filtros dos imóveis por um ou várias regiões
    1.2- Escolher uma ou mais variáveis para visualizar.
    1.3- Observar o número total de imóveis, a média de preço, a média da sala de estar e também a média do preço por metro
    quadrado em cada um dos códigos postais.
    1.4- Analisar cada uma das colunas de um modo mais descrito.
    1.5- Um mapa com a densidade de portfólio por região e também densidade de preço
    1.6- Checar a variação anual de preço.
    1.7- Checar a variação diária de preço.
    1.8- Conferir a distribuição dos imóveis por:
        - preço,
        - Número de quartos;
        - Número de banheiros;
        - Número de andares;
        - Vista para a água ou não
'''

import funcoes_domesticas_st as fd
import streamlit as st
import pandas as pd
import numpy as np
import folium as fol
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout='wide')

# Cabeçalho
st.title('Aula #06 - Tipos de Visualização de Dados')
st.subheader('House Rocket Company')
st.markdown(f"<span style='color: blue;font-size: 20px;font-weight: bold;'>Welcome to House Rocket Data Analisys</span>", unsafe_allow_html=True)


# Carregando o conjunto de dados
dfhouses = fd.load_data(data_url='dados/originais/kc_house_data.csv.zip', date_f='date')


# ------------------------
#  Adicionando novos atributos
# ------------------------
# Preço por metro quadrado
dfhouses['size_m2'] = dfhouses['sqft_living'].apply(lambda x: x * 0.092903)
dfhouses['price_m2'] = dfhouses['price'] / dfhouses['size_m2']

# ------------------------
#  Data Overview
# 1.2- Escolher uma ou mais variáveis para visualizar.
# ------------------------

# Filtros

# campos_default = ['id', 'price', 'zipcode', 'size_m2', 'price_m2']

f_atributos = st.sidebar.multiselect('Selecione as colunas', dfhouses.columns.tolist())
f_zipcode = st.sidebar.multiselect('Selecione o zipcode', dfhouses['zipcode'].sort_values(kind='mergesort').unique())

if f_zipcode != [] and f_atributos != []:
    dffiltrado = dfhouses.loc[dfhouses['zipcode'].isin(f_zipcode), f_atributos]

elif f_zipcode != [] and f_atributos == []:
    dffiltrado = dfhouses.loc[dfhouses['zipcode'].isin(f_zipcode), :]

elif f_zipcode == [] and f_atributos != []:
    dffiltrado = dfhouses.loc[:, f_atributos]
    
else:
    dffiltrado = dfhouses.copy()

if st.checkbox('visualizar dados crus'):
    st.markdown(f"<span style='color: darkgreen;font-size: 15px;'>Amostra dos Dados Crus</span>",
                unsafe_allow_html=True)
    st.dataframe(dffiltrado.sample(20))

c1, c2 = st.beta_columns((1.2, 1))
# ------------------------
# a média de preço, a média da sala de estar e também a média do preço por metro
# quadrado em cada um dos códigos postais.
# ------------------------

# Contagem por código postal
df1 = dffiltrado[['id', 'zipcode']].groupby('zipcode').count().reset_index()
# Média de preço por código postal
df2 = dffiltrado[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
# Média do tamanho por código postal
df3 = dffiltrado[['size_m2', 'zipcode']].groupby('zipcode').mean().reset_index()
# Média do preço por metro quadrado por código postal
df4 = dffiltrado[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

# merge
m1 = pd.merge(df1, df2, on='zipcode', how='inner')
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
dfmerged = pd.merge(m2, df4, on='zipcode', how='inner')
dfmerged.columns = ['zipcode', 'total_houses', 'mean_price', 'mean_size', 'mean_price_m2']

c1.markdown("<span style='color:CadetBlue;font-size: 15px; font-weight: bold'>Valores médios</span>",
            unsafe_allow_html=True)
c1.dataframe(dfmerged, height=580)

# ------------------------
# Estatísticas descritivas
# ------------------------
num_atributos = dffiltrado.select_dtypes(include=['int64', 'float64'])
media = pd.DataFrame(num_atributos.apply(np.mean))
mediana = pd.DataFrame(num_atributos.apply(np.median))
std = pd.DataFrame(num_atributos.apply(np.std))
max_ = pd.DataFrame(num_atributos.apply(np.max))
min_ = pd.DataFrame(num_atributos.apply(np.min))

dfestatistica = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
dfestatistica.columns = ['atributos', 'max', 'min', 'media', 'mediana', 'desvio_padrao']

c2.markdown(f"<span style='color: CadetBlue;font-size: 15px; font-weight: bold'>Estatística Descritiva</span>",
                unsafe_allow_html=True)
c2.dataframe(dfestatistica, height=580)

# ------------------------
#  Densidade de Portfolio
# ------------------------

st.title('Overview por Região')

c1, c2 = st.beta_columns((1, 1))
c1.header('Densidade de Portfolio')

df = dffiltrado.sample(10)

# Base Map - Folium
densidade_map = fol.Map(location=[dffiltrado['latitude'].mean(),
                                 dffiltrado['longitude'].mean()],
                       default_zoom_start=15)
marker_cluster = MarkerCluster().add_to(densidade_map)
for name, row in df.iterrows():
    fol.Marker( [row['latitude'], row['longitude']],
               popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(row['price'],
                                                                                                                    row['date'],
                                                                                                                   row['sqft_living'],
                                                                                                                   row['bedrooms'],
                                                                                                                   row['bathrooms'],
                                                                                                                   row['yr_built'])).add_to(marker_cluster)

with c1:
    folium_static(densidade_map)


# Mapa de preço por região
c2.header('Densidade de Preço')

df = dffiltrado[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df.columns = ['zip', 'price']
df = df.sample(10)

regiao_map = fol.Map(location=[dffiltrado['latitude'].mean(),
                                 dffiltrado['longitude'].mean()],
                       default_zoom_start=15)

geourl = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
geofile = fd.load_geofile(geourl)
regiao_map.choropleth(data=df, geo_data=geofile, columns=['zip', 'price'], key_on='feature.properties.ZIP',
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      legend_name='MEDIA PREÇO')
with c2:
    folium_static(regiao_map)
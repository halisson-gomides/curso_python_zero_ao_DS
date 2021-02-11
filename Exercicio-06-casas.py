'''
### Exercícios da Aula 06
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
    1.3- Observara o número total de imóveis, a média de preço, a média da sala de estar e também a média do preço por metro
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

import pandas as pd
import streamlit as st
import funcoes_domesticas_st as fd

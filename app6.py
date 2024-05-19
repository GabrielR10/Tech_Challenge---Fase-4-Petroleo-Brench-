#Aula de gráfico de linhas e barras

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Páginas de Dashboard da empresa XPTO.LTDA")

st.header("Gráficos de Barras")

data = pd.DataFrame ({
    'Cidade': ['João Pessoa', 'Rio de Janeiro','Curitiba', 'Belo Horizonte'],
    'Vendas': [1000, 200, 150, 300]
})

st.bar_chart(data, x= 'Cidade', y= 'Vendas')

st.markdown('---')

st.subheader('Gráfico de Linhas')

data2 = pd.DataFrame({
    'Dias': range(1,31),
    'Vendas': np.random.randint(200,1000,size=30) #n° aleatórios em um range de 200 a 1000 em faixas de 30 em 30
})

st.line_chart(data2, x='Dias', y='Vendas')

#Aula de gráfico de dispersão, histograma e Pizza

st.markdown('---')

st.subheader('Gráfico de Dispersão')

data3 = pd.DataFrame({
    'X': np.random.randn(100),
    'Y': np.random.randn(100)
})
sns.scatterplot(x='X', y='Y', data= data3)
st.pyplot()

st.markdown('---')

st.subheader('Gráfico de Histograma')
data4 = np.random.randn(1000)
plt.hist(data4, bins= 20)
st.pyplot()

st.markdown('---')

data = pd.DataFrame({
    'Categoria':['A','B','C','D'],
    'Valores': [25,30,15,20]
})

st.subheader('Gráfico de Pizza')
plt.pie(data['Valores'], labels=data['Categoria'])
st.pyplot()


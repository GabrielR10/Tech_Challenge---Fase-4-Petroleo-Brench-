#Criando a aplicação no Streamlit para o tech challenge sobre a variação do preço do Petróleo Brent

#Importando as bibliotecas
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import seaborn as sb

#Configurando a página
st.set_page_config(page_title='Tech Challenge Fase 4 - Grupo 11 DTAT', page_icon = ':oil_drum',layout='wide')

# Criando o menu de navegação
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",  # required
        options=["Página Inicial", "Série Histórica", "Insights", "Previsão", "Sobre"],  # required
        icons=["house", "graph-down-arrow", "lightbulb","clock","info-circle"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )

#Criando os DataFrames e realizando as alterações

df_previsao = pd.read_csv("Previsao.csv")
df_base_completa = pd.read_csv("FIAP_PRECO_PETROLEO.csv")
df_base_completa2 = pd.read_csv("FIAP_PRECO_PETROLEO - Copia.csv")
df_novo_completo = pd.read_csv("df_novo.csv")
df_sem_pandemia = pd.read_csv("FIAP_PRECO_PETROLEO_SEM_PANDEMIA.csv")
df_2008_resampled_monthly = pd.read_csv("df_2008_resampled_monthly.csv")
df_2014_resampled_monthly = pd.read_csv("df_2014_resampled_monthly.csv")
df_2020_resampled_monthly = pd.read_csv("df_2020_resampled_monthly.csv")
df_2022_resampled_monthly = pd.read_csv("df_2022_resampled_monthly.csv")

#Convertendo a 'Data' para datetime
df_base_completa['Data'] = pd.to_datetime(df_base_completa['Data'], format='%d/%m/%Y')
# df_base_completa.set_index('Data', inplace=True)

#Convertendo o valor do petroleo para float64 além de corrigir o separador decimal
df_base_completa['Último'] = df_base_completa['Último'].str.replace(',', '.')
df_base_completa['Último'] = pd.to_numeric(df_base_completa['Último'], errors='coerce')

# Exibindo o conteúdo baseado na seleção do menu
if selected == "Página Inicial":
    st.title('Análise sobre a variação dos preços do Petróleo Brent 📊🛢️')
    st.write("Vamos apresentar a nossa entrega do Tech Challenge da Fase 4 da Pós-Tech em Data Analytics na FIAP.")
    st.image("C:/Users/Gabri/Desktop/Streamlit/20220316090049_barril-petr-leo.jpg")
    st.caption("*Fonte: Google Imagens*")
    texto1 = """
        O Tech Challenge é o projeto da fase que englobará os conhecimentos obtidos em todas as disciplinas.
        Nesse Fase 4 tivemos disciplinas que abordaram os temas de:
        - **Análise de Negócios**;
        - **Técnicas de Visualização e Storytelling**;
        - **Deploy de Aplicações**; 
        - **Machine Learning**; 
        """
    st.write(texto1)
    st.markdown("---")
    st.subheader("Desafio")
    texto2 = """ 
        Fazemos parte de uma consultoria voltada a Análise de dados e um grande cliente do segmento de petróleo e gás nos solicitou essa análise. \n
        Nosso objetivo é desenvolver um dashboard interativo e que gere insights relevantes para a tomada de decisão:     
        - Apresentando um storytelling que traga insights relevantes sobre a variação do preço do petróleo.
        - Elaboramos a criação de um modelo de Machine Learning que faz a previsão do preço do petróleo diariamente. 
        """
    st.write(texto2)
    st.markdown('---')
    texto3 = """
     ### O que é o Petróleo Brent?

        >*O Petróleo Brent, também conhecido como Brent Blend, é um tipo de petróleo bruto leve e doce extraído do Mar do Norte, entre a Noruega e o Reino Unido.* \n
        >*É um ativo crucial para a economia global, influenciando diversos setores e impactando diretamente o preço dos combustíveis, a inflação e a receita de governos.* \n
        >*Compreender os fatores que afetam o preço do Brent é essencial para empresas, governos e consumidores tomarem decisões conscientes em um mercado em constante mudança.* \n
        >*Ele serve como referência global para precificação de mais de dois terços do petróleo comercializado no mundo, sendo fundamental para a economia global e influenciando diversos setores, desde combustíveis até produtos petroquímicos.*  
        """
    st.write(texto3)
    st.caption("*Fonte: Site Investing*")
    st.markdown('---')
    texto4 = """
     ### Base de Dados

        Vamos usar os dados do site do **IPEA (Instituto de Pesquisa Econômica Aplicada)** para analisar os dados da série histórica do preço do petróleo brent.
        """
    st.write(texto4)
    

elif selected == "Série Histórica":
    st.title("Entendendo a variação do petróleo brent 📉")
    st.write("Apresentando as principais variações durante o período.")
    st.subheader('Fechamento do Preço do Petróleo Brent nos últimos anos')
    fig = px.line(df_base_completa, x='Data', y='Último')
    st.plotly_chart(fig)
    st.write("""Podemos notar uma variação muito grande em todos os anos, o petróleo sofre muitas influências não só na oferta e demanda, mas também na macro economia, sendo muito influenciado por guerras, juros altos, tensões politicas e etc.
             """)
    st.markdown("---")


    # Barra lateral
    with st.sidebar:  
           lista_ano = list(df_novo_completo.ano.unique())[::]
           ano_selecionado = st.selectbox('Selecione o Ano', lista_ano, index=len(lista_ano)-1)
           df_ano_selecionado = df_novo_completo[df_novo_completo.ano == ano_selecionado]
           df_ano_selecionado_sorted = df_ano_selecionado.sort_values(by='data', ascending=True)

    # Funções
    def calcula_ultimo_valor_atual(df):
        valor_atual = df_novo_completo.preco.iloc[-1]
        data_atual = df_novo_completo.data.iloc[-1]
        return valor_atual, data_atual
    
    def calcula_maior_menor_valor(df):
        maior_valor = df_novo_completo.preco.max()
        maior_valor_data = df_novo_completo[df_novo_completo.preco == maior_valor]['data'].max()
        menor_valor = df_novo_completo.preco.min()
        menor_valor_data = df_novo_completo[df_novo_completo.preco == menor_valor]['data'].max()
        return maior_valor, maior_valor_data, menor_valor, menor_valor_data
    
    def calcula_valor_medio(df):
        valor_medio = df_novo_completo.preco.mean().round(2)
        return valor_medio

    # Colunas
    col = st.columns((2.5, 8), gap='medium')

    with col[0]:
        st.markdown('#### Último Fechamento')

        if ano_selecionado >= 2000:
            valor = calcula_ultimo_valor_atual(df_ano_selecionado_sorted)[0]
            data = calcula_ultimo_valor_atual(df_ano_selecionado_sorted)[1]

        st.metric(label=data, value=f'{valor} US$')

        st.markdown('#### Maior Valor Fechado')

        if ano_selecionado >= 2000:
            valor = calcula_maior_menor_valor(df_ano_selecionado_sorted)[0]
            data = calcula_maior_menor_valor(df_ano_selecionado_sorted)[1]

        st.metric(label=data, value=f'{valor} US$')

        st.markdown('#### Menor Valor Fechado')

        if ano_selecionado >= 2000:
            valor = calcula_maior_menor_valor(df_ano_selecionado_sorted)[2]
            data = calcula_maior_menor_valor(df_ano_selecionado_sorted)[3]

        st.metric(label=data, value=f'{valor} US$')

        st.markdown('#### Valor Médio Anual')

        if ano_selecionado >= 2000:
            valor = calcula_valor_medio(df_ano_selecionado_sorted)
            ano = str(ano_selecionado)

        st.metric(label=ano, value=f'{valor} US$')

    with col[1]:
        st.markdown('#### Preço Histórico (US$)')

        if ano_selecionado >= 2000:
            df_ano_selecionado_sorted_grafico = df_ano_selecionado_sorted.rename(columns={'data': 'Data', 'preco':'Preço (US$)'})
            st.line_chart(data=df_ano_selecionado_sorted_grafico, x='Data', y='Preço (US$)', color=None, width=0, height=0, use_container_width=True)
            

elif selected == "Insights":
    st.title("Insights Encontrados 💡")
    st.write("Informações adicionais para entender o cenário apresentando fatores externos")
    # Adiciona as tabs
    tab1, tab2, tab3, tab4 = st.tabs(['Insight 1', 'Insight 2', 'Insight 3', 'Insight 4']) 

    with tab1:
        st.header('Ano de 2008')
        st.write("""
            Em 2008 houve uma crise financeira mundial que atingiu paises de todos os continentes do mundo, foi uma crise gerada pela alta dos juros que ocasionou
            muita oferta por crédito e pouca procura, resultando no colápso de várias instiuições financeiras e imobiliárias. 
                 \n
            Até hoje essa crise financeira é considerada uma das piores da história e podemos notar a variação drástica do preço do barril de petróleo, saindo de aproximadamente
            90 dólares, passando para 134 com uma alta de mais 40% e depois seguido por uma queda para 40 dólares, uma incrivel queda abrupta de quase 75%
                 """)

        # Criar o gráfico de linhas com Plotly Express
        fig = px.line(df_2008_resampled_monthly, x='Data', y='Último', title='Variação do preço do petróleo Brent em 2008')

        # Adicionar rótulos aos pontos
        fig.update_traces(
            mode='markers+lines+text', 
            text=df_2008_resampled_monthly['Último'].round(2).astype(str),  # Certifique-se de que o texto seja string
            textposition='top center'
        )

        # Editar os nomes dos eixos e adicionar linhas de grade verticais
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Média do último fechamento',
            title_x=0.5,  # Centraliza o título
            xaxis=dict(showgrid=True),  # Adiciona linhas de grade verticais
            yaxis=dict(showgrid=True)   # Adiciona linhas de grade horizontais (já ativadas por padrão)
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

    with tab2:
        st.header('Ano de 2014')
        st.write("""
            Em 2014, diferente dos outros insights que trouxemos, não houve uma grande crise global que gerassem a variação no preço do petróleo, aqui tivemos um aumento da
            produção norte americana que atingiu a sua máxima em 30 anos, e esse aumento da oferta não foi seguido pela demanda, dado que os paises europeus e asiáticos não tiveram
            o aumento esperado no consumo. Como tinha muito petróleo sendo produzido e pouco sendo consumido, os preços acabaram caindo quase 50% em menos de 6 meses.
                 """)
        # Criar o gráfico de linhas com Plotly Express
        fig = px.line(df_2014_resampled_monthly, x='Data', y='Último', title='Variação do preço do petróleo Brent em 2014')

        # Adicionar rótulos aos pontos
        fig.update_traces(
            mode='markers+lines+text', 
            text=df_2014_resampled_monthly['Último'].round(2).astype(str),  # Certifique-se de que o texto seja string
            textposition='top center'
        )

        # Editar os nomes dos eixos e adicionar linhas de grade verticais
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Média do último fechamento',
            title_x=0.5,  # Centraliza o título
            xaxis=dict(showgrid=True),  # Adiciona linhas de grade verticais
            yaxis=dict(showgrid=True)   # Adiciona linhas de grade horizontais (já ativadas por padrão)
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

    with tab3:
        st.header('Ano de 2020')
        st.write( """
            Em 2020 tivemos uma das piores pandemia da história, a pandemia do Corona Virus. A incerteza no cenário mundial afetou diretamente o preço de praticamente todos os ativos
            do mundo e com o petróleo não foi diferente, chegando a bater 18.47 dolares em maio, um dos valores mais baixos da série histórica.
                 """)
            # Criar o gráfico de linhas com Plotly Express
        fig = px.line(df_2020_resampled_monthly, x='Data', y='Último', title='Variação do preço do petróleo Brent em 2020')

        # Adicionar rótulos aos pontos
        fig.update_traces(
            mode='markers+lines+text', 
            text=df_2020_resampled_monthly['Último'].round(2).astype(str),  # Certifique-se de que o texto seja string
            textposition='top center'
        )

        # Editar os nomes dos eixos e adicionar linhas de grade verticais
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Média do último fechamento',
            title_x=0.5,  # Centraliza o título
            xaxis=dict(showgrid=True),  # Adiciona linhas de grade verticais
            yaxis=dict(showgrid=True)   # Adiciona linhas de grade horizontais (já ativadas por padrão)
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

    with tab4:
        st.header('Ano de 2022')
        st.write("""
            Em 2022 tivemos uma grande alta no preço do petróleo por conta da guerra entre Rússia e Ucrânia, essa alta foi causada pelo fato da Rússia ser o segundo maior produtor
            de petróleo do mundo e por conta da invasão a Ucrânia eles sofreram fortes sansoes de vários países contrários. \n
            Essas sansões dificultavam a exportação do petróleo Russo, gerando assim uma incerteza no mercado e a grande alta, chegando a atingir valores acima de 122 doláres, patamar não alcançado desde 2014.
                 """)
              # Criar o gráfico de linhas com Plotly Express
        fig = px.line(df_2022_resampled_monthly, x='Data', y='Último', title='Variação do preço do petróleo Brent em 2022')

        # Adicionar rótulos aos pontos
        fig.update_traces(
            mode='markers+lines+text', 
            text=df_2022_resampled_monthly['Último'].round(2).astype(str),  # Certifique-se de que o texto seja string
            textposition='top center'
        )

        # Editar os nomes dos eixos e adicionar linhas de grade verticais
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Média do último fechamento',
            title_x=0.5,  # Centraliza o título
            xaxis=dict(showgrid=True),  # Adiciona linhas de grade verticais
            yaxis=dict(showgrid=True)   # Adiciona linhas de grade horizontais (já ativadas por padrão)
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
        
elif selected == "Previsão":
    st.title("Previsões para os próximos dias 🔮")
    st.write("Aqui mostramos as previões de fechamento do barril de petróleo nos próximos dias.")

    # Colunas
    col = st.columns((3, 7), gap='medium')

    with col[0]:
        st.markdown('#### Preços de petróleo previstos')
        df = pd.read_csv("dataset-previsao-editado4.csv")
        st.dataframe(df)

    with col[1]:
        st.markdown('#### Gráfico de Tendência dos valores Previstos')

         # Criar o gráfico de linhas com Plotly Express
        fig = px.line(df, x='Data', y='preco', title='Variação do preço do petróleo previsto')

        # Adicionar rótulos aos pontos
        fig.update_traces(
            mode='markers+lines+text', 
            text=df_2020_resampled_monthly['Último'].round(2).astype(str),  # Certifique-se de que o texto seja string
            textposition='top center'
        )

        # Editar os nomes dos eixos e adicionar linhas de grade verticais
        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Média do último fechamento',
            title_x=0.5,  # Centraliza o título
            xaxis=dict(showgrid=True),  # Adiciona linhas de grade verticais
            yaxis=dict(showgrid=True)   # Adiciona linhas de grade horizontais (já ativadas por padrão)
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)


elif selected == "Sobre":
    st.title("Sobre 📝")
    texto_sobre = """
        Olá, somos **Gabriel Reis** e **Gustavo Andrade** \n
        Fazemos parte  de uma equipe de Especialistas em Análise de Dados da consultoria **DATA-Insights (Empresa Fictícia)** \n
        Fizemos essa análise para um grande cliente do segmento de petróleo e gás que tem a necessidade de entender mais sobre essa área. \n
        Nosso maior desafio foi atender e essa demanda realizando uma análise com grandes conjuntos de dados obtidos pelo site do IPEA (Instituto de Pesquisa Econômica Aplicada) gerando insights relevantes e auxiliando para a tomada de decisão do nosso cliente.
        \n
        \n
         
         
        ### Contato 📫📢
        Para mais informações, visitem nosso perfil no **LinkedIn**: \n
        """
    st.write(texto_sobre)

# Link para o perfil do LinkedIn
    st.markdown("""
            <div style="display: flex; justify-content: space-around;">
            <div style="text-align: center;">
                <a href="https://www.linkedin.com/in/gabrielreisdourado/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="100">
                <p>Gabriel Reis</p>
                </a>
            </div>
            <div style="text-align: center;">
                <a href="https://www.linkedin.com/in/gustavopandrade/" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="100">
                <p>Gustavo Andrade</p>
                </a>
            </div>
            </div>
            """, unsafe_allow_html=True) 


#referencias:

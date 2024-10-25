import streamlit as st
import plotly.express as px
from data_processing import carregar_dados, resumir_dados

# Carregar e processar os dados
df = carregar_dados()
vendas_por_regiao, vendas_por_produto, vendas_por_periodo = resumir_dados(df)

# Configurar a página do Streamlit
st.set_page_config(page_title="Painel de Vendas", layout="wide")

# Título do painel
st.title("Painel Interativo de Vendas - AdventureWorks")

# Filtros
produto_selecionado = st.sidebar.selectbox("Selecione o Produto", df['Produto'].unique())
data_inicial = st.sidebar.date_input("Data Inicial", min_value=df['OrderDate'].min())
data_final = st.sidebar.date_input("Data Final", max_value=df['OrderDate'].max())

# Filtrar os dados
df_filtrado = df[(df['Produto'] == produto_selecionado) & 
                 (df['OrderDate'] >= data_inicial) & 
                 (df['OrderDate'] <= data_final)]

# Adicionar KPI
total_vendas = df_filtrado['TotalDue'].sum()
st.metric(label="Total de Vendas no Período", value=f"R$ {total_vendas:,.2f}")

# Gráfico de Barras - Vendas por Produto
fig_produto = px.bar(vendas_por_produto, x='Produto', y='TotalDue', title='Vendas por Produto')
st.plotly_chart(fig_produto)

# Gráfico de Linhas - Vendas ao Longo do Tempo
fig_tempo = px.line(vendas_por_periodo, x='Mes', y='TotalDue', title='Vendas ao Longo do Tempo')
st.plotly_chart(fig_tempo)

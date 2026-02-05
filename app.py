import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Data Insights Dashboard", layout="wide")

# --- 1. ETAPA DE EXTRAÇÃO (EXTRACT) ---
@st.cache_data
def get_raw_data():
    # Simulando um dataset de vendas global
    np.random.seed(42)
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(200)]
    data = {
        'Data': np.random.choice(dates, 500),
        'Região': np.random.choice(['América do Sul', 'Europa', 'Ásia', 'América do Norte'], 500),
        'Produto': np.random.choice(['Notebook', 'Tablet', 'Smartphone', 'Monitor'], 500),
        'Preço_Unitario': np.random.uniform(100, 1500, 500),
        'Quantidade': np.random.randint(1, 10, 500),
        'Custo_Envio': np.random.uniform(10, 50, 500)
    }
    return pd.DataFrame(data)

# --- 2. ETAPA DE TRANSFORMAÇÃO (TRANSFORM) ---
def transform_data(df):
    # Criando métricas calculadas
    df['Faturamento_Bruto'] = df['Preço_Unitario'] * df['Quantidade']
    df['Lucro_Liquido'] = df['Faturamento_Bruto'] - (df['Custo_Envio'] * df['Quantidade'])
    df['Mes'] = df['Data'].dt.strftime('%Y-%m')
    return df

# Executando o "Pipeline"
raw_df = get_raw_data()
df = transform_data(raw_df)

# --- 3. INTERFACE DO DASHBOARD (LOAD/VISUALIZE) ---
st.title("📊 Dashboard de Performance de Vendas")
st.markdown("Este dashboard demonstra um pipeline de **ETL** completo para análise de e-commerce.")

# Sidebar - Filtros
st.sidebar.header("Filtros de Análise")
regiao_selecionada = st.sidebar.multiselect("Selecione a Região:", options=df['Região'].unique(), default=df['Região'].unique())
df_filtered = df[df['Região'].isin(regiao_selecionada)]

# KPIs Principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Faturamento Total", f"R$ {df_filtered['Faturamento_Bruto'].sum():,.2f}")
with col2:
    st.metric("Lucro Líquido", f"R$ {df_filtered['Lucro_Liquido'].sum():,.2f}", delta="12%")
with col3:
    st.metric("Total de Pedidos", len(df_filtered))

st.divider()

# Gráficos Plotly
c1, c2 = st.columns(2)

with c1:
    st.subheader("Faturamento por Categoria")
    fig_bar = px.bar(df_filtered, x='Produto', y='Faturamento_Bruto', color='Região', barmode='group', template='plotly_white')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Tendência Mensal de Lucro")
    df_trend = df_filtered.groupby('Mes')['Lucro_Liquido'].sum().reset_index()
    fig_line = px.line(df_trend, x='Mes', y='Lucro_Liquido', markers=True, template='plotly_white')
    st.plotly_chart(fig_line, use_container_width=True)

# Visualização da Tabela de Dados Transformados
with st.expander("🔍 Visualizar Dados Processados (Pós-ETL)"):
    st.write(df_filtered.head(50))

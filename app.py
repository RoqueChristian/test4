import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
import plotly.express as px
from meu_app import * # Importe as funções do meu_app.py

st.set_page_config(page_title="Go MED SAÚDE", page_icon=":bar_chart:", layout="wide")

# Função para exibir o cabeçalho com imagem
def exibir_cabecalho(img_path, titulo):
    if os.path.exists(img_path):
        col1, col2 = st.columns([1, 12])
        with col1:
            st.image(img_path, width=80)
        with col2:
            st.title(titulo)
    else:
        st.title(titulo)

exibir_cabecalho("go_med_saude.jpeg", "Sistema de Análise")

st.write("")
st.write("")

# Função para obter os caminhos dos arquivos
def carregar_arquivos(tipo: str):
    caminhos = {
        "vendas": "df_vendas.csv",
    }
    return caminhos.get(tipo, None)

# Barra lateral de navegação
with st.sidebar:
    menu_selecionado = option_menu(
        menu_title="Navegação",
        options=["Análise de Vendas"],
        icons=["bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "red"},
        },
    )

if menu_selecionado == "Análise de Vendas":
    caminho_arquivo = carregar_arquivos("vendas")

    if caminho_arquivo and os.path.exists(caminho_arquivo):
        try:
            df = pd.read_csv(caminho_arquivo)
            if df.empty:
                st.warning("O arquivo CSV está vazio.")
            else:
                renderizar_pagina_vendas(df)  # Chame a função renderizar_pagina_vendas()
        except pd.errors.ParserError:
            st.error("Erro ao analisar o arquivo CSV. Verifique o formato.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
    else:
        st.error("Arquivo não encontrado!")
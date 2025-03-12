import streamlit as st
import pandas as pd
import plotly.express as px


# Funções de Formatação
def formatar_moeda(valor, simbolo_moeda="R$"):
    """Formata um valor numérico como moeda."""
    return f"{simbolo_moeda} {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Funções de Agregação e Cálculo
def calcular_metricas(df):
    """Calcula e retorna métricas de vendas."""
    total_nf = len(df['NF'].unique())
    total_qtd_produto = df['Qtd_Produto'].sum()
    valor_total_item = df['Valor_Total_Item'].sum()
    total_custo_compra = df['Total_Custo_Compra'].sum()
    total_lucro_venda = df['Total_Lucro_Venda_Item'].sum()
    return total_nf, total_qtd_produto, valor_total_item, total_custo_compra, total_lucro_venda

def agrupar_e_somar(df, coluna_agrupamento):
    """Agrupa e soma vendas por uma coluna específica."""
    return df.groupby(coluna_agrupamento).agg(
        {'Valor_Total_Item': 'sum', 'Total_Custo_Compra': 'sum', 'Total_Lucro_Venda_Item': 'sum'}
    ).reset_index()

def produtos_mais_vendidos(df, top_n=10, ordenar_por='Valor_Total_Item'):
    """Retorna os top N produtos mais vendidos."""
    df_agrupado = df.groupby('Descricao_produto')[ordenar_por].sum().reset_index()
    df_ordenado = df_agrupado.sort_values(by=ordenar_por, ascending=False)
    return df_ordenado.head(top_n)

# Funções de Filtro
def aplicar_filtros(df, vendedor='Todos', mes='Todos', ano='Todos', situacao='Todos'):
    """Aplica filtros ao DataFrame."""
    df_filtrado = df.copy()
    if vendedor != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Vendedor'] == vendedor]
    if mes != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Mes'] == mes]
    if ano != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Ano'] == ano]
    if situacao != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['situacao'] == situacao]
    return df_filtrado

# Funções de Gráficos
def criar_grafico_barras(df, x, y, title, labels):
    """Cria e retorna um gráfico de barras com layout aprimorado."""
    fig = px.bar(df, x=x, y=y, title=title, labels=labels, 
                 color=y, text_auto=True, template="plotly_white", 
                 hover_data={x: False, y: ":,.2f"})

    fig.update_traces(marker=dict(line=dict(color='black', width=1)), 
                      hoverlabel=dict(bgcolor="white", font_size=14, 
                                      font_family="Arial, sans-serif"))

    fig.update_layout(yaxis_title=labels.get(y, y), 
                      xaxis_title=labels.get(x, x), 
                      showlegend=False, height=400)

    return fig

# Renderiza a página de vendas com filtros, métricas e gráficos.
def renderizar_pagina_vendas(df):
    vendedores = df['Vendedor'].unique().tolist()
    mes = df['Mes'].unique().tolist()
    ano = df['Ano'].unique().tolist()
    situacao = df['situacao'].unique().tolist()

    with st.expander("Filtros"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            vendedor_selecionado = st.selectbox("Selecionar Vendedor", options=['Todos'] + vendedores)
        with col2:
            mes_selecionado = st.selectbox("Selecionar Mes", options=['Todos'] + mes)
        with col3:
            ano_selecionado = st.selectbox("Selecionar Ano", options=['Todos'] + ano)
        with col4:
            situacao_selecionada = st.selectbox('Selecione a Situação', options=['Todos'] + situacao)

    df_filtrado = aplicar_filtros(df, vendedor_selecionado, mes_selecionado, ano_selecionado, situacao_selecionada)

    # Métricas
    total_nf, total_qtd_produto, valor_total_item, total_custo_compra, total_lucro_venda = calcular_metricas(df_filtrado)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total de Notas", f"{total_nf}")
    col2.metric("Total de Produtos", f"{total_qtd_produto}")
    col3.metric("Faturamento Total", formatar_moeda(valor_total_item))
    col4.metric("Custo Total", formatar_moeda(total_custo_compra))
    col5.metric("Lucro Total", formatar_moeda(total_lucro_venda))

    # Gráficos
    st.subheader("Vendas por Linha de Produto")
    fig_linha = criar_grafico_barras(agrupar_e_somar(df_filtrado, 'Linha'), 'Linha', 'Valor_Total_Item',
                                    'Vendas por Linha de Produto', {'Valor_Total_Item': 'Valor Total de Venda'})
    st.plotly_chart(fig_linha)

    st.subheader("Vendas por Vendedor")
    fig_vendedor = criar_grafico_barras(agrupar_e_somar(df_filtrado, 'Vendedor'), 'Vendedor', 'Valor_Total_Item',
                                        'Vendas por Vendedor', {'Valor_Total_Item': 'Valor Total de Venda'})
    st.plotly_chart(fig_vendedor)

    st.subheader("Top 10 Produtos Mais Vendidos")
    fig_produtos = criar_grafico_barras(produtos_mais_vendidos(df_filtrado), 'Descricao_produto', 'Valor_Total_Item',
                                        'Top 10 Produtos Mais Vendidos',
                                        {'Descricao_produto': 'Produto', 'Valor_Total_Item': 'Valor Total de Venda'})
    st.plotly_chart(fig_produtos)

    
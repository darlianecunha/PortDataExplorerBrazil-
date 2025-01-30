import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo consolidado
arquivo_path = "movimentacaoportuaria2020_2023.xlsx"

# Carregar cada ano e renomear as colunas para garantir consistência
dados_2020 = pd.read_excel(arquivo_path, sheet_name='2020', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2021 = pd.read_excel(arquivo_path, sheet_name='2021', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2022 = pd.read_excel(arquivo_path, sheet_name='2022', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})
dados_2023 = pd.read_excel(arquivo_path, sheet_name='2023', engine='openpyxl').rename(columns={'Carga Movimentada': 'carga', 'Porto': 'porto'})

# Adicionar uma coluna 'Ano' em cada conjunto de dados
dados_2020['Ano'] = "2020"
dados_2021['Ano'] = "2021"
dados_2022['Ano'] = "2022"
dados_2023['Ano'] = "2023"

# Combinar os dados em um único DataFrame
dados = pd.concat([dados_2020, dados_2021, dados_2022, dados_2023])

# Título em azul marinho
st.markdown("<h1 style='color: #002060;'>Movimentação Portuária dos Portos Brasileiros (2020-2023)</h1>", unsafe_allow_html=True)

# Interface de seleção de porto
porto_escolhido = st.selectbox("Selecione o Porto ou Terminal", sorted(dados['porto'].unique()))

# Filtrar dados pelo porto selecionado
dados_porto = dados[dados['porto'] == porto_escolhido]

if not dados_porto.empty:
    st.markdown(f"<h2 style='color: #002060;'>Movimentação para o Porto: {porto_escolhido}</h2>", unsafe_allow_html=True)

    # Agrupar por 'Ano' e somar a carga do porto selecionado
    dados_anos = dados_porto.groupby('Ano')['carga'].sum().reset_index()
    
    # Agrupar por 'Ano' para calcular a movimentação total
    dados_totais = dados.groupby('Ano')['carga'].sum().reset_index()
    
    # Calcular o percentual de participação do porto na movimentação total
    dados_anos = dados_anos.merge(dados_totais, on='Ano', suffixes=('_porto', '_total'))
    dados_anos['percentual'] = (dados_anos['carga_porto'] / dados_anos['carga_total']) * 100

    # **Garantir que os valores numéricos estejam corretos**
    dados_anos['carga_porto'] = dados_anos['carga_porto'].astype(float)
    dados_anos['carga_total'] = dados_anos['carga_total'].astype(float)

    # Formatar os números para o padrão brasileiro
    dados_anos['carga_porto_movimentada'] = dados_anos['carga_porto'].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    dados_anos['carga_total_movimentada'] = dados_anos['carga_total'].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    dados_anos['percentual'] = dados_anos['percentual'].map(lambda x: f"{x:.2f}".replace(".", ",")) + "%"

    # Exibir DataFrame formatado
    st.dataframe(dados_anos[['Ano', 'carga_porto_movimentada', 'carga_total_movimentada', 'percentual']], use_container_width=True)

    # **Criar gráfico com Matplotlib mostrando a carga movimentada pelo porto selecionado**
    st.markdown(f"<h2 style='color: #002060;'>Resumo da Movimentação do Porto {porto_escolhido} por Ano</h2>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(dados_anos['Ano'], dados_anos['carga_porto'], color='#002060')
    ax.set_ylabel("Carga Movimentada")
    ax.set_xlabel("Ano")
    ax.set_title(f"Movimentação do Porto {porto_escolhido} (2020-2023)")
    
    # **Corrigir o eixo Y para melhor visualização**
    ax.set_ylim(0, max(dados_anos['carga_porto']) * 1.1)  # Definir um espaço extra no topo

    # **Formatar eixo Y no padrão brasileiro**
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")))

    st.pyplot(fig)

else:
    st.write("Dados não disponíveis para o porto selecionado.")

# Adicionar a fonte e o crédito ao final da aplicação
st.write("Fonte: Estatístico Aquaviário ANTAQ. Dados obtidos em nov/24.")
st.markdown("<p><strong>Ferramenta desenvolvida por Darliane Cunha.</strong></p>", unsafe_allow_html=True)

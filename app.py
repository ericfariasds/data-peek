#-----IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS-----
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configura estilo padrão para todos os gráficos
plt.style.use('seaborn-v0_8-darkgrid')

plt.rcParams.update({
    'font.size': 12,
    'font.family': 'sans-serif',
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.labelweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 100,
    'savefig.dpi': 100,
    'figure.autolayout': True
})

#-----CABEÇALHO DA APLICAÇÃO-----
st.title("DataPeek - Seu CSV Explicado")
st.write("Faça upload do seu arquivo CSV para obter insights e visualizações rápidas!   ")


#-----UPLOAD DO ARQUIVO CSV-----
arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")

#-----PROCESSAMENTO PRINCIPAL -----
if arquivo is not None:

#-----LEITURA DO CSV COM TRATAMENTO DE ERROS-----
    try:
        df = pd.read_csv(arquivo) #Tenta ler o CSV normalmente
    except:
        #Se ocorrer um erro, tenta ler o CSV ignorando as linhas com formatação irregular
        st.warning("CSV com formatação irregular - algumas linhas foram ignoradas")
        df = pd.read_csv(arquivo,
                         on_bad_lines='skip',#Pula as linhas com formatação irregular
                         encoding='utf-8')#Força a leitura com codificação UTF-8
        
    st.success("Arquivo carregado com sucesso!")

#-----PRÉ-VISUALIZAÇÃO E ANÁLISE DOS DADOS-----
    st.subheader("Visão geral do DataFrame")
    st.dataframe(df.head())#Mostra as 5 primeiras linhas em tabela interativa

#-----MÉTRICAS COM NÚMEROS-----
    col1, col2 = st.columns(2)
    col1.metric("Número de Linhas", df.shape[0])
    col2.metric("Número de Colunas", df.shape[1])

#-----LISTA DE COLUNAS-----
    st.subheader("Colunas do arquivo")
    st.write(list(df.columns))

#-----ANÁLISE DE VALORES NULOS-----
    st.subheader("Valores nulos por coluna")
    nulos = df.isnull().sum()

    tabela_nulos = pd.DataFrame({
        'Colunas': nulos.index,
        'Qt. de valores Nulos': nulos.values
    })

    st.write(tabela_nulos)

#-----ESTATÍSTICAS DESCRITIVAS-----
    st.subheader("Estatísticas das colunas numéricas")

    #calcula as estatísticas
    estatisticas = df.describe()

    #Dicionário de tradução dos índices
    traducao = {
        'count': 'Contagem',
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Mínimo',
        '25%': '1º Quartil (25%)',
        '50%': 'Mediana (50%)',
        '75%': '3º Quartil (75%)',
        'max': 'Máximo'
    }

    #Renomeia os índices
    estatisticas.rename(index=traducao, inplace=True)
    
    #Exiber a tabela
    st.dataframe(estatisticas.style.format("{:.2f}"))

#-----GERAÇÃO DE GRÁFICOS-----
    st.subheader("Gráficos")

    # Filtra apenas colunas numéricas (inteiros ou decimais)
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()


    if len(colunas_numericas) > 0: # Se existe pelo menos uma coluna numérica

        # Dropdown pro usuário escolher qual coluna analisar
        coluna_escolhida = st.selectbox("Escolha uma coluna numérica: ", colunas_numericas)

        # Cria o histograma
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(df[coluna_escolhida].dropna(), 
                bins=30,
                color='#2E86AB',
                edgecolor='white',
                alpha=0.7,
                linewidth=0.5)
        
        # Calcular a média da coluna escolhida
        media = df[coluna_escolhida].mean()
        ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')
        
        # Calcular a mediana da coluna escolhida
        mediana = df[coluna_escolhida].median()
        ax.axvline(mediana, color='green', linestyle=':', linewidth=2, label=f'Mediana: {mediana:.2f}')
        
        # Título e rótulos
        ax.set_title(f"Distribuição de {coluna_escolhida}", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(coluna_escolhida, fontsize=12)
        ax.set_ylabel("Frequência", fontsize=12)
        
        # Grade de fundo
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

        # Legenda
        ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
        
        # Remover bordas superior e direita
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Ajustar layout e exibe o gráfico
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Nenhuma coluna numérica encontrada para gerar gráfico.")

#-----COLUNAS CATEGÓRICAS-----
    st.subheader("Análise de colunas categóricas")

    # Pega apenas colunas do tipo texto (object)
    colunas_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    
    # Só executa se existir pelo menos uma coluna de texto
    if len(colunas_categoricas) > 0:
        coluna_cat = st.selectbox("Escolha uma coluna categórica:", colunas_categoricas)
        
        contagem = df[coluna_cat].value_counts().head(10)
        
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.barh(contagem.index, contagem.values, color='#A23B72')
        
        # Título e rótulos
        ax2.set_title(f"Top 10 valores em {coluna_cat}")
        ax2.set_xlabel("Quantidade")
        ax2.set_ylabel(coluna_cat)
    
        st.pyplot(fig2)

#-----EXPORTAÇÃO DE DADOS LIMPOS-----
    st.subheader("Exportar dados limpos")

    # Botão que só processa quando clicado
    if st.button("Remover linhas com valores nulos"):
        df_limpo = df.dropna()
        csv = df_limpo.to_csv(index=False).encode('utf-8')

        # Botão de download (só aparece depois do clique acima)
        st.download_button(
            label="Download do CSV limpo",
            data=csv,
            file_name='dados_limpos.csv',
            mime='text/csv',
        )

else:
    #Estado inicial enquanto nenhum arquivo é carregado
    st.info("Aguardando o upload do arquivo CSV...")
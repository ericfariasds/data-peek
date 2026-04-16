import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("DataPeek - Seu CSV Explicado")
st.write("Faça upload do seu arquivo CSV para obter insights e visualizações rápidas!   ")

arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)
    except:
        st.warning("CSV com formatação irregular - algumas linhas foram ignoradas")
        df = pd.read_csv(arquivo,
                         on_bad_lines='skip',
                         encoding='utf-8')
        
    st.success("Arquivo carregado com sucesso!")

    st.subheader("Colunas do arquivo")
    st.write(list(df.columns))

    st.subheader("Valores nulos por coluna")
    st.write(df.isnull().sum())

    st.subheader("Estatísticas das colunas numéricas")
    st.write(df.describe())

    st.subheader("Gráficos")
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()


    if len(colunas_numericas) > 0:
        coluna_escolhida = st.selectbox("Escolha uma coluna numérica: ", colunas_numericas)

        fig, ax = plt.subplots()
        ax.hist(df[coluna_escolhida].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f"Distribuição de {coluna_escolhida}")
        st.pyplot(fig)
    else:
        st.warning("Nenhuma coluna numérica encontrada para gerar gráfico.")

else:
    st.info("Aguardando o upload do arquivo CSV...")



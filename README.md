## DataPeek - Analisador de CSV

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0-green.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-orange.svg)](https://matplotlib.org/)

**DataPeek** é uma aplicação web para análise rápida de arquivos CSV. Faça upload, visualize estatísticas, identifique valores nulos e gere gráficos automaticamente.

---

## Funcionalidades

- Upload de CSV com detecção automática de separador (`,` ou `;`)
- Pré-visualização dos dados (5 primeiras linhas)
- Métricas: total de linhas e colunas
- Identificação de valores nulos por coluna
- Estatísticas descritivas traduzidas (média, mediana, quartis)
- Gráficos:
  - Histograma com linhas de média e mediana
  - Gráfico de barras para colunas categóricas (Top 10)
- Exportação de dados limpos (sem valores nulos)

---

## Como executar o projeto

**1. Clone o repositório
```bash
git clone https://github.com/ericfariasds/DataPeek.git
cd DataPeek

```

**2. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate

```

**3. Instale as dependências
```bash
pip install -r requirements.txt


```
**4. Execute
```bash
streamlit run app.py

```

---

## Tecnologias

- Streamlit - Interface web
- Pandas - Manipulação de dados
- Matplotlib - Visualizações

---

## Autor

Eric Farias

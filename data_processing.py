import pandas as pd

def carregar_dados(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, delimiter=',')
    return df

def resumir_dados(df):
    resumo = df.describe()
    return resumo

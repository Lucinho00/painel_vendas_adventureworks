import pyodbc
import pandas as pd

# Configurar a conexão com o banco de dados
def carregar_dados():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=seu_servidor;'
        'DATABASE=AdventureWorks;'
        'UID=seu_usuario;'
        'PWD=sua_senha'
    )

    query = """
    SELECT 
        soh.OrderDate, 
        soh.TotalDue, 
        addr.StateProvinceID, 
        prod.Name AS Produto
    FROM 
        Sales.SalesOrderHeader AS soh
    JOIN 
        Sales.SalesOrderDetail AS sod ON soh.SalesOrderID = sod.SalesOrderID
    JOIN 
        Person.Address AS addr ON soh.ShipToAddressID = addr.AddressID
    JOIN 
        Production.Product AS prod ON sod.ProductID = prod.ProductID
    """

    # Carregar os dados em um DataFrame
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Processar os dados
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Ano'] = df['OrderDate'].dt.year
    df['Mes'] = df['OrderDate'].dt.month

    return df

def resumir_dados(df):
    vendas_por_regiao = df.groupby('StateProvinceID')['TotalDue'].sum().reset_index()
    vendas_por_produto = df.groupby('Produto')['TotalDue'].sum().reset_index()
    vendas_por_periodo = df.groupby(['Ano', 'Mes'])['TotalDue'].sum().reset_index()
    
    return vendas_por_regiao, vendas_por_produto, vendas_por_periodo

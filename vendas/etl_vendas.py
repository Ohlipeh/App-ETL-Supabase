"""
Importações:
Pandas → Biblioteca Python para análise e manipulação de dados em tabelas (DataFrames).

SQLAlchemy → Ferramenta Python para interagir com bancos de dados usando ORM (mapear classes/objetos para tabelas SQL).
"""

import pandas as pd
from sqlalchemy import create_engine


# Classe responsável por extrair dados de arquivos CSV
# e preparar para análise.
class ExtratorDados:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    # Lê um arquivo CSV e retorna um DataFrame Pandas
    def ler_arquivo(self):
        tabela = pd.read_csv(self.caminho_arquivo)
        return tabela


# Classe responsável por precessar os dados.
class ProcessadorRegras:
    def __init__(self, dados_brutos):
        self.dados_brutos = dados_brutos

    # Usei dropna para remover valores ausentes.
    def limpar_nulos(self):
        dados_limpos = self.dados_brutos.dropna()
        return dados_limpos


# Classe responsável por exportar os arquivos, subir o arquivo pra nuvem.
class ExportadorDados:
    def __init__(self, tabela_final, host, port, database, user, senha):
        self.tabela_final = tabela_final
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.senha = senha

    # Salva o arquivo na nuvem(supabase)
    def salvar_relatorio(self):

        url_conexao = (
            f"postgresql://{self.user}:{self.senha}"
            f"@{self.host}:{self.port}/{self.database}"
        )

        motor = create_engine(url_conexao)

        self.tabela_final.to_sql(
            "vendas_consolidadas", con=motor, if_exists="replace", index=False
        )

        return "Dados enviados para o Supabase com sucesso!"

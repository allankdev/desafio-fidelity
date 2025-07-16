import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do arquivo .env

# Configuração do Banco de Dados PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "db_teste")
DB_USER = os.getenv("DB_USER", "usr_teste")
DB_PASSWORD = os.getenv("DB_PASSWORD", "teste")
DB_PORT = os.getenv("DB_PORT", "5432")

# Configuração do Selenium
EXECUTABLE_PATH = os.getenv("EXECUTABLE_PATH", "C:/Users/teste/OneDrive/Documentos/msedgedriver.exe")

# Configuração da Pesquisa
PESQUISA_LIMIT = 210
URL_TJSP = "https://esaj.tjsp.jus.br/cpopg/open.do"

# Constantes de Resultado
RESULT_MAP = {
    'NADA_CONSTA': 'Não existem informações disponíveis para os parâmetros informados.',
    'CONSTA_01': 'Processos encontrados',
    'CONSTA_02': 'Audiências'
}

RESULT_CODE = {
    'SUCESSO_NADA_CONSTA': 1,
    'SUCESSO_CRIMINAL': 2,
    'SUCESSO_CIVEL': 5,
    'ERRO_INDEFINIDO': 7
}

#banco.py



import psycopg2
from psycopg2 import Error

from config import POSTGRES_CONFIG


def conectar():
    
    try:
        return psycopg2.connect(**POSTGRES_CONFIG)
    except (Error, UnicodeDecodeError) as erro:
       
        raise RuntimeError(
            f"Nao foi possivel conectar ao PostgreSQL em "
            f"{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']} / database "
            f"'{POSTGRES_CONFIG['dbname']}'. Verifique o .env e se voce ja rodou "
            f"o script '0_criar_banco.sql'. Detalhe: {erro}"
        )


def executar(conexao, sql):
    
    cursor = conexao.cursor()
    cursor.execute(sql)
    conexao.commit()
    cursor.close()


def inserir_em_lote(conexao, sql_insert, linhas):
   
    if not linhas:
        return
    cursor = conexao.cursor()
    cursor.executemany(sql_insert, linhas)
    conexao.commit()
    cursor.close()
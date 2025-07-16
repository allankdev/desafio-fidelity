import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from src import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fetch_pending_searches(search_filter, limit):
    """Busca no banco de dados por pesquisas pendentes com base em um filtro."""
    conn = get_db_connection()
    if not conn:
        return []

    # O filtro determina qual campo de documento usar (CPF, RG, Nome)
    # 0=CPF, 1=RG, 2=Nome, 3=RG
    conditions = {
        0: 'p.cpf IS NOT NULL AND p.cpf <> \'\'',
        1: 'p.rg IS NOT NULL AND p.rg <> \'\'',
        2: 'p.nome IS NOT NULL AND p.nome <> \'\'',
        3: 'p.rg IS NOT NULL AND p.rg <> \'\''
    }
    filter_condition = conditions.get(search_filter, '1=0') # '1=0' para filtro inválido não retornar nada

    # Query refatorada para maior clareza e usando placeholders (%) para segurança
    sql = """
        SELECT
            p.cod_pesquisa,
            p.cpf,
            COALESCE(p.rg_corrigido, p.rg) AS rg,
            COALESCE(p.nome_corrigido, p.nome) AS nome
        FROM
            pesquisa p
        JOIN estado e ON e.cod_uf = p.cod_uf
        LEFT JOIN pesquisa_spv ps ON p.cod_pesquisa = ps.cod_pesquisa
                                  AND ps.cod_spv = 1
                                  AND ps.filtro = %(filter)s
        WHERE
            p.data_conclusao IS NULL
            AND ps.cod_pesquisa_spv IS NULL -- Mais eficiente checar se o resultado já existe
            AND p.tipo = 0
            AND (e.uf = 'SP' OR p.cod_uf_nascimento = 26 OR p.cod_uf_rg = 26)
            AND {dynamic_condition}
        GROUP BY
            p.cod_pesquisa
        ORDER BY
            nome ASC
        LIMIT %(limit)s;
    """.format(dynamic_condition=filter_condition)

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, {'filter': str(search_filter), 'limit': limit})
            results = cursor.fetchall()
            return results
    except Exception as e:
        logging.error(f"Erro ao buscar pesquisas: {e}")
        return []
    finally:
        if conn:
            conn.close()

def save_search_result(cod_pesquisa, search_filter, result_code):
    """Salva o resultado de uma pesquisa no banco de dados."""
    conn = get_db_connection()
    if not conn:
        return

    sql = """
        INSERT INTO pesquisa_spv
            (cod_pesquisa, cod_spv, cod_spv_computador, resultado, cod_funcionario, filtro, website_id)
        VALUES
            (%(cod_pesquisa)s, 1, 36, %(resultado)s, -1, %(filtro)s, 1)
        ON CONFLICT (cod_pesquisa, cod_spv, filtro) DO NOTHING;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, {
                'cod_pesquisa': cod_pesquisa,
                'resultado': result_code,
                'filtro': str(search_filter)
            })
            conn.commit()
            logging.info(f"Resultado salvo para pesquisa {cod_pesquisa} com filtro {search_filter}.")
    except Exception as e:
        logging.error(f"Erro ao salvar resultado para pesquisa {cod_pesquisa}: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
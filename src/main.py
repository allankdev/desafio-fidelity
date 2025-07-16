import time
import logging
from tqdm import tqdm
from src import database, config
from src.scraper import Scraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_search(search_data, search_filter, scraper):
    """Processa uma única pesquisa: extrai dados, executa scraping e salva."""
    cod_pesquisa = search_data['cod_pesquisa']
    
    # Seleciona o documento correto com base no filtro
    doc_map = {0: 'cpf', 1: 'rg', 2: 'nome', 3: 'rg'}
    document_key = doc_map.get(search_filter)
    document = search_data.get(document_key)
    
    if not document:
        logging.warning(f"Documento não encontrado para pesquisa {cod_pesquisa} com filtro {search_filter}")
        return

    logging.info(f"Processando pesquisa {cod_pesquisa} com filtro {search_filter} para '{document[:30]}...'")
    
    page_source = scraper.perform_search(search_filter, document)
    
    if not page_source:
        logging.error(f"Falha ao obter a página para a pesquisa {cod_pesquisa}")
        # Opcional: Salvar como erro
        # database.save_search_result(cod_pesquisa, search_filter, config.RESULT_CODE['ERRO_INDEFINIDO'])
        return
        
    result_code = Scraper.analyze_result(page_source)
    database.save_search_result(cod_pesquisa, search_filter, result_code)

def main():
    """Função principal que executa o loop de automação."""
    while True:
        logging.info("Iniciando novo ciclo de automação.")
        found_searches_in_cycle = False

        # Itera sobre os filtros: 0 (CPF), 1 (RG), 2 (Nome), 3 (RG novamente, conforme script original)
        for search_filter in [0, 1, 2, 3]:
            logging.info(f"Buscando pesquisas pendentes com FILTRO = {search_filter}")
            
            pending_searches = database.fetch_pending_searches(search_filter, config.PESQUISA_LIMIT)
            
            if not pending_searches:
                logging.info(f"Nenhuma pesquisa pendente encontrada para o filtro {search_filter}.")
                continue

            found_searches_in_cycle = True
            scraper = Scraper()

            try:
                for search in tqdm(pending_searches, desc=f"Processando Filtro {search_filter}"):
                    process_search(search, search_filter, scraper)
            finally:
                scraper.close() # Garante que o navegador feche mesmo se ocorrer um erro

        if not found_searches_in_cycle:
            wait_time = 300 # 5 minutos
            logging.info(f"Nenhuma pesquisa encontrada em todos os filtros. Aguardando {wait_time} segundos para o próximo ciclo.")
            time.sleep(wait_time)
        else:
            logging.info("Ciclo de automação concluído. Reiniciando imediatamente.")

if __name__ == "__main__":
    main()
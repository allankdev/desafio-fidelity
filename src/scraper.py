import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from src import config

class Scraper:
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(service=service, options=options)

    def perform_search(self, search_filter, document):
        """Executa a busca no site do TJSP."""
        try:
            self.browser.get(config.URL_TJSP)
            
            filter_map = {
                0: {'select_value': 'DOCPARTE', 'input_id': 'campo_DOCPARTE'},  # CPF
                1: {'select_value': 'DOCPARTE', 'input_id': 'campo_DOCPARTE'},  # RG
                3: {'select_value': 'DOCPARTE', 'input_id': 'campo_DOCPARTE'},  # RG
                2: {'select_value': 'NMPARTE', 'input_id': 'campo_NMPARTE'}     # Nome
            }
            
            if search_filter not in filter_map:
                logging.error(f"Filtro de pesquisa inválido: {search_filter}")
                return ""

            search_params = filter_map[search_filter]

            select_el = self.browser.find_element('id', 'cbPesquisa')
            Select(select_el).select_by_value(search_params['select_value'])

            if search_filter == 2:  # Se for por nome, clica no radio button
                self.browser.find_element('id', 'pesquisarPorNomeCompleto').click()
            
            self.browser.find_element('id', search_params['input_id']).send_keys(document)
            self.browser.find_element('id', 'botaoConsultarProcessos').click()

            time.sleep(2)
            return self.browser.page_source

        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Erro de automação no Selenium para o documento '{document}': {e}")
            return ""
        except Exception as e:
            logging.error(f"Erro inesperado durante a automação: {e}")
            return ""

    @staticmethod
    def analyze_result(page_source):
        """Analisa o HTML da página de resultados e retorna um código."""
        if config.RESULT_MAP['NADA_CONSTA'] in page_source:
            return config.RESULT_CODE['SUCESSO_NADA_CONSTA']
        
        has_consta = (
            config.RESULT_MAP['CONSTA_01'] in page_source or 
            config.RESULT_MAP['CONSTA_02'] in page_source
        )
        is_criminal = 'Criminal' in page_source or 'criminal' in page_source

        if has_consta:
            return config.RESULT_CODE['SUCESSO_CRIMINAL'] if is_criminal else config.RESULT_CODE['SUCESSO_CIVEL']
        
        return config.RESULT_CODE['ERRO_INDEFINIDO']

    def close(self):
        """Fecha o navegador."""
        if self.browser:
            self.browser.quit()

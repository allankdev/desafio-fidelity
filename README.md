# Desafio Técnico - Fidelity Pesquisas Cadastrais

Este projeto é uma solução para o desafio técnico da Fidelity, que consiste em refatorar um script de automação de pesquisas jurídicas.

O objetivo foi reestruturar o código original, aplicando boas práticas de desenvolvimento de software, separando responsabilidades, migrando o banco de dados para PostgreSQL e melhorando a lógica geral da aplicação.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `src/`: Contém todo o código fonte da aplicação.
  - `main.py`: Ponto de entrada que orquestra o processo.
  - `database.py`: Módulo para interação com o banco de dados PostgreSQL.
  - `scraper.py`: Classe responsável pela automação web com Selenium.
  - `config.py`: Centraliza todas as configurações, carregadas de variáveis de ambiente.
- `requirements.txt`: Lista de dependências Python.
- `README.md`: Este arquivo.
- `.env.example`: Arquivo de exemplo para as variáveis de ambiente.

## Como Executar

### Pré-requisitos

- Python 3.8+
- PostgreSQL
- Microsoft Edge e o `msedgedriver` correspondente

### 1. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd desafio-fidelity
-- Tabela de Estados (UF)
CREATE TABLE estado (
    cod_uf SERIAL PRIMARY KEY,
    uf VARCHAR(2) NOT NULL UNIQUE,
    nome VARCHAR(50) NOT NULL
);

-- Tabela de Serviços
CREATE TABLE servico (
    cod_servico SERIAL PRIMARY KEY,
    civel VARCHAR(255),
    criminal VARCHAR(255)
);

-- Tabela de Lotes de Pesquisa
CREATE TABLE lote (
    cod_lote SERIAL PRIMARY KEY,
    cod_lote_prazo INTEGER,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cod_funcionario INTEGER,
    cod_fornecedor INTEGER,
    tipo VARCHAR(50),
    prioridade INTEGER
);

-- Tabela Principal de Pesquisas
CREATE TABLE pesquisa (
    cod_pesquisa SERIAL PRIMARY KEY,
    cod_cliente INTEGER NOT NULL,
    cod_uf INTEGER REFERENCES estado(cod_uf),
    cod_servico INTEGER REFERENCES servico(cod_servico),
    tipo INTEGER DEFAULT 0,
    cpf VARCHAR(14),
    cod_uf_nascimento INTEGER REFERENCES estado(cod_uf),
    data_entrada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP WITH TIME ZONE,
    nome TEXT,
    nome_corrigido TEXT,
    rg VARCHAR(20),
    rg_corrigido VARCHAR(20),
    cod_uf_rg INTEGER REFERENCES estado(cod_uf),
    nascimento DATE,
    mae TEXT,
    mae_corrigido TEXT,
    anexo TEXT
);

-- Tabela de Associação Lote-Pesquisa
CREATE TABLE lote_pesquisa (
    cod_lote_pesquisa SERIAL PRIMARY KEY,
    cod_lote INTEGER NOT NULL REFERENCES lote(cod_lote),
    cod_pesquisa INTEGER NOT NULL REFERENCES pesquisa(cod_pesquisa),
    cod_funcionario_conclusao INTEGER,
    cod_fornecedor INTEGER,
    data_entrada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP WITH TIME ZONE,
    cod_uf INTEGER REFERENCES estado(cod_uf),
    obs TEXT
);

-- Tabela de Resultados da Automação SPV
CREATE TABLE pesquisa_spv (
    cod_pesquisa_spv SERIAL PRIMARY KEY,
    cod_pesquisa INTEGER NOT NULL REFERENCES pesquisa(cod_pesquisa),
    cod_spv INTEGER NOT NULL,
    cod_spv_computador INTEGER,
    cod_spv_tipo INTEGER,
    cod_funcionario INTEGER,
    filtro VARCHAR(50),
    website_id INTEGER,
    resultado INTEGER,
    data_execucao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_pesquisa_spv_filtro UNIQUE (cod_pesquisa, cod_spv, filtro)
);
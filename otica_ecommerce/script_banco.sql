-- 1. Cria e seleciona o banco de dados
CREATE DATABASE IF NOT EXISTS otica_bd;
USE otica_bd;

-- 2. Cria a tabela de produtos e insere o stock inicial
CREATE TABLE produto (
    cod_produto INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    preco FLOAT NOT NULL,
    estoque INT NOT NULL,
    PRIMARY KEY(cod_produto)
);

INSERT INTO produto (nome, preco, estoque) VALUES 
('Óculos de Sol Ray-Ban Aviador', 550.00, 15),
('Armação de Grau Vogue Gatinho', 320.00, 10),
('Óculos de Sol Oakley Esportivo', 480.00, 8),
('Lentes de Contato Acuvue (Caixa)', 150.00, 30),
('Armação de Grau Armani Exchange', 410.00, 12),
('Óculos de Sol Carrera Vintage', 600.00, 5),
('Armação Infantil Turma da Mônica', 180.00, 20),
('Spray Limpa Lentes Antiembaçante', 35.00, 50),
('Óculos de Sol Prada Elegance', 1200.00, 3),
('Armação de Grau Titanium Ultra Leve', 750.00, 7);

-- 3. Cria a tabela para guardar os logins e senhas
CREATE TABLE usuario (
    cod_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    PRIMARY KEY(cod_usuario)
);

-- 4. Cria a tabela do carrinho de compras
CREATE TABLE carrinho (
    id_item INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(255) NOT NULL,
    cod_produto INT NOT NULL,
    PRIMARY KEY(id_item),
    FOREIGN KEY(cod_produto) REFERENCES produto(cod_produto)
);

-- 5. Cria a tabela para armazenar o histórico de compras
CREATE TABLE pedido (
    id_pedido INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(255) NOT NULL,
    nome_produto VARCHAR(255) NOT NULL,
    preco FLOAT NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id_pedido)
);

USE otica_bd;
ALTER TABLE carrinho ADD COLUMN quantidade INT NOT NULL DEFAULT 1;
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

USE otica_bd;

-- 1. Cria a coluna 'imagem' e define uma imagem padrão (placeholder) caso o produto não tenha foto
ALTER TABLE produto ADD COLUMN imagem VARCHAR(500) DEFAULT 'https://via.placeholder.com/250x150?text=Sem+Imagem';

UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 1;

UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 2;

UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1582142407894-ec85a1260a46?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 3;

UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1550537687-c91072c4792d?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 4; -- Lentes de Contato
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 5; -- Armani Exchange
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 6; -- Carrera Vintage
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1591076482161-42ce6da69f67?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 7; -- Armação Infantil
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 8; -- Spray Limpa Lentes
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1625591340236-41ec9cd2e238?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 9; -- Prada Elegance
UPDATE produto SET imagem = 'https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=250&q=80' WHERE cod_produto = 10; -- Titanium Ultra Leve

USE otica_bd;

UPDATE produto 
SET imagem = 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=250&q=80' 
WHERE cod_produto = 9;
CREATE DATABASE doacao_comida;

USE doacao_comida;

CREATE TABLE pessoa_fisica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20),
    localizacao VARCHAR(100)
);

CREATE TABLE restaurante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cnpj VARCHAR(20),
    endereco VARCHAR(255),
    telefone VARCHAR(20)
);

CREATE TABLE ong (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cnpj VARCHAR(20),
    responsavel VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

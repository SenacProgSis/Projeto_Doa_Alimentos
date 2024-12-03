-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS doacao_comida;
USE doacao_comida;

-- Tabela de usuários para login
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(191) NOT NULL UNIQUE, -- Ajuste no tamanho do campo email
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    cpf_cnpj VARCHAR(50) NOT  NULL,
    telefone VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'restaurante', 'ong') NOT NULL
);

-- Inserção de um usuário administrativo inicial
INSERT INTO usuarios (email, senha, nome, endereco, cpf_cnpj, telefone, tipo) VALUES 
('admin@doacao.com', 'admin123', 'Administrador', 'Rua do Passeio', '12345678901', '32456789', 'admin');




-- Tabela de doações
CREATE TABLE doacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('comida', 'roupas', 'outros') NOT NULL,
    descricao TEXT NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    localizacao VARCHAR(255) NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    
);

-- Tabela de notificações (opcional para controle de envio de notificações)
CREATE TABLE notificacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_destinatario VARCHAR(191) NOT NULL, -- Ajuste no tamanho do campo email
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    mensagem TEXT NOT NULL
);




SELECT * FROM usuarios;
-- Initialisation de la BDD pour OnionRouter
-- Auteur : Arjanit (simulé)
-- Date : 28/11/2025

CREATE DATABASE IF NOT EXISTS onion_db;
USE onion_db;

-- Table des routeurs (Topology)
-- On stocke l'IP, le Port et la Clé Publique (E, N) séparément
CREATE TABLE IF NOT EXISTS routers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    port INT NOT NULL,
    pub_key_e TEXT NOT NULL, 
    pub_key_n TEXT NOT NULL,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('online', 'offline') DEFAULT 'offline'
);

-- Table des logs (Anonymisés)
-- AC23.04 : Stockage des données
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50), -- ex: "Master", "Router-1"
    event_type VARCHAR(50),
    message TEXT
);

-- Création d'un utilisateur dédié (pour ne pas utiliser root dans le code python)
CREATE USER IF NOT EXISTS 'onion_user'@'localhost' IDENTIFIED BY 'onion_pass';
GRANT ALL PRIVILEGES ON onion_db.* TO 'onion_user'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS backend_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE backend_db;

CREATE TABLE IF NOT EXISTS hostsToScann (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    entityName VARCHAR(255),
    publicIP VARCHAR(255),
    email VARCHAR(255),
    webSite VARCHAR(255),
    nextDateToScan VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) UNIQUE
);

INSERT INTO hostsToScann VALUES('Foncal', '0.0.0.0', 'foncal@gmail.com', 'https://foncal.es/', '2023-01-01')

INSERT INTO users VALUES('admin', 'admin@localhost.com', '1234')
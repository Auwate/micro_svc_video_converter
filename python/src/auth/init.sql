CREATE DATABASE auth;

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE USER (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO USER (email, password)
VALUES ('auwate1@gmail.com', 'Admin123');
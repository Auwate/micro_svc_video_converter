# Documentation

This repository follows tutorials on building microservice dominant systems, with added modifications to increase difficulty and learning material.

Technology used include:

- Kubernetes
- Docker
  - Images are pushed to Docker Hub as well
- Python
  - Flask
- RabbitMQ (To be implemented)
- MySQL
  - Currently used for basic authentication
- JWT

# Directions

## Kubernetes setup

Please start Kubernetes (or minikube) and apply the manifest files

## MySQL setup

This repository has not yet included the init.sql file as a Volume, so you will need to apply the database, table, and authorized user.

```
CREATE DATABASE auth;

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE USER (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

# Versions

## v0.1

Date: 09/30/24
Changes:

- Added server.py
  - Uses Flask, MySQL, and JWTs
- Added Dockerfile
- Added init.sql
- Added requirement.txt
- Added manifests
  - Added MySQL Deployment & Service
  - Added Auth-service ConfigMap, Secrets, Service, & Deployment

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

## Applying Ingress

This application uses a loopback address to allow communication with the Kubernetes cluster. To add a custom loopback address, you can do edit `hosts` on either Debian or Windows

### Debian

```
sudo vim /etc/hosts

# Add something like "127.0.0.1 mp3converter.com" or "127.0.0.1 myApp.com"
```

### Windows

```
# Open notepad as adminstrator
# Click open file and go to C:\Windows\System32\drivers\etc\ and open "hosts"

# Add something like "127.0.0.1 <YOUR_CUSTOM_LOOPBACK>"
```

## MySQL setup

This repository has not yet included the init.sql file as a Volume, so you will need to apply the database, table, and authorized user.

To do this, please run:

```
kubectl get pods

# Find the MySQL pod

kubectl exec -it <MySQL_POD_ID> -- bash
./usr/bin/mysql -u root -p

# Enter admin password. If you haven't changed it, it will be "adminpass"
```

Then copy and paste this init.sql file:

```
CREATE DATABASE auth;

CREATE USER 'auth_user'@'%' IDENTIFIED BY 'Aauth123';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password)
VALUES ('test@gmail.com', 'Admin123');
```

## Testing the application

Currently, testing involves using `cURL` and using the POST utility. Here's an example:

```
curl.exe -X POST http://<YOUR_CUSTOM_LOOPBACK>/login -u auwate1@gmail.com:Admin123
```

# Versions

## v0.2

Date 10/01/24
Changes:

- Added gateway directory
  - Added server.py
  - Added Dockerfile
  - Added subdirectories
  - Fixed connectivity issues regarding auth pods
- Fixed auth directory
  - Fixed issues regarding Flask and connections
- Added rabbitmq directory
  - Created outline for manifests

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

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

All console commands will start with "$"

*IMPORTANT*

If you are using Windows, use `curl.exe` for all cURL commands.

## Kubernetes setup

Please start Kubernetes (or minikube) and apply the manifest files

## Applying Ingress

This application uses a loopback address to allow communication with the Kubernetes cluster. To add a custom loopback address, you can do edit `hosts` on either Debian or Windows

### Debian

```
$ sudo vim /etc/hosts

# Add something like "127.0.0.1 mp3converter.com" or "127.0.0.1 myApp.com"
```

### Windows

```
# Open notepad as adminstrator
# Click open file and go to C:\Windows\System32\drivers\etc\ and open "hosts"

# Add something like "127.0.0.1 <YOUR_CUSTOM_LOOPBACK>"
```

## MySQL Setup

The project contributor decided to use a relational database for ease-of-use and ACID compliance, using a master-slave setup to provide limited scalability. Currently the setup is limited to 2 nodes as the slave MySQL instance is not automated yet.

To do this, please apply the manifest and run:

```
$ kubectl exec -it auth-master-sfs-0 -- mysql -u root -p
# Enter admin password

$ SHOW MASTER STATUS;
# Copy the name of the bin log. It should be something like mysql-bin.000001
# Copy the position of the bin log's latest entry. It should be something like 1740
exit

$ kubectl exec -it auth-slave-sfs-0 -- mysql -u root -p
# Enter admin password

$ CHANGE MASTER TO 
    MASTER_HOST='auth-master-sfs-0.auth-master-headless-service', 
    MASTER_USER='replica_user', 
    MASTER_PASSWORD='replica_password', 
    MASTER_LOG_FILE='<ENTER BIN LOG NAME HERE>', # Enter bin_log_name here with quotes
    MASTER_LOG_POS=<ENTER BIN LOG POSITION>; # Enter bin_log_pos here with no quotes

$ START SLAVE;
# The slave DB will not start without this command
```

## Testing the application

Currently, testing involves using `cURL` and using the POST utility. To install, you can use:

`apt install curl` if you are on a Linux distro
`choco install curl` if you are on Windows

This command will send a message to the `auth` application, returning a JWT

```
curl -X POST http://<YOUR_CUSTOM_LOOPBACK>/login -u test@gmail.com:Admin123
```

This command will return a 400 response, but it will interface with `/validate`

```
curl -X POST http//<YOUR_CUSTOM_LOOPBACK>/upload -H "Authorization: Bearer <PUT_JWT_HERE>"
```

# Versions

## v0.4

Date 11/06/24
Changes:

- Added `accessed` to database tables
  - A `DATETIME` object that references the last time the user interacted with the API
- Added new `admin/recent` API to see who has accessed the API recently
- Added Redis
  - Because `admin/recent` is a computationally expensive operation, it is better for cache the data on Redis and pull from there whenever possible
- Fixed `auth_user` on both master and slave from not being able to interact with databases
- Changed logic on `auth/server.py` to reference Redis and update the master database.

## v0.3

Date 10/15/24
Changes:

- Changed to MySQL replicaset
  - Added master node
  - Added replica node
    - Replica nodes can be scaled out infinitely if needed, as it is part of a ClusterIP Service
- Added HTTP status codes to Flask responses
- Fixed connectivity issues from gateway API to auth pods
- Changed responses to be in JSON format

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

# The Minimarket

## Description

The purpose of this project is to show the abilities both of [Docker](https://docs.docker.com) and [Kubernetes](https://kubernetes.io/).  
This project simulates an online market/shop, where you can "buy" and view your purchase history.   
The whole infrastructure is configured and ran on Kubernetes (using [Helm](https://helm.sh/) chart) or [Docker Compose](https://docs.docker.com/compose/).  
(Created by mr-anderson86, started @11/2021)

## Structure
<img src="Infrastructure.png" alt="Infrastructure Design" width="500"/>

* [The Frontend](frontend) - the frontend generates a new purchase and send the data to the Kafka.  
In addition, it can also request from the backend API for purchase history of a specific user (and show the result).
* [The Kafka Consumer](backend_consumer) - part of the backend, which listens to the Kafka.  
Each time there's a new data (a new purchase) it consumes it, and sends the data into the MongoDB.
* [The Backend API Server](backend_api) - another flask application (not exposed to external network), which listens to requests from the frontend .  
Currently, handles only 1 request: get the purchase history of a specific user.  
When such request is received, it queries the MongoDB for the data, and sends the data back to the fronted.
* Frontend, Backend, Kafka and MongoDB, are all being deployed via [docker-compose](docker-compose.yml) or by [Helm chart](kubernetes/helm/minimarket).  
  (In docker-compose, The frontend, API server and Kafka consumer are all being firstly docker built)

## Usage

### To start the minimarket
* Via Docker Compose:  
(need Docker installed on your host/computer)
```bash
git clone https://github.com/mr-anderson86/minimarket_kubernetes.git
cd minimarket_kubernetes
docker-compose up -d
```

* Via Kubernetes:  
(need to have both kubernetes and helm installed, and of course an existing k8s cluster, such as minikube, etc...)
```bash
git clone https://github.com/mr-anderson86/minimarket_kubernetes.git
cd minimarket_kubernetes/kubernetes/helm
# helm install [your app name] minimarket, example below:
helm install minimarket minimarket

# If needed anymore network configuration to allow incoming requests, 
# such as minikube tunnel
# or kubectl proxy, etc...
# now it's a good time ;-)
```

That's it, then all you need is to open your browser and go to http://localhost:9090/  
It explains there how to generate a random purchase, and also how to retrieve purchase history of a specific user.  
  
You might need to wait ~10 seconds before the frontend application is up and running.  
Or you can tail the frontend log in realtime, until you see it's running:
```bash
# For docker:
docker logs -f frontend
# For k8s:
kubectl logs -f <frontend pod name> -n minimarket (or whichever namespace you gave in values)

kafka_url = kafka:9092
backend_url = backend:9091
Attempting to connect to kafka...
Attempting to connect to kafka...
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.192.8:9090/ (Press CTRL+C to quit)
```

### To stop the minimarket.
* Via Docker:  
  (from the same directory type this command)
```bash
docker-compose down
```
The data from the DB won't be lost, since it is mounted from your host, so you'll see a new directory **mongodb** in your project's directory, 
and it contains all purchase history data.  
When you'll rerun the minimarket once again, the whole data will be mounted into the MongoDB, thus all purchase history will be there.

* Via Helm:
```bash
helm uninstall [your app name]
```
  
## Bonus
Also added mongo-express, so you could access the data in your mongodb via web browser.  
just go to http://localhost:8081/ (And enter the username and password mentioned in the [docker-compose.yml](docker-compose.yml) file) and there you can browse at your own will. :-)
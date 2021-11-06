# The Minimarket

## Description

This project simulates an online market/shop, where you can "buy" and view your purchase history.   
The whole infrastructure is configured and ran via docker-compose.  
(Created by mr-anderson86, started @11/2021)

## Structure
<img src="Infrastructure.png" alt="Infrastructure Design" width="500"/>

* [The Frontend](frontend) - the frontend generates a new purchase and send the data to the Kafka.  
In addition, it can also request from the backend API for purchase history of specific user (and show the result).
* [The Kafka Consumer](backend_consumer) - part of the backed, which listens to the Kafka.  
Each time there's a new data (a new purchase) it consumes it, and sends the data into the MongoDB.
* [The Backend API Server](backend_api) - another flask application (not exposed to external network), which listens to requests from the frontend .  
Currently, handles only 1 request: get the purchase history of a specific user.  
When such request is received, it queries the MongoDB for the data, and sends the data back to the fronted.
* Frontend, Backend, Kafka and MongoDB, are all being deployed via [docker-compose](docker-compose.yml).  
  (The frontend, api server and kafka consumer are being firstly docker built, also via the docker compose)

## Usage
```bash
git clone https://github.com/mr-anderson86/minimarket.git
cd minimarket
docker-compose up -d
```

That's it, then all you need is to open your browser and go to http://localhost:9090/  
It explains there how to generate a random purchase, and also how to retrieve purchase history of a specific user.  
(You might need to wait ~10 seconds before the frontend application is up and running)
  
## Bonus
Also added mongo-express, so you could access the data in your mongodb via web browser.  
just go to http://localhost:8081/ (And enter the username and password mentioned in the [docker-compose.yml](docker-compose.yml) file) and there you can browse at your own will. :-)
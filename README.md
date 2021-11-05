# minimarket

## Usage
```bash
git clone https://github.com/mr-anderson86/minimarket.git
cd minimarket
docker-compose up -d
```

That's it, then all you need is to open your browser and go to http://localhost:9090/  
It explains there how to generate a random purchase, and also how to retrieve purchase history of a specific user.  
  
## Bonus
Also added mongo-express so you could access the data in your mongodb via web browser.  
just go to http://localhost:8081/ (And enter the username and password mentioned in the [docker-compose.yml](docker-compose.yml) file) and there you can browse at your own will. :-)
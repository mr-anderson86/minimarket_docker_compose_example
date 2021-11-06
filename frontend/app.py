from json import dumps
from kafka import KafkaProducer
from flask import Flask, request
from time import sleep
import random
import datetime
import os
import requests
from app_data import products, users

kafka_url = os.environ.get('KAFKA_URL')  # localhost:29092
backend_url = os.environ.get('BACKEND_URL')  # localhost:9091
print("kafka_url =", kafka_url)
print("backend_url =", backend_url)
producer = ''

tries = 0
while tries < 6:
    try:
        print("Attempting to connect to kafka...")
        producer = KafkaProducer(
            bootstrap_servers=[kafka_url],
            value_serializer=lambda x:
            dumps(x).encode('utf-8'),
            retries=5)
        break
    except:
        tries += 1
        sleep(10)

if tries == 6:
    raise ConnectionError("Couldn't connect to kafka")


app = Flask(__name__)


@app.route("/")
def hello():
    text = "Hello, welcome to the miniminimini-market :-) <br><br>" \
           "to generate a random buying, just visit <a href=\"" + request.base_url + "buy\">" + request.base_url + "buy</a><br>" \
           + "buy and refresh the page as many times as you want. <br><br>" \
           "" \
           "In order to view purchase history, just visit <a href=\"" + request.base_url + "getAllUserBuys?userid=[userid]\">" + request.base_url + "getAllUserBuys?userid=[userid]</a><br>" \
           + "And add the user ID in the link. Example: " + request.base_url + "getAllUserBuys?userid=1234"
    return text, 200


@app.route("/buy")
def order_purchase():
    user = random.choice(users)
    username = user['name']
    userid = user['id']
    purchase = random.choice(products)
    product = purchase['product']
    price = purchase['price']
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()
    data = {'username': username,
            'userid': userid,
            'product': product,
            'price': price,
            'timestamp': timestamp}
    print("Sending data " + str(data))
    try:
        producer.send('purchases', value=data)

        return """Hello. :-)<br><br>
        Username: """ + username + """<br>
        User ID: """ + str(userid) + """<br>
        Product: """ + product + """<br>
        Price: """ + price + """<br>
        Timestamp: """ + str(current_time) + """<br><br>
        Purchase ordered successfully.""", 200

    except Exception as e:
        err_name = type(e).__name__
        err_msg = str(e)
        print("[ERROR]", err_name, "has occurred.", err_msg)
        return {"code": 500, "status": "ERROR", "msg": err_name + " has occurred. " + err_msg}, 500


@app.route("/getAllUserBuys")
def get_all_user_buys():
    userid = request.args.get('userid')
    url = 'http://' + backend_url + '/getAllUserBuys'
    userid_param = {'userid': userid}
    try:
        response = requests.get(url, params=userid_param)
        data = response.json()
        # print(data)
        if not (data['code'] == 200):
            raise Exception(data['msg'])
        return data, 200

    except Exception as e:
        err_name = type(e).__name__
        err_msg = str(e)
        print("[ERROR]", err_name, "has occurred.", err_msg)
        return {"code": 500, "status": "ERROR", "msg": err_name + " has happened. " + err_msg, "list": []}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)

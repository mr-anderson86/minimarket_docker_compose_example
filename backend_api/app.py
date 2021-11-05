from pymongo import MongoClient
from flask import Flask, request
import os

mongo_url = os.environ.get('MONGO_URL')  # localhost:27017
mongo_user = os.environ.get('MONGO_USER')  # root
mongo_pass = os.environ.get('MONGO_PASS')  # pass12345
client = MongoClient(mongo_url,
                     username=mongo_user,
                     password=mongo_pass)
db = client["purchases"]
collection = db["history"]
app = Flask(__name__)


@app.route("/getAllUserBuys")
def get_all_user_buys():
    try:
        userid = request.args.get('userid')
        print("userid =", userid)
        query = {"userid": int(userid)}

        result = list(collection.find(query, {'_id': False}))
        # print(result)
        return {"code": 200, "status": "OK", "msg": "", "list": result}, 200

    except Exception as e:
        err_name = type(e).__name__
        err_msg = str(e)
        print("[ERROR]", err_name, "has occurred.", err_msg)
        return {"code": 500, "status": "ERROR", "msg": err_name + " has happened. " + err_msg, "list": []}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9091)

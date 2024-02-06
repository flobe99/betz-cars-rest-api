from bson.json_util import dumps
from flask import Flask
from pymongo.mongo_client import MongoClient
from flask import jsonify, request


uri = "mongodb://flobe:test@ac-3gep0lx-shard-00-00.xl7gtcu.mongodb.net:27017,ac-3gep0lx-shard-00-01.xl7gtcu.mongodb.net:27017,ac-3gep0lx-shard-00-02.xl7gtcu.mongodb.net:27017/?ssl=true&replicaSet=atlas-vkht93-shard-0&authSource=admin&retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

print("##########################")


mongo = client.Cars

app = Flask(__name__)

@app.route('/fuels', methods = ['GET'])
def fuels():
    fuel = mongo.fuel.find()
    resp = dumps(fuel)
    return resp

@app.route('/addfuels', methods = ['POST'])
def add_fuels():
    _json = request.json
    _kilometer = _json['kilometer']
    _price_liter = _json['price_liter']
    _amount_liter = _json['amount_liter']
    _price = _json['price']
    _date = _json['date']

    if _kilometer and _price_liter and _amount_liter and _date and _price and request.method == 'POST':         
        id = mongo.fuel.insert_one({"kilometer":_kilometer,"price_liter":_price_liter,"amount_liter":_amount_liter,"date":_date, "price":_price})
        
        resp = jsonify("Fuel added successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()

@app.route('/cars',  methods=['GET'])
def cars():
    cars = mongo.car.find()
    resp = dumps(cars)
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()

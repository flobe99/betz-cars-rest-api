from bson.json_util import dumps
from flask import Flask
from pymongo.mongo_client import MongoClient
from flask import jsonify, request
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route('/users/addUser', methods=['POST'])
def add_user():
    _json = request.json
    _first_name = _json['first_name']
    _last_name = _json['last_name']
    _email = _json['email']
    _password = _json['password']

    if _first_name and _last_name and _email and _password and request.method == 'POST': 
        _hashed_password = generate_password_hash(_password)
        
        id = mongo.user.insert_one({"first_name":_first_name,"last_name":_last_name,"email":_email,"password":_hashed_password})
        
        resp = jsonify("User added successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def users():
    users = mongo.user.find()
    resp = dumps(users)
    return resp

@app.route('/users/<id>', methods=['GET'])
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/users/deleteUser/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User deleted successfully")

    resp.status_code = 200
    return resp

@app.route('/users/updateUser/<id>',  methods=['PUT'])
def user_update(id):
    _id = id
    _json = request.json
    _first_name = _json['first_name']
    _last_name = _json['last_name']
    _email = _json['email']
    _password = _json['password']

    if _first_name and _last_name and _email and _password and request.method == 'PUT':

        _hashed_password = generate_password_hash(_password)

        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {"first_name":_first_name, "last_name":_last_name, "email":_email,"password":_hashed_password}})

        resp = jsonify("User updated successfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()

@app.route('/fuels', methods = ['GET'])
def fuels():
    fuel = mongo.fuel.find()
    resp = dumps(fuel)
    return resp

@app.route('/fuels/addfuels', methods = ['POST'])
def add_fuels():
    _json = request.json
    _carId = _json['_carId']
    _kilometer = _json['kilometer']
    _price_liter = _json['price_liter']
    _amount_liter = _json['amount_liter']
    _price = _json['price']
    _date = _json['date']

    if _carId and _kilometer and _price_liter and _amount_liter and _date and _price and request.method == 'POST':         
        id = mongo.fuel.insert_one({"_carId" : ObjectId(_carId),"kilometer":_kilometer,"price_liter":_price_liter,"amount_liter":_amount_liter,"date":_date, "price":_price})
        
        resp = jsonify("Fuel added successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()
    
@app.route('/fuels/updatefuels/<fuelId>', methods = ['PUT'])
def update_fuels():
    _json = request.json
    _carId = _json['_carId']
    _kilometer = _json['kilometer']
    _price_liter = _json['price_liter']
    _amount_liter = _json['amount_liter']
    _price = _json['price']
    _date = _json['date']

    if _carId and _kilometer and _price_liter and _amount_liter and _date and _price and request.method == 'PUT':         
        id = mongo.fuel.update_one({"_carId":_carId, "kilometer":_kilometer,"price_liter":_price_liter,"amount_liter":_amount_liter,"date":_date, "price":_price})
        
        resp = jsonify("Fuel added successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()
    
@app.route('/fuels/deleteFuel/<fuelId>', methods=['DELETE'])
def deleteFuel(fuelId):
    print(fuelId)
    mongo.fuel.delete_one({'_id':ObjectId(fuelId)})
    resp = jsonify("User deleted successfully")

    resp.status_code = 200
    return resp

@app.route('/cars',  methods=['GET'])
def cars():
    cars = mongo.car.find()
    resp = dumps(cars)
    return resp

@app.route('/cars/<carId>', methods = ['GET'])
def car(carId):
    car = mongo.car.find_one({'_id': ObjectId(carId)})
    resp = dumps(car)
    return resp

@app.route('/cars/addCar', methods = ['POST'])
def add_car():
    _json = request.json
    _producer = None
    _modell = None
    _year = None
    _kilometers = None
    _buying_price = None
    _repair_costs = None
    _customer_service = None
    _oil_change = None
    _next_inspection = None

    if _json:
        if 'producer' in _json:
            _producer = _json['producer']
        if 'modell' in _json:
            _modell = _json['modell']
        if 'year' in _json:
            _year = _json['year']
        if 'kilometers' in _json:
            _kilometers = _json['kilometers']
        if 'buying-price' in _json:
            _buying_price = _json['buying-price']
        if 'repair-costs' in _json:
            _repair_costs = _json['repair-costs']
        if 'customer-service' in _json:
            _customer_service = _json['customer-service']       
        if 'oil-change' in _json:
            _oil_change = _json['oil-change']   
        if 'next-inspection' in _json:
            _next_inspection = _json['next-inspection']                                                                                            

    if _producer and _modell and request.method == 'POST': 

        id = mongo.car.insert_one(
            {
            "producer": _producer,
            "modell": _modell,
            "year": _year,
            "kilometers": _kilometers,
            "buying-price": _buying_price,
            "repair-costs": _repair_costs,
            "customer-service": _customer_service,
            "oil-change": _oil_change,
            "next-inspection": _next_inspection
            }
        )

    resp = jsonify("Car added successfully")

    resp.status_code = 200

    return resp

@app.route('/cars/updateCar/<carId>', methods= ['PUT'])
def update_car(carId):

    _json = request.json
    _producer = None
    _modell = None
    _year = None
    _kilometers = None
    _buying_price = None
    _repair_costs = None
    _customer_service = None
    _oil_change = None
    _next_inspection = None

    if _json:
        if 'producer' in _json:
            _producer = _json['producer']
        if 'modell' in _json:
            _modell = _json['modell']
        if 'year' in _json:
            _year = _json['year']
        if 'kilometers' in _json:
            _kilometers = _json['kilometers']
        if 'buying-price' in _json:
            _buying_price = _json['buying-price']
        if 'repair-costs' in _json:
            _repair_costs = _json['repair-costs']
        if 'customer-service' in _json:
            _customer_service = _json['customer-service']       
        if 'oil-change' in _json:
            _oil_change = _json['oil-change']   
        if 'next-inspection' in _json:
            _next_inspection = _json['next-inspection']  

    car = mongo.car.update_one(
        {
            '_id': ObjectId(carId),
            "producer": _producer,
            "modell": _modell,
            "year": _year,
            "kilometers": _kilometers,
            "buying-price": _buying_price,
            "repair-costs": _repair_costs,
            "customer-service": _customer_service,
            "oil-change": _oil_change,
            "next-inspection": _next_inspection
        }
    )

@app.route('/cars/deleteCar/<carId>', methods= ['DELETE'])
def delete_car(carId):
    car = mongo.car.delete_one({'_id': ObjectId(carId)})
    resp = jsonify("Car deleted successfully")
    return resp

@app.route('/repairs', methods = ['GET'])
def repairs():
    car = mongo.repair.find()
    resp = dumps(car)
    return resp

@app.route('/repairs/<repairId>', methods = ['GET'])
def repair(repairId):
    car = mongo.db.repair.find({'_id': ObjectId(repairId)})
    resp = dumps(car)
    return resp

@app.route('/repairs/addRepair', methods = ['POST'])
def addRepair():
    _json = request.json

    _summary = _json['summary']
    _date = _json['date']
    _workshop = _json['workshop']
    _costs = _json['costs']
    _kilometers = _json['kilometers']

    car = mongo.db.repair.insert_one(
        {
            'summary': _summary,
            'date': _date,
            'workshop': _workshop,
            'costs': _costs,
            'kilometers': _kilometers
        }
    )
    resp = jsonify("Repair added successfully")
    return resp

@app.route('/repairs/deleteRepair/<repairId>', methods= ['DELETE'])
def delete_car(repairId):
    car = mongo.repair.delete_one({'_id': ObjectId(repairId)})
    resp = jsonify("Repair deleted successfully")
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

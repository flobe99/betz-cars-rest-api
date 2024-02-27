import datetime
from bson.json_util import dumps
from flask import Flask
from pymongo.mongo_client import MongoClient
from flask_bcrypt import Bcrypt 

from flask import jsonify, request
from bson.objectid import ObjectId
from datetime import datetime

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

bcrypt = Bcrypt(app) 

@app.route('/users/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        
        # Check if the username already exists
        if mongo.users.find_one({'username': _username}):
            resp = jsonify("Username already exists. Choose a different one."), 401
        else:
            _hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')
            mongo.users.insert_one({'username': _username, 'password': _hashed_password})
            resp = jsonify("Registration successful. You can now log in."), 200
            return resp
        

    return resp

@app.route('/users/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _json = request.json
        _username = _json['username']
        _password = _json['password']

        # Check if the username and password match
        user = mongo.users.find_one({'username': _username})
        if bcrypt.check_password_hash(user["password"], _password):
            resp = jsonify("Login successful."), 200
            # Add any additional logic, such as session management
        else:
            resp = jsonify("Invalid username or password. Please try again."), 401

    return resp

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
    _carId = _json['carId']
    _kilometer = _json['kilometer']
    _price_liter = _json['price_liter']
    _amount_liter = _json['amount_liter']
    _price = _json['price']
    _date = _json['date']

    date_object = datetime.fromisoformat(_date.replace("Z", "+00:00"))

    if _carId and _kilometer and _price_liter and _amount_liter and _price and _date  and request.method == 'POST':         
        id = mongo.fuel.insert_one({"_carId" : ObjectId(_carId),"kilometer":_kilometer,"price_liter":_price_liter,"amount_liter":_amount_liter,"date":date_object, "price":_price})
        
        resp = jsonify("Fuel added successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()
    
@app.route('/fuels/updatefuels/<fuelId>', methods = ['PUT'])
def update_fuels(fuelId):
    _json = request.json
    _carId = _json['carId']
    _kilometer = _json['kilometer']
    _price_liter = _json['price_liter']
    _amount_liter = _json['amount_liter']
    _price = _json['price']
    _date = _json['date']
    print("fuelId: "+fuelId)

    date_object = datetime.fromisoformat(_date.replace("Z", "+00:00"))

    if _carId and _kilometer and _price_liter and _amount_liter and _date and _price and request.method == 'PUT':         
        id = mongo.fuel.update_many({"_id": ObjectId(fuelId)},{"$set":{"_carId" : ObjectId(_carId),"kilometer":_kilometer,"price_liter":_price_liter,"amount_liter":_amount_liter,"date":date_object, "price":_price}},upsert=True)
        
        resp = jsonify("Fuel updated successfully")

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
    cars = mongo.car.aggregate([
  {
    "$lookup": {
      "from": "fuel",
      "localField": "_id",
      "foreignField": "_carId",
      "as": "fuelData"
    }
  },
  {
    "$unwind": "$fuelData"
  },
  {
    "$sort": {
      "fuelData.kilometer": -1
    }
  },
  {
    "$group": {
      "_id": "$_id",
      "buying-price": {
        "$first": "$buying-price"
      },
      "customer-service": {
        "$first": "$customer-service"
      },
      "kilometer": {
        "$first": "$fuelData.kilometer"
      },
      "last_fuel": {
          "$first": "$fuelData.date"
      },
      "modell": {
        "$first": "$modell"
      },
      "next-inspection": {
        "$first": "$next-inspection"
      },
      "oil-change": {
        "$first": "$oil-change"
      },
      "producer": {
        "$first": "$producer"
      },
      "repair-costs": {
        "$first": "$repair-costs"
      },
      "year": {
        "$first": "$year"
      }
    }
  },
  {
    "$project": {
      "_id": 1,
      "buying-price": 1,
      "customer-service": 1,
      "kilometer": 1,
      "modell": 1,
      "next-inspection": 1,
      "oil-change": 1,
      "producer": 1,
      "repair-costs": 1,
      "year": 1
    }
  }
])
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

@app.route('/cars/fuels/<carId>', methods= ['GET'])
def car_fuels(carId):
    fuels = mongo.fuel.find({"_carId" : ObjectId(carId)}).sort({"date": -1})
    resp = dumps(fuels)
    return resp

@app.route('/cars/repairs/<carId>', methods= ['GET'])
def car_repairs(carId):
    repair = mongo.repair.find({"_carId" : ObjectId(carId)}).sort({"date": -1})
    resp = dumps(repair)
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
def delete_repair(repairId):
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

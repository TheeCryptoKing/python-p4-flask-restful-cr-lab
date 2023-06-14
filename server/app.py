#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# fetch("http://localhost:5000/plants")
class Plants(Resource):
    def get(self):

        # .to_dict() and jsonify() do the smae thing
        # plants_to_dict = [plant.to_dict() for plant in Plant.query.all()]
        plants = Plant.query.all()
        plants_to_dict = [plant.to_dict() for plant in plants]
        response = make_response(jsonify(plants_to_dict),200)
        return response
        # figure out difference 
    # def post(self):
    # used for 
    #     new_plant=Plant(
    #         name=request.form.get("name"),
    #         image=request.form.get("image"),
    #         price=request.form.get("price")
    #     )
    def post(self):
        # sent as a body in the post
        data = request.get_json()
        new_plant =Plant(
            name=data['name'],
            image=data["image"],
            price=data["price"]
        )
        
        db.session.add(new_plant)
        db.session.commit()
        
        Plant_dict = new_plant.to_dict()
        response = make_response(Plant_dict, 201)
        return response 
        # return make_response(new_plant.to_dict(),201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        # data = request.get_json()
        # request.get_json() parses the JSON data from the request body and returns it as a Python dictionary.
        # will be a Python dictionary containing the JSON payload
        #  when data accessed, will manipulate the JSON data as needed
        plants = Plant.query.filter_by(id=id).first().to_dict()
        # unusre if need to make a dict
        response = make_response(jsonify(plants), 200)
        return response

api.add_resource(PlantByID,'/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

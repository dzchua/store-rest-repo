import os #read the virtual environment

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #read the first variable for cloud hosting heroku postgre, default: 2nd value for local environment.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to know object changed but not saved in database: turn it off as it is a tracker
app.secret_key = 'jose'
api = Api(app)

# @app.before_first_request #create database
# def create_tables():
#     db.create_all()

#app.config['JWT_AUTH_URL_RULE'] = '/login' # changes /auth to /login
jwt = JWT(app, authenticate, identity) # /auth - default


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':         #only file that is run = main, if main=name: run the file and start flask server
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True) #error msg to tell

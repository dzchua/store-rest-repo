import sqlite3
from db import db

class UserModel(db.Model): #API
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password): #SQlite or any kind: auto increment id, therefore id removed
        #self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM users WHERE username=?" #WHERE limit to only rows that matches a parameter
        # result = cursor.execute(query, (username,)) #has to be tuple
        # row = result.fetchone() #fetch 1st rows
        # if row: #if there is row, create user object from data of the row
        #     user = cls(*row)
        # else:
        #     user = None
        # connection.close()
        # return user
        return cls.query.filter_by(username=username).first() # SELECT * FROM users LIMIT 1

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

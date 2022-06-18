#import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True) #read the columns
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') #lazy='dynamic' to tell ItemModel not to create each item for each store yet

    def __init__(self, name): #create object
        self.name = name

# each item from ItemModel objects are retrieved using self.items.all(). Because item is an ItemModel object, json() function can be called
    def json(self): #unless used, not looking into table
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod #returns the object of ItemModel not dictionary
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #query from class || SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self): #insert and update
        db.session.add(self) #for one insert
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

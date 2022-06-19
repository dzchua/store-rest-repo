from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
#API wont work if it returns object, only dict

class Item(Resource):
    parser = reqparse.RequestParser() #able to use: HTML to send data
    parser.add_argument('price', #only price field, others will be erased
        type=float,              #put on the very top and use Item.[] instead of copy/paste
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required() #token will be require, can put on all def but troublesome
    def get(self, name): #READ
        # for item in items:
        #     if item['name'] == name:
        #         return item #no need jsonify when flask_restful is used

        # next(filter(...)) gives first item of filter, call next again for more items but we only have one. If no items, it will break unless none
        #item = next(filter(lambda x: x['name'] == name, items), None) #filter x, then the list of items fitered
        #return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #because it returns object after changing models.item, need to change: JSON represents objects as name/value pairs, just like a Python dictionary.
        return {'message': 'Item not found'}, 404

    def post(self, name): #CREATE
        if ItemModel.find_by_name(name): #self.get is from jwt_required || self. is from classmethod
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        #data = request.get_json() #force: not need content-type header |silent: none
        data = Item.parser.parse_args() #checks for price                 #This is put below because the above code checks for error, if ok, proceed.

        item = ItemModel(name, **data)

        try: #do this if fails to search, then...
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 #internal server error

        return item.json(), 201 #created, must return json

    def delete(self, name): #delete
        ##global items #from outside
        ##items = list(filter(lambda x: x['name' ] != name, items))

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?" #delete specific column: unique
        # cursor.execute(query, (name,)) #
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}
    #return {'message': 'Item not found.'}, 404

    def put(self, name): #UPDATE
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name) #it is just python entity that has name and price not the database


        if item is None:
            item = ItemModel(name, data['price'], data['store_id']) #**data
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        # return {'items': items}

        return {'items': [item.json() for item in ItemModel.query.all()]} #return json instead of all objects
        #or              list(map(lambda x: x.json(), ItemModel.query.all())) || mapping of functions to elements

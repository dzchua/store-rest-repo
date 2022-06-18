from hmac import compare_digest
from models.user import UserModel

# users = [User(1, 'bob', 'asdf')]
# username_mapping = {u.username: u for u in users} #assign key value pairs
# userid_mapping = {u.id: u for u in users} || userid_mapping.get(user_id, None)

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password): #safe_str_cmp instead of == password, safer
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

from flask import Flask
from flask_cors import CORS
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
import json


# init
app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# create 2 models one for users and one for messages
model_user = api.model('User', {'username' : fields.String('Name of the User')})
model_message = api.model('Message', {'username' : fields.String('Username of the User'),'message' : fields.String('Message user wants to send'),'time' : fields.String('Timestamp of the Message'),'receiver' : fields.String('who can see the messages')})

# creating 2 arrays (messages and users)
messages = []
users = []
admins = [{'username': 'ale'}]

# Users API call
@api.route('/api/users')
class User(Resource):
    # Get all Users in the Chatroom
    def get(self):
        return users

    # Put an new User to the Chatroom
    @api.expect(model_user)
    def put(self):
        username = api.payload
        if username in users:
            print( username + 'already signed in')
            return {'result' : 'You are already signed in'}, 403
        users.append(username)
        return {'result' : 'user added to the chatroom'}, 201
        # doesnt work yet
        if username in admins:
            print('User is Admin')
            # Do something here

    # Remove User from the Chatroom
    @api.expect(model_user)
    def delete(self):
        users.remove(api.payload)
        return {'result' : 'User removed from the chatroom'}, 200

# Message API Call
@api.route('/api/messages')
class Message(Resource):
    # Returns all Messages in the Chatroom
    def get(self):
        return messages

    # Posts a new Message to the Chatroom
    @api.expect(model_message)
    def post(self):
        username = api.payload['username']
        print(username)
        messages.append(api.payload)
        return {'result' : 'user sent the message'}, 201

    # Remove Message from the Chatroom
    @api.expect(model_message)
    def delete(self):
        messages.remove(api.payload)
        return {'result' : 'Message removed from the chatroom'}, 200



if __name__ == '__main__':
    app.run(debug=True)

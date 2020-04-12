from flask import Flask
from flask_restplus import Api, Resource, fields

# init
app = Flask(__name__)
api = Api(app)

# create 2 models one for users and one for messages
model_user = api.model('User', {'ip' : fields.String('ip adress of the user'),'username' : fields.String('Username of the User')})
model_message = api.model('Message', {'username' : fields.String('Username of the User'),'message' : fields.String('Message user wants to send')})

# creating 2 arrays (messages and users) and create for each array an initial object
messages = []
init_message = {
                          "username": "chatbot",
                          "message": "welcome to the chat!"
                        }
messages.append(init_message)
users = []
init_user = {
              "ip": "192.168.1.15",
              "username": "ale"
            }
users.append(init_user)

# Users API call
@api.route('/api/users')
class User(Resource):
    # Get all Users in the Chatroom
    def get(self):
        return users

    # Put an new User to the Chatroom
    @api.expect(model_user)
    def put(self):
        users.append(api.payload)
        return {'result' : 'User added to the chatroom'}, 201

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
        messages.append(api.payload)
        return {'result' : 'User sent the message'}, 201

if __name__ == '__main__':
    app.run(debug=True)

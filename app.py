from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

model_user = api.model('User', {'ip' : fields.String('ip adress of the user'),'username' : fields.String('Username of the User')})
model_message = api.model('Message', {'username' : fields.String('Username of the User'),'message' : fields.String('Message user wants to send')})

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

@api.route('/api/users')
class User(Resource):
    def get(self):
        return users

    @api.expect(model_user)
    def put(self):
        users.append(api.payload)
        return {'result' : 'User added to the chatroom'}, 201

    @api.expect(model_user)
    def delete(self):
        users.remove(api.payload)
        return {'result' : 'User removed from the chatroom'}, 200

@api.route('/api/messages')
class Message(Resource):
    def get(self):
        return messages

    @api.expect(model_message)
    def post(self):
        messages.append(api.payload)
        return {'result' : 'User sent the message'}, 201

if __name__ == '__main__':
    app.run(debug=True)

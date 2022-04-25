from flask import Flask
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)

class Message(Resource):
    def get(self):
        return {'data': 'hello world'}, 200
    pass

api.add_resource(Message, '/test')  # '/users' is our entry point

if __name__ == '__main__':
    app.run()  # run our Flask app
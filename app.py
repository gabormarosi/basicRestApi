import jwt
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
import jwt
from jwt import PyJWKClient

app = Flask(__name__)
api = Api(app)

class Message(Resource):
    def get(self):
        try:
            token = request.headers.get("Authorization","none")[7:]
            decoded = jwt.decode(token,options={"verify_signature": False})
            email = decoded["email"]
            print(decoded)
            print(email)
            return {'email': decoded["email"]}, 200
        except jwt.InvalidTokenError:
            return {'message_from_demoapp':'invalid token'}, 400
        except KeyError:
            return {'message_from_demoapp':'email is missing'}, 400
        except Exception:
            return {'message_from_demoapp':'Some error occurred.'}, 400
    pass

class JwksProcessor(Resource):
    def get(self):
        url = 'https://test.cs.azure.nevis.dev/.well-known/openid-configuration/jwks.json'
        try:
            jwks_client = PyJWKClient(url)
        except Exception:
            return {'message_from_demoapp': 'unable to download JWKS'}, 400
        try:
            token = request.headers.get("Authorization","none")[7:]
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"], options={"verify_exp": True})
            email = decoded["email"]
            print(decoded)
            return {'email': decoded["email"]}, 200
        except jwt.InvalidTokenError:
            return {'message_from_demoapp':'invalid token'}, 400
        except KeyError:
            return {'message_from_demoapp':'email is missing'}, 400
#        except Exception:
#            return {'message_from_demoapp':'Some error occurred.'}, 400
    pass

api.add_resource(Message, '/test')  # '/test' is our entry point
api.add_resource(JwksProcessor, '/jwks')

if __name__ == '__main__':
    app.run()  # run our Flask app

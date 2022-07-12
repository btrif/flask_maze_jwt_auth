#  Created by btrif Trif on 03-07-2022 , 10:09 PM.

from flask_restx import Api, Resource, fields
from models import app, db, Users, Mazes
from routes import *


# Create the Api
api = Api(app, version='1.0', title='Mazes with User authentication API',
          description='Mazes with User Authentication using JWT Token',
          )

# Namespace
ns = api.namespace('mazes', description='MAZES operations')

#
# users_model = api.model('Users',
#                         {
#                             'id': fields.Integer(readonly=True, description='The User unique identifier'),
#                             'name': fields.String(required=True, description='The user name'),
#                             'public_id': fields.String(required=True, description='The public identifier '),
#                             'password': fields.String(required=True, description='The password')
#                         }
#                         )
#




if __name__ == '__main__':
    app.run(debug=True, port=5009, use_reloader=True)
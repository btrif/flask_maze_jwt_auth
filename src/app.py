#  Created by btrif Trif on 03-07-2022 , 10:09 PM.

from apispec_webframeworks.flask import FlaskPlugin
from models import app, db, Users, Mazes
from routes import *
from apispec import APISpec
from marshmallow import Schema


@app.route('/api')
def get_api():
    hello_dict = {'en': 'Hello', 'es': 'Hola'}
    lang = request.args.get('lang')
    # return 'works temprarily'
    return jsonify(hello_dict['es'])

# @app.route('/api/docs')
# def get_docs():
#     print('sending docs')
#     return render_template('/templates/swagger-ui.html')
#     return render_template('swaggerui.html')

class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


if __name__ == '__main__':
    app.run(debug=True, port=5009, use_reloader=True)
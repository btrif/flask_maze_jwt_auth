#  Created by btrif Trif on 04-07-2022 , 10:47 PM.
import string

from flask import request, render_template, json, jsonify, make_response
from src.models import app, Users, db, Mazes, MazeSchema, check_only_one_exit

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from src.auth import token_required
from marshmallow import fields, validate, ValidationError
from src.tools import MazeGrid

##      ROUTES      ##

class UserApi:
    @app.route('/register', methods=['POST'])
    def signup_user():
        print(f'request :  {request}       is_json :  {request.is_json}  ')
        data = request.get_json()
        print(f'data : {data}')
        print(f'password : { data["password"] }')
        hashed_password = generate_password_hash(data['password'], method='sha256')

        existing_user = Users.query.filter_by(name=data['name'])
        if existing_user.count() > 0 :
            return {'status' : 'error' , 'message' : 'There is already an existing user with that name' }
        else :
            new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'registered successfully'})


    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = Users.query.all()
        result = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password

            result.append(user_data)
        return jsonify({'users': result})


    @app.route('/login', methods=['POST'])
    def login_user():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'Authentication': 'login required"'})

        user = Users.query.filter_by(name=auth.username).first()
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() +
                                                                      datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], "HS256")

            return jsonify({'status' : "success", 'token' : token})

        return make_response('could not verify',  401, {'Authentication': '"login required"'})



@app.route('/hello')
def hello():
    import os
    import subprocess
    login = os.getlogin()
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    time = datetime.datetime.now().strftime("%H:%M")
    processor = str(subprocess.check_output(["wmic", "cpu", "get", "name"]).strip()).split('\\n')[1]

    return f'Hello <b>' + str(login) +'</b><br> Today is : <b><p style="color:blue;">'  + str(date) + ' </b></p>' \
              ' and the time is : <p style="color:magenta;"> <b>'+ str(time) +'</b></p><b>  ' + str(processor)



@app.route('/maze', methods=['POST'])
@token_required
def create_maze(current_user):

    '''     Example input Postman: json Format :
                {
            "entrance":  "A1",
            "gridSize": "8x8",
            "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6", "E6", "G6", "H6", "B7", "D7", "G7", "B8"]
            }

    '''

    data = request.get_json()
    print(data)

    gridSize = request.json['gridSize']
    entrance = request.json['entrance']
    walls = request.json['walls']
    maze_config = {"gridSize": gridSize, "entrance": entrance,  "walls": walls }


    print(f'gridSize : {gridSize}')
    print(f'entrance : {entrance}')
    print(f'walls : {walls}')

    # Validate the data from request before serialization :
    error_maze = MazeSchema().validate( data = maze_config )
    if error_maze :
        return jsonify(error_maze)

    # Check that Entrance Column is not bigger than the gridSize column index :
    entrance_col, gridSize_col = entrance[:1], int(gridSize.split('x')[1])
    chars = string.ascii_uppercase[:gridSize_col]
    if entrance_col not in chars :
        return {'status' : 'error', 'message': 'The entrance letter should fit the number of columns' }

    # Check that entrance is always first row
    if entrance[1:] != "1" :
        return {'status' : 'error', 'message': 'The entrance should always be the first row. Example: A1, B1, C1 ' }

    # Check only one exit
    if not check_only_one_exit(gridSize, walls) :
        return {'status' : 'error', 'message': 'Please assure that you have only one single exit in the last row. Add more walls.' }


    # We limit the minimum walls, because we don't want to slow solution:
    rows, cols = gridSize.split('x')
    if  len(walls) < int(rows)*int(cols) //3 :
        more_walls = int(rows)*int(cols) // 3 - len(walls)
        return {'status' : 'error', 'message': f'Please add at least another {more_walls} walls' }

    try :
        solutions = MazeGrid(maze_config)
    except IndexError :
        return {'status' : 'error', 'message': f'You added a wall which is just outside the grid space. Please check and correct your walls input.' }

    # Solve the grid at INPUT from the user, if there is at least one solution
    try :
        min_sol = solutions.get_min_or_max_path('min')
        max_sol = solutions.get_min_or_max_path('max')
    except ValueError :
        return {'status' : 'error', 'message': f'There is no solution for this configuration. Please delete walls. '
                                               f'Verify that you have at least one valid exit.' }

    new_maze = Mazes(
                            gridSize = gridSize,
                            entrance = entrance,
                            walls = str(walls),
                            user_id=current_user.id,
                            min_solution = str(min_sol),
                            max_solution = str(max_sol)
                                )
    print(f"new maze : {new_maze}")

    # We 've added this for the return result
    try:
        json_input = request.get_json()
        print(f'json_input = {json_input}')
        result = MazeSchema().load(json_input)

    except ValidationError as err:
        return {"errors": err.messages}, 422

    db.session.add(new_maze)
    db.session.flush()
    result["id"] = new_maze.id
    db.session.commit()
    return result, 201



@app.route('/maze/<int:maze_id>/solution', methods=['GET', 'POST'])
@token_required
def get_maze(current_user, maze_id):                    #                  http://127.0.0.1:5009/maze/10/solution?steps=min
    print(f"my request : {request.args.to_dict()}")

    maze = Mazes.query.filter_by(id=maze_id, user_id=current_user.id).first()
    if maze :
        print(f'maze:  {type(maze)}         {maze}     ')

        steps = request.args.get('steps')
        print(f"steps :  {steps}")
        if steps == 'min':
            solution = maze.min_solution
            print(f"solution : {solution}")
            return {'status': 'success', 'path': solution }
        elif steps == 'max':
            solution = maze.max_solution
            print(f"solution : {solution}")
            return {'status': 'success', 'path': solution }

        else :
            return {'status': 'error', 'message': f"You typed : {steps}    steps must be either min or max. "}

        return {'status' : 'success' , 'message' : str(maze) }
    else :
        return {'status': 'error', 'message': f'There is no maze with id {maze_id} for user {current_user.name}.'}



@app.route('/hi/<string:name>')
def hi(name):
    return f'Hello ' + str(name)
#  Created by btrif Trif on 04-07-2022 , 10:43 PM.
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, post_load, ValidationError, validate
from flask_marshmallow import Marshmallow
import string

####        The definition of our application       ####
# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY']='dc095a097e37eed90ce22499fbd3ac42'                 # Generate it with :    uuid.uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mazes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Create the DB conn
db = SQLAlchemy(app)


ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"< id : {self.id},  name : {self.name},  password : {self.password},  " \
               f"public_id : {self.public_id} > "


class Mazes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False )
    gridSize = db.Column(db.String(7), nullable=False)
    entrance = db.Column(db.String(5), nullable=False)
    walls = db.Column(db.Text(512), nullable=False)
    min_solution = db.Column(db.Text(512), default=None)
    max_solution = db.Column(db.Text(512), default=None)

    def __repr__(self):
        return f"< id : {self.id},  user_id : {self.user_id},  gridSize : {self.gridSize},  " \
               f"entrance : {self.entrance}, walls : {self.walls}  " \
               f"min_solution : {self.min_solution}  max_solution : {self.max_solution} > "



def validate_grid(grid_size):
    ''' method to validate grid'''
    # 33x33
    import re
    pattern = re.compile("[0-9]{1,2}x[0-9]{1,2}")
    match_data = re.match(pattern, grid_size)
    if match_data.group() != grid_size :
        raise ValidationError("ValidationError : Please provide maze gridSize on the form {Int}x{Int}. With Max Int=99.  Example : 9x9")



def validate_entrance(entrance):
    # A1, B1, C1 or Z1
    import re
    pattern = re.compile("[A-Z]1")
    match_data = re.match(pattern, entrance)
    if match_data :
        # print(f'YEs, we have MATCH DATA :   { match_data.group() } { type(match_data.group() )}')
        if match_data.group() != entrance :
            raise ValidationError("ValidationError : Please provide Entrance of the form A1, B1, C1,... Max Int is the max column from Grid Size ")
    else :
        raise ValidationError("ValidationError : Please provide Entrance of the form A1, B1,... Max Int is the max column from Grid Size")



class WallsSchema(Schema):
    walls = fields.List(fields.String(validate=validate.Length(min=1)))


class MazeSchema(Schema):
    gridSize = fields.String(required=True, allow_none=False , validate=validate_grid)
    if gridSize :
        entrance = fields.String(required=True, allow_none=False, validate=validate_entrance )
    walls = fields.List(fields.String(validate = validate.Length(min=1)), required=True, validate = validate.Length(min=1) )

    class Meta:
        fields = ("gridSize", "entrance", "walls")

    def get_grid_columns(self, gridSize):
        col = str(gridSize).split('x')[1]
        return int(col)


def check_only_one_exit(gridSize, walls):
    last_row, last_col = gridSize.split('x')
    cols = string.ascii_uppercase[:int(last_col)]
    all_last_cols = { letter+last_row for letter in cols }
    # print(f"all-last_cols    =   {all_last_cols}")
    one_exit = all_last_cols - set(walls)
    # print(f'Only one exit :    {one_exit}' )
    if len(one_exit) <= 1 : return True
    return False







if __name__ == '__main__':
    gridSize = "9x8"
    walls = ["C1", "G1", "A2", "C2", "E2", "G2", "E3", "B4", "E4", "G4", "D5", "E5", "H5",
              "D6", "H6", "B6", "D7", "G7", "H2", "A9", "B9", "D9", "E9", "F9", "G9", "H9"]

    print(  check_only_one_exit(gridSize, walls)  )



from venv import create
from app import app, get_db, api, db
from flask import json, jsonify, request
from app.form import RegisterForm
from flask_restx import Api, Resource
from app.models import User
from app.__init__ import userReg_model, jwt, userLogin_model
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


@api.route('/eyecu')
class LandingPage(Resource):
    def get(self):
        return {"hello":"world"}
     
    
#--------REGISTRATION CODE --------------------------------#
@api.route('/register')
class register(Resource):
    #Reference
    #https://www.youtube.com/watch?v=GXVvBU_Vynk&ab_channel=SsaliJonathan
    
    # '''
    # this function saves a new account entry to database
    # '''
    
    '''Test with postman'''
    #@api.marshal_with(userReg_model)
    '''Test with postman END'''
    
    @api.expect(userReg_model)
    def post(self):
        #grabs json from frontend
        data = request.get_json()
        
        #validate username is new and not taken
        username = data.get('username')
        #query through SQLAlchemy ORM
        #queries table User for an existing username
        db_user = User.query.filter_by(username = username).first()
        if db_user is not None:
            return jsonify({"message":f"{username} already taken. Please try again"})
        
        #appends data
        new_user = User(
            username = data.get('username'),
            password = generate_password_hash(data.get('password')),
            firstName = data.get('firstName'),
            lastName = data.get('lastName')
        )
        #commits to db
        new_user.save()
        return jsonify({"message":"User created successfully!"})
#--------REGISTRATION CODE END--------------------------------#
    
    
#--------LOGIN CODE --------------------------------#
#JWT Auth
@api.route('/login')
class login(Resource):
    #Reference
    #https://www.youtube.com/watch?v=GXVvBU_Vynk&ab_channel=SsaliJonathan
    
    
    @api.expect(userLogin_model)
    def post(self):
        
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')    
        
        db_user = User.query.filter_by(username = username).first()
        
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            return jsonify(
                {"access token": access_token,
                 "refresh token": refresh_token
                 }
            )
#--------LOGIN CODE END--------------------------------#    
    
    
    
    
'''
BELOW ARE TESTS DONE WITH DIRECT SQL QUERIES 
NOT SQLALCHEMY
'''

# #test
# @app.route('/home')
# def home():
#     return jsonify(hello = "world",
#                    status = 200,
#                    mimetype = 'application/json') #returns json associated with this route
    
    
# #test
# @app.route('/accounts')
# def viewAcc():
#     db = get_db()
#     statement = f"SELECT * FROM users"
#     cursor = db.execute(statement)
#     results = cursor.fetchall()
#     return jsonify(results)
#     #return jsonify([tuple(row) for row in results])
#     #return f"<h1>username: {results[0]['username']}"

# #--------REGISTRATION CODE --------------------------------#
# #TODO:
# '''something with POST AND GET for front end.
#     figure out how to pass data to and from REACT.'''

# @app.route('/register', methods = ['POST', 'GET'])
# def register():
#     regForm = RegisterForm()
    
#     #CLI FOR TESTING
#     #remove when connected to FRONTEND
#     username = input('username: ')
#     password = input('password: ')
#     firstName = input('firstName: ')
#     lastName = input('lastName: ')
    
    
#     #connects and gets db access
#     db = get_db()  
#     #prepares statement for SQL execution                                 
#     statement = f"SELECT username FROM users WHERE username = '{username}'"
#     cursor = db.execute(statement)
#     #checks for existing username so only fetch 1 occurance
#     results = cursor.fetchone()
#     if results:
#         print('username has been taken')
#         return f"<h1> username taken </h1>"
#     else:
#         if not results:
#             #insert into table
#             db.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?,?,?,?)',
#                        (username, password, firstName, lastName))
#             db.commit()
#             db.close()
#             print('account registered')
#             return f"<h1> account made </h1>"
    
# #---------REGISTRATION CODE END--------------------------------$    
            
    
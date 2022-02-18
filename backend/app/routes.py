from app import webapp, get_db, api, db
from flask import json, jsonify, request
from app.form import RegisterForm
from flask_restx import Api, Resource
from app.model.Account import Account
from app.database import session
from app.services.AccountServices import AccountServices
from app.__init__ import jwt, userReg_model, userLogin_model
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity
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
    
    # '''Test with postman'''
    #@api.marshal_with(userReg_model)
    # '''Test with postman END'''
    
    @api.expect(userReg_model)
    def post(self):
        #grabs json from frontend
        data = request.get_json()
        
        
        #unload json to variables
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        #queries table User for an existing username
        db_user = session.query(Account).filter_by(username = username).first()
        if db_user is not None:
            return jsonify({
                "error": 400,
                "message": f"{username} already taken. Please try again"
            })
        
        #appends data if no issues#
        AccountServices.createAcc(username, password, email)
        
        #communicate with frontend
        access_token = create_access_token(identity=username)
        return jsonify(
                {"token": access_token}
        )
        # #validate username is new and not taken
        # username = data.get('username')
        # #query through SQLAlchemy ORM
        # #queries table User for an existing username
        # db_user = Account.query.filter_by(username = username).first()
        # if db_user is not None:
        #     return jsonify({"message":f"{username} already taken. Please try again"})
        
        # #appends data
        # new_user = User(
        #     username = data.get('username'),
        #     password = generate_password_hash(data.get('password')),
        #     firstName = data.get('firstName'),
        #     lastName = data.get('lastName')
        # )
        # #commits to db
        # new_user.save()
        
        # #communicate with frontend
        # access_token = create_access_token(identity=username)
        # return jsonify(
        #         {"token": access_token}
        #     )
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
        
        db_user = session.query(Account).filter_by(username = username).first()
        
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            return jsonify(
                {"access token": access_token}
            )
        else:
            return jsonify({"message": "Wrong Credentials. No account associated.",
                            "error": 400})
#--------LOGIN CODE END--------------------------------#    
    
    
    
    
#-------- DASH CODE BEGIN -----------------------------#
'''
test to protect paths from non logged in visits.
'''
@api.route("/dash")
class dashboard(Resource):
    
    
    #this function is protected.
    @jwt_required()
    def get(self):
        #gets current user by mapping jwt token to username
        currUser = get_jwt_identity()
        return jsonify({"Logged In": currUser})
    
#-------- DASH CODE END -----------------------------#        
        

 
        
        
        
#-------- SERVO CONTROL CODE BEGIN -----------------------------#   
'''
param: string
pass "OPEN" to initiate OPEN SERVO logic
pass "CLOSE" to initiate CLOSE SERVO logic
'''          
@api.route("/dash/<string:func>")
class lockFunction(Resource):
    @jwt_required()
    def post(self, func):
        if func == 'OPEN':
            return jsonify({"operation" : "OPEN",
                        "success": "TRUE"})
        elif func == 'CLOSE':
            return jsonify({"operation" : "CLOSE",
                        "success": "TRUE"})
        else:
            return jsonify({"error": "unable to control servo"})
        
        
        
#-------- SERVO CONTROL CODE BEGIN -----------------------------#           
  
        
import os
from app import webapp, get_db, api, db
from flask import json, jsonify, request, send_from_directory, Response
from app.model.Faces import Faces
from flask_restx import Api, Resource
from app.model.Account import Account
from app.database import session
from app.services.AccountServices import AccountServices
from app.services.FaceServices import FaceServices
from app.__init__ import jwt, userReg_model, userLogin_model, userFace_model
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import asyncio

#response for invalid data or errors
def user_error_to_json(error_message):
    return Response(json.dumps(error_message), status=400, mimetype='application/json')


#response for successful GETs
def positiveReponse(message): # this takes in a dictionary and makes it into a positive json 
    return Response(json.dumps(message), status=200, mimetype='application/json')

#response for successful POSTs
def createdResponse(message):
    return Response(json.dumps(message), status=201, mimetype='application/json')


@api.route('/eyecu')
class LandingPage(Resource):
    def get(self):
        return {"hello":"world"}
     
    
#--------REGISTRATION CODE --------------------------------#
@api.route('/signup')
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
            return user_error_to_json({"general":f"{username} Already Taken. Please Try Again."})
        
        #appends data if no issues#
        AccountServices.createAcc(username, password, email)
        
        #communicate with frontend
        access_token = create_access_token(identity=username)
        return createdResponse({"token": access_token})

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
            return createdResponse({"token": access_token})
        else:
            return user_error_to_json({"general":"Wrong Credentials. Please Try Again."})
        
    
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
        
#------- UPLOAD FACE CODE BEGIN -------#

# Asynchronous function to validate face to not stall server
# Uploads Face and returns appropriate response
@api.expect(userFace_model)
@asyncio.coroutine
async def async_upload_face(self):
    pic = request.files["image"]
        
    if not pic:
        return user_error_to_json({"general": "No File Uploaded."})
      
    filename = secure_filename(pic.filename)
    
    #Async Call to Validate
    valid = await FaceServices.validate_picture(pic)

    if valid == 1:
        face_name = request.form.get("data")
        mimetype = pic.mimetype
        curr_user = get_jwt_identity()
        userObj = session.query(Account).filter_by(username = curr_user).first()

        #Async Call to Store Face
        await FaceServices.init_face(pic, filename, face_name, mimetype, userObj.id)
        return createdResponse({"general": "Face Is Recognized and Saved."})
    elif valid > 1:
        return user_error_to_json({"general": "Too Many Faces Detected. Please Show 1 Face."})
    elif valid == 0:
        return user_error_to_json({"general": "No Faces Detected. Please Show 1 Face."})


@api.route("/dash/register_face")
class registerFace(Resource):
    
    '''
    Creates coroutine to run concurrently 
    goal: not stall server while running validation and storing
    '''
    @jwt_required()
    @api.expect(userFace_model)
    def post(self):
        
        '''
        dunno if need these statements
        '''
        #asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        
        response = asyncio.run(async_upload_face(self))
        response.close()
        #loop.close()
        return response
       
#------- UPLOAD FACE CODE END -------#
 
 
 
#------- RETURN FACE CODE BEGIN -------# 
'''
THIS SEGMENT IS FOR TESTING PURPOSES. 
'''
@api.route("/get_face/<int:id>")
class getFace(Resource):
    
    
    '''
    SO FAR, ONLY RETURNS 1 PICTURE AT A TIME.
    FOR EFFICIENCY, SHOULD BE ABLE TO RETURN ALL FACES REGISTERED UNDER AN ACCOUNT.
    '''
    def get(self, id):
        #img_file = session.query(Faces).filter_by(user_id = id).first()
        img_file = "0c7a8f34ab739850.jpg"
        
       # print(img_file.picture_file)
        print(os.path.join(webapp.root_path, 'model\\faces'))
        return send_from_directory(os.path.join(webapp.root_path, "model\\faces"), img_file)
        
    
#------- RETURN FACE CODE END -------# 
        
        
        
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
  
        
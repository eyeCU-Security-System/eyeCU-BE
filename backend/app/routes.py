import os
from app import webapp, get_db, api, db
from flask import json, jsonify, render_template, request, send_from_directory, Response, make_response
from app.model.Faces import Faces
from flask_restx import Api, Resource
from app.model.Account import Account
from app.database import session
from app.services.AccountServices import AccountServices
from app.services.FaceServices import FaceServices
#from app.services.Processing import Processing
from app.__init__ import jwt, userReg_model, userLogin_model, userFace_model
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import asyncio
import threading
import socketio
from flask_socketio import SocketIO


#--------STATUS RESPONSES CODE BEGIN----------------------------#

#response for invalid data or errors
def user_error_to_json(error_message):
    return Response(json.dumps(error_message), status=400, mimetype='application/json')


#response for successful GETs
def positiveReponse(message): # this takes in a dictionary and makes it into a positive json 
    return Response(json.dumps(message), status=200, mimetype='application/json')

#response for successful POSTs
def createdResponse(message):
    return Response(json.dumps(message), status=201, mimetype='application/json')

#--------STATUS RESPONSES CODE END----------------------------#




#--------VIDEO RENDERING CODE TEST BEGIN----------------------------#
@api.route("/video")
class video(Resource):
    def get(self):
        return make_response(render_template("video.html"),200)
#--------VIDEO RENDERING CODE TEST END----------------------------#     





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
@api.route("/get_face")
class getFace(Resource):
    def get(self):
    #     img_file = session.query(Faces).first()
        
    #     print(img_file.face_name)
    # #     print(os.path.join(webapp.root_path, 'model\\faces_img'))
    #     return send_from_directory(os.path.join(webapp.root_path, "model\\faces_img"), img_file.picture_file)
        # img_obj = Processing.pull_faces()
        # print(len(img_obj))

        img_file = "fafe4d2d6fc11837.jpg"  
        print("landed")



    
#------- RETURN FACE CODE END -------# 
        
        
        
#-------- SERVO CONTROL CODE BEGIN -----------------------------#
'''
param: string
pass "OPEN" to initiate OPEN SERVO logic
pass "CLOSE" to initiate CLOSE SERVO logic
'''          
@api.route("/status/open")
class lockFunction(Resource):
    @jwt_required()
    def post(self):
        pass
        
        
#-------- SERVO CONTROL CODE BEGIN -----------------------------#           
  


#-------- FR PROCESSING AND STREAMING CODE BEGIN ---------------#
#-------- FR PROCESSING AND STREAMING CODE END ---------------#




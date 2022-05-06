import os
from app import webapp, api
from flask import json, jsonify, render_template, request, send_from_directory, Response, make_response
from app.model.Faces import Faces
from flask_restx import Api, Resource
from app.model.Account import Account
from app.database import session
from app.services.AccountServices import AccountServices
from app.services.FaceServices import FaceServices
#from app.services.Processing import Processing
from app.__init__ import jwt, userReg_model, userLogin_model, userFace_model, socketio
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import asyncio
import threading
from flask_socketio import SocketIO
from app.services.Processing import rpi_address, feed_receiver, get_ack
import base64
import cv2
import requests
import face_recognition
import numpy as np


# def start_vid():
#     global stop_run
#     t = threading.Thread(target=feed_receiver(stop_run))
#     t.daemon = True
#     t.start()
#     return

#--------STATUS RESPONSES CODE BEGIN----------------------------#

#response for invalid data or errors
def user_error_to_json(error_message):
    return Response(json.dumps(error_message), status=400, mimetype='application/json')


#response for successful GETs
def positiveResponse(message): # this takes in a dictionary and makes it into a positive json 
    return Response(json.dumps(message), status=200, mimetype='application/json')

#response for successful POSTs
def createdResponse(message):
    return Response(json.dumps(message), status=201, mimetype='application/json')



#--------STATUS RESPONSES CODE END----------------------------#


#--------REGISTRATION CODE --------------------------------#
@api.route('/signup')
class register(Resource):
    #Reference
    #https://www.youtube.com/watch?v=GXVvBU_Vynk&ab_channel=SsaliJonathan
    
    # '''
    # this function saves a new account entry to database
    # '''
    
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
            t = threading.Thread(target=feed_receiver)
            t.daemon = True
            t.start()
            return createdResponse({"token": access_token})
        else:
            return user_error_to_json({"general":"Wrong Credentials. Please Try Again."})
        
    
#--------LOGIN CODE END--------------------------------#   

     
        
#------- UPLOAD FACE CODE BEGIN -------#

# Asynchronous function to validate face to not stall server
# Uploads Face and returns appropriate response
@api.expect(userFace_model)
@asyncio.coroutine
async def async_upload_face(self):
    pic = request.files["file"]
    if not pic:
        return user_error_to_json({"general": "No File Uploaded."})
      
    filename = secure_filename(pic.filename)
    #Async Call to Validate
    print("validating... ")

    valid = await FaceServices.validate_picture(pic)

    print("validating done")
    if valid == 1:
        curr_user = get_jwt_identity()
        mimetype = pic.mimetype
        userObj = session.query(Account).filter_by(username = curr_user).first()
        face_name = userObj.username
        user_id = userObj.id
        #Async Call to Store Face
        await FaceServices.init_face(pic, filename, face_name, mimetype, user_id)
        print("storing...")
        return createdResponse({"general": "Face Is Recognized and Saved."})
    elif valid > 1:
        return user_error_to_json({"general": "Too Many Faces Detected. Please Show 1 Face."})
    elif valid == 0:
        return user_error_to_json({"general": "No Faces Detected. Please Show 1 Face."})


@api.route("/upload")
class registerFace(Resource):
    '''
    Creates coroutine to run concurrently 
    goal: not stall server while running validation and storing
    '''
    @jwt_required()
    @api.expect(userFace_model)
    def post(self):
        response = asyncio.run(async_upload_face(self))
        response.close()
        return response
       
#------- UPLOAD FACE CODE END -------#
 
 
 
#------- USER DASH CODE BEGIN -------# 
'''
RETURNS USER INFO FOR PROFILE PAGE
'''
@api.route("/user")
class getUser(Resource):
    @jwt_required()
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity() # this tells us the identity of the user/ This should be the primary key
        user_data = {}
        user_obj = session.query(Account).filter_by(username = current_user).first()
        file = session.query(Faces).filter_by(user_id = user_obj.id).first()
        if(file):
            filename = file.picture_file
            path = os.path.join(webapp.root_path, 'model/faces_img', filename)
            frame = cv2.imread(path)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            small_frame_bytes = cv2.imencode('.jpg', small_frame)[1].tobytes()
            sender = base64.encodebytes(small_frame_bytes).decode("utf-8")
        else:
            filename = "default.jpeg"
            path = os.path.join(webapp.root_path, 'model/faces_img', filename)
            frame = cv2.imread(path)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            small_frame_bytes = cv2.imencode('.jpg', small_frame)[1].tobytes()
            sender = base64.encodebytes(small_frame_bytes).decode("utf-8")

        user_data["user_data"] = {
            "full_name":current_user,
            'image':"data:image/jpeg;base64,{}".format(sender)
        }
        return positiveResponse(user_data)
    
#------- USER DASH CODE END -------# 
        
        
        
#-------- SERVO CONTROL CODE BEGIN -----------------------------#
'''
param: string

pass "OPEN" to initiate OPEN SERVO logic
pass "CLOSE" to initiate CLOSE SERVO logic
'''          
@api.route("/status/open")
class unlockFunction(Resource):
    def post(self):
        face_ack = get_ack()
        #print("hitting unlock post face_ack: ", face_ack)
        if face_ack == True:
            requests.post(rpi_address + ":5002/open")
            return positiveResponse({"general": "Open Success."})
        else:
            return user_error_to_json({"general": "No Face Detected. Unoperable."})

@api.route("/status/close")
class lockFunction(Resource):
    def post(self):
        requests.post(rpi_address + ":5002/close")
        return 
    
          
#-------- SERVO CONTROL CODE BEGIN -----------------------------#           
  




#-------- FR PROCESSING AND STREAMING CODE BEGIN ---------------#
# @socketio.on('connect', namespace='/web')
# def connect_web():
#     print('[INFO] Web client connected: {}'.format(request.sid))


# @socketio.on('disconnect', namespace='/web')
# def disconnect_web():
#     print('[INFO] Web client disconnected: {}'.format(request.sid))

#-------- FR PROCESSING AND STREAMING CODE END ---------------#
# @api.route("/faces")
# class getFaces(Resource):
#     @jwt_required()
#     def get(self):
#         global known_face_encodings, known_face_names
#         known_face_encodings = []
#         known_face_names = []
#     #---- PROCESS FACES ---------------#
#         curr_user = get_jwt_identity()
#         #print(curr_user)
#         user = session.query(Account).filter_by(username = curr_user).first()
#         entries = session.query(Faces).filter_by(user_id = user.id).first()
#         #entries = session.query(Faces).all()
#         if entries:
#             # for row in entries:
#             filename = entries.picture_file
#             name = entries.face_name
#             face_image = face_recognition.load_image_file('./app/model/faces_img/' + filename)
#             pic_encoding = face_recognition.face_encodings(face_image)[0]
#             known_face_encodings = [pic_encoding]
#             known_face_names = [name]
#     #---- PROCESS FACES ---------------#
#         else:
#             return [],[]
#         return known_face_encodings, known_face_names

# @api.route("/stop")
# class vidStop(Resource):
#     def get(self):
#         global stop_run
#         stop_run = True
#         return


# @api.route("/run")
# class vidRun(Resource):
#     def get(self):
#         global stop_run
#         stop_run = False
#         start_vid()
#         return
    

# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/ 
# LOOK INTO KILLING CHILD THREAD TO UPLOAD FACE
# AND THEN RESTART VIDEO THREAD 
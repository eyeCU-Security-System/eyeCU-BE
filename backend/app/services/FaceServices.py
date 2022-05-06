import json
import os
import secrets
from app.model.Faces import Faces
from app.model.Account import Account
from app.database import session
from flask import jsonify
from app import webapp
import face_recognition
import asyncio

def save_picture(pic_obj, pic_fn): #creates hash for profile pic file
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic_fn)
    picture_fn= random_hex + f_ext
    picture_path = os.path.join(webapp.root_path, 'model/faces_img', picture_fn)
    pic_obj.seek(0)
    pic_obj.save(picture_path)
    return picture_fn



# Functions are running Asynchronously
class FaceServices():
    
    async def init_face(pic,file, name, mimetype, user_id):
        
        new_face = Faces(
            picture_file = save_picture(pic,file),
            face_name = name,
            mimetype = mimetype,
            user_id = user_id
        ) 
        session.add(new_face)
        session.commit()
        return jsonify({"message":"Picture Uploaded"})
        
    async def validate_picture(pic):
        print("inside validate ")
        test_image = face_recognition.load_image_file(pic)
        print("got pics ")
        try:
            face_locations = face_recognition.face_locations(test_image)
        except:
            print("cant grab faces")
        print("found faces...")
        print("encoding faces.. ")
        face_encodings = face_recognition.face_encodings(test_image, face_locations)
        print("face encoded...")
        return len(face_encodings)

    def return_all_faces():
        #returns all the faces within db
        img_file = session.query(Faces).first()
        return img_file



        

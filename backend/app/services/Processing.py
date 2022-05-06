from flask_socketio import SocketIO
from flask import Flask, render_template, request, send_from_directory
from sqlalchemy import false
from app import socketio
import pickle
import face_recognition
import cv2
import numpy as np
import base64
from os.path import exists
import http3
import threading
from flask import Response
from flask import Flask
import argparse
import os
import time
from time import sleep
from .FaceServices import FaceServices
from app import webapp
from app.model.Faces import Faces
import asyncio
from app.database import session
import requests

device_state = "CLOSE"
open_timestamp = None
CLOSE_AFTER = 3
face_ack = True
stop = False


def convert_byte_to_mat(byte):
    nparr = np.frombuffer(byte, np.byte)
    img2 = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    return img2

def convert_mat_to_byte(mat):
    frame = cv2.imencode('.jpg', mat)[1].tobytes()
    return frame


@socketio.on('connect', namespace='/web')
def connect_web():
    global stop
    print('[INFO] Processing.py Web client connected: {}'.format(request.sid))
    if stop == True:
        print("restarting camera thread...")
        t = threading.Thread(target=feed_receiver)
        t.daemon = True
        t.start()


@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    global stop
    print('[INFO] Processing.py Web client disconnected: {}'.format(request.sid))
    stop = True
    



outputFrame = None
lock = threading.Lock()

rpi_address = "http://192.168.1.13"
#rpi_address = "http://10.0.0.136"
# Hardcode raspberry pi streaming url for dev purpose. Move
# this to environment variable when used in production
cam = rpi_address + ":9090/stream/video.jpeg"

# Use cv2.CAP_ANY for auto select
# TODO: uncomment this for prod
cap = cv2.VideoCapture(cam, cv2.CAP_ANY)


if not cap:
    print("!!! Failed VideoCapture: invalid parameter!")


def get_ack():
    return face_ack

def feed_receiver():
    global outputFrame, device_state, open_timestamp, CLOSE_AFTER, face_ack, stop
    face_ack = False
    known_face_encodings = []
    known_face_names = []
#---- PROCESS FACES ---------------#
    entries = session.query(Faces).all()
    for row in entries:
        filename = row.picture_file
        name = row.face_name
        face_image = face_recognition.load_image_file('./app/model/faces_img/' + filename)
        pic_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings = [pic_encoding]
        known_face_names = [name]
#---- PROCESS FACES ---------------#
    stop = False
    while not stop:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if type(frame) == type(None):
            print("!!! Couldn't read frame!")
            break
        
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
        

            if len(known_face_encodings) > 0:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_ack = True
        
                else:
                    face_ack = False
    
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom + 10), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 1, bottom + 6), font, 0.35, (255, 255, 255), 1)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        frame = base64.encodebytes(frame).decode("utf-8")
        socketio.emit('server2web', {'image':"data:image/jpeg;base64,{}".format(frame)}, namespace='/web')

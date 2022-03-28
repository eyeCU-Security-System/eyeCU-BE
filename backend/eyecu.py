#kept in separate file to avoid tempering
from app import webapp
from app import manager
import threading
#from app import feed_receiver
from flask_socketio import SocketIO
from app import socketio
from app.services.Processing import feed_receiver
from flask import request




"""
ANY CHANGES TO DB LIKE: ADDING NEW COLUMN TO TABLE OR ADDING NEW TABLES:
COMMENT OUT APP.RUN, run the manager.run() below.
then run these commands in the shell:

--NO NEED TO RUN THIS COMMAND UNLESS STARTING OVER ENTIRE DB---
python .\eyecu.py db init ( do this once) 
------------------------------

--RUN THESE-------
python .\eyecu.py db migrate
python .\eyecu.py db upgrade
---------
ONCE RAN, COMMENT OUT manager.run() AND 
RUN APP.RUN LIKE USUAL
"""

#run application
if __name__=='__main__':
    #manager.run()

    #train all faces in db
    #proccess_faces = Processing()
   # proccess_faces.pull_and_train_faces()

    # Run RP feed proccessor in a sub thread
    t = threading.Thread(target=feed_receiver())
    t.daemon = True
    t.start()

    #webapp.run(debug = True, port = 5001)

    #intended to shoot feed
    print('[INFO] Starting server at http://localhost:5001')
    socketio.run(app = webapp, host = "localhost", port = 5001)
    
    




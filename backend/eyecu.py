#kept in separate file to avoid tempering
from app import webapp
from app import manager
import threading
#from app import feed_receiver
from flask_socketio import SocketIO
from app.__init__ import socketio
from app import socketio
from app.services.Processing import feed_receiver
from flask import request
import sys
import asyncio
from multiprocessing import Process, Lock


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
    #webapp.run(debug = True, port = 5001)
    

    #Run RP feed proccessor in a sub thread
    # stop_threads = False
    # t = threading.Thread(target=feed_receiver, args = (lambda : stop_threads, ))
    # t.daemon = True
    # t.start()


    # p = Process(target=feed_receiver)
    # p.start()

    # t = threading.Thread(target=feed_receiver)
    # t.daemon = True
    # t.start()
    

    #intended to shoot feed
    #print('[INFO] Starting server at http://localhost:5001')
    socketio.run(app=webapp,host = '0.0.0.0',port=5001)
    
    




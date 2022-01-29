#kept in separate file to avoid tempering
from app import app
from app import manager


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
    app.run(debug = True)

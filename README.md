----CRUCIAL----:
Removed venv from git due to size. PLEASE CREATE THE VENV AND INSTALL LIBRARIES EVERY PULL
1. cd to root directory
2. pip install virtualenv
3. WINDOWS: python -m virtualenv venv
you should now see a folder called venv pop up in root dir.



BEFORE ANY CHANGES TO BACKEND CODE OR TO START BACKEND
1. open terminal
2. cd to root project directory
3. run venv: ' .\venv\scripts\activate '
4. run: ' pip install -r requirements.txt '
THIS INSTALLS ALL NEEDED LIBRARIES/DEPENDANCIES FOR THIS PROJECT

PLEASE UPDATE requirements.txt BEFORE ANY PUSH TO GIT
1. in terminal with venv running
2. ensure path is to root directory not in backend folder
3. run: ' pip freeze > requirements.txt '




"""
ANY CHANGES TO DB LIKE: ADDING NEW COLUMN TO TABLE OR ADDING NEW TABLES:
COMMENT OUT APP.RUN, run the manager.run() below.
then run these commands in the shell:

--NO NEED TO RUN THIS COMMAND UNLESS STARTING OVER ENTIRE DB BY DELETING EXISTING FILE---

python .\eyecu.py db init ( do this once) 


--RUN THESE IN TERMINAL-------
1. python .\eyecu.py db migrate
2. python .\eyecu.py db upgrade
---------
ONCE RAN, COMMENT OUT manager.run() AND 
RUN APP.RUN LIKE USUAL
"""


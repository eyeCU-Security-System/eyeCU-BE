BEFORE ANY CHANGES TO BACKEND CODE OR TO START BACKEND
1. open terminal
2. cd to project directory and into backend folder
3. run venv: ' .\venv\scripts\activate '
4. run: ' pip install -r requirements.txt '
THIS INSTALLS ALL NEEDED LIBRARIES/DEPENDANCIES FOR THIS PROJECT

PLEASE UPDATE requirements.txt BEFORE ANY PUSH TO GIT
1. in terminal with venv running
2. run: ' pip freeze > requirements.txt '



BEFORE ANY CHANGES TO DATABASE
1. make sure (venv) is present
2. cd to database directory
3. run: 'sqlite3 eyecu.db; ' to enter schema and sql terminal

OR TO EXECUTE SQL SCRIPTS 
1. cd to backend\database
2. make script edits to schema.sql
3. run: 'sqlite3 eyecu.db ".read schema.sql" '


START FRONT END
1. cd to frontend folder
2. in terminal : ' npm start '


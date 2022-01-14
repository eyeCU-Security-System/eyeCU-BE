from app import app, get_db
from flask import json, jsonify
from app.form import RegisterForm





@app.route('/')
def landing():
    return '<h1> Hello World </h1>'


#test
@app.route('/home')
def home():
    return jsonify(hello = "world",
                   status = 200,
                   mimetype = 'application/json') #returns json associated with this route
    
    
#test
@app.route('/accounts')
def viewAcc():
    db = get_db()
    cursor = db.execute('SELECT username FROM users')
    results = cursor.fetchall()
    return f"<h1>username: {results[0]['username']}"

#--------REGISTRATION CODE --------------------------------#
#TODO:
'''something with POST AND GET for front end.
    figure out how to pass data to and from REACT.'''

@app.route('/register', methods = ['POST', 'GET'])
def register():
    regForm = RegisterForm()
    
    #CLI FOR TESTING
    #remove when connected to FRONTEND
    username = input('username: ')
    password = input('password: ')
    firstName = input('firstName: ')
    lastName = input('lastName: ')
    
    
    #connects and gets db access
    db = get_db()  
    #prepares statement for SQL execution                                 
    statement = f"SELECT username FROM users WHERE username = '{username}'"
    cursor = db.execute(statement)
    #checks for existing username so only fetch 1 occurance
    results = cursor.fetchone()
    if results:
        print('username has been taken')
        return f"<h1> username taken </h1>"
    else:
        if not results:
            #insert into table
            db.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?,?,?,?)',
                       (username, password, firstName, lastName))
            db.commit()
            db.close()
            print('account registered')
            return f"<h1> account made </h1>"
    
#---------REGISTRATION CODE END--------------------------------$    
            
    
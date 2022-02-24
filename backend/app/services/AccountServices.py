import json
from app.model.Account import Account
from app.database import session
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required
from flask import jsonify

class AccountServices():
    
    def createAcc(username, password, email):
        #ISSUE:
        #only appends data, doesnt return json
        
        
        #queries table User for an existing username 
        # db_user = session.query(Account).filter_by(username = username).first()
        # if db_user is not None:
        #     return jsonify({
        #         "error": 400,
        #         "message": f"{username} already taken. Please try again"
        #     })
                  
        #appends data
        new_user = Account(
            username = username,
            password = generate_password_hash(password),
            email = email,
        )
        #commits to db
        session.add(new_user)  # Add the user
        session.commit()  # Commit the change
        
        # #communicate with frontend
        # access_token = create_access_token(identity=username)
        # return jsonify(
        #         {"token": access_token,
        #          "status" : 200}
        # )



    #------ NOT TESTED YET -------#
    def delete(username):
        #queries table User for an existing username
        db_user = session.query(Account).filter_by(username = username).first()
        if db_user is None:
            return {
                "error": 400,
                "message": f"{username} Not found"
            }
    
        #commits to db
        session.delete(db_user)  # Add the user
        session.commit()  # Commit the change


        return {
            "message": "deleted"
        }
     #------ NOT TESTED YET -------#


     #------ NOT TESTED YET -------#
    def update(username, password, email):
        #queries table User for an existing username
        db_user = session.query(Account).filter_by(username = username).first()
        if db_user is None:
            return {
                "error": 400,
                "message": f"{username} Not found"
            }
    
        #appends data  
        db_user.password = generate_password_hash(password)
        db_user.email = email

        #commits to db
        session.commit()  # Commit the change


        return {
            db_user
        }
     #------ NOT TESTED YET -------#
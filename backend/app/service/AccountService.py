from app.model.Account import Account
from app.database import session
from werkzeug.security import generate_password_hash

def create(username, password, email, phone):
    #queries table User for an existing username
    db_user = session.query(Account).filter_by(username = username).first()
    if db_user is not None:
        return {
            "error": 400,
            "message": f"{username} already taken. Please try again"
        }
    
    #appends data
    new_user = Account(
        username = username,
        password = generate_password_hash(password),
        email = email,
        phone = phone
    )

    #commits to db
    session.add(new_user)  # Add the user
    session.commit()  # Commit the change


    return {
        new_user
    }

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

def update(username, password, email, phone):
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
    db_user.phone = phone

    #commits to db
    session.commit()  # Commit the change


    return {
        db_user
    }

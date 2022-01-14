#kept in separate file to avoid tempering
from app import app

#run application
if __name__=='__main__':
    app.run(debug = True)

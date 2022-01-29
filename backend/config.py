import os
baseDirectory = os.path.abspath(os.path.dirname(__file__))

#locate database to be in same working __file__
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'vnkdjnfjknfl1232#'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(baseDirectory, 'eyecu.db') #locates database

    SQLALCHEMY_TRACK_MODIFICATIONS= False #logs any changes

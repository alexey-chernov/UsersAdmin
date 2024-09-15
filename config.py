import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usersadmin:usersadmin@10.66.66.1/users_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_ECHO = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
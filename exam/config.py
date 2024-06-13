
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://std_2572_exam:123456789@std-mysql.ist.mospolytech.ru/std_2572_exam'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'covers')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


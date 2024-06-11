import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'b3baa1cb519a5651c472d1afa1b3f4e04f1adf6909dae88a4cd39adc0ddd9732'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2572_exam:123456789@std-mysql.ist.mospolytech.ru/std_2572_exam'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



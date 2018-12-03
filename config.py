import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'imtracerustupidbitch'
    DEBUG = os.environ.get('DEBUG') or 'TRUE'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:shuttle@localhost:5432/PoetTone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

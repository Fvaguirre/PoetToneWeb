import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'imtracerustupidbitch'
    DEBUG = os.environ.get('DEBUG') or 'TRUE'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:shuttle@localhost:5432/PoetTone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['fvaguirre@gmail.com']
    POEMS_PER_PAGE = 6

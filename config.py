import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mircoblog-secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_POST') or 25)
    MAIL_USE_TSL = os.environ.get('MAIL_USE_TSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['marwanali2428@gmail.com']

    POSTS_PER_PAGE = 25

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

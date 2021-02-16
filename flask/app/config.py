import os
from os import getenv
from dotenv import load_dotenv
from aiopg.sa import create_engine

load_dotenv()

API_V1_URL_PREFIX = '/api/v1/'


class Config(object):
    BASE_PATH = os.path.dirname(__file__).rstrip('/app')
    SERVER_NAME = 'localhost'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{getenv("DB_USER")}:{getenv("DB_PWD")}@localhost:5432/{getenv("DB_NAME")}'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    AIOPG_ENGINE = create_engine(user=getenv('DB_USER'),
                                 database=getenv('DB_NAME'),
                                 host='127.0.0.1',
                                 password=getenv('DB_PWD'))
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 465
    ADMIN_EMAIL_LOGIN = getenv('ADMIN_EMAIL_LOGIN')
    ADMIN_EMAIL_PWD = getenv('ADMIN_EMAIL_PWD')

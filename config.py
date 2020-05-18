import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MYSQL_DATABASE_HOST = os.environ.get('STACKS_MYSQL_HOST')
    MYSQL_USER = os.environ.get('STACKS_MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('STACKS_MYSQL_ROOT_PASSWORD')
    MYSQL_DB = 'stacks'
    MYSQL_PORT = os.environ.get('STACKS_MYSQL_PORT')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_DATABASE_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

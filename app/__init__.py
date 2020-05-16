from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')
migrate = Migrate(app, db)

from app import routes
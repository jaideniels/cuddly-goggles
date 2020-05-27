from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
marsh = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)

from app import routes  # noqa: E402 F401

api.register_blueprint(routes.blp)

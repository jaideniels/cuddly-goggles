from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
from flask_smorest import Api
import os

from config import Config, ProductionConfig

app = Flask(__name__)

if os.environ['FLASK_ENV'] == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(Config)

auth = HTTPTokenAuth(scheme='Bearer')
db = SQLAlchemy(app)
marsh = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)

tokens = {
    os.environ['STACKS_USER_TOKEN_1']: "jaydan",
    os.environ['STACKS_USER_TOKEN_2']: "jessie"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

from app import routes  # noqa: E402 F401

api.register_blueprint(routes.admin_blp)
api.register_blueprint(routes.stacks_blp)
api.register_blueprint(routes.cards_blp)
api.register_blueprint(routes.scores_blp)

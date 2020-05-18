from app import app, db
from .models import Something
from config import Config

@app.route('/')
def index():
    return db.session.query(Something).first().data

@app.route('/createdb/')
def create():
    db.create_all()
    return "created!"

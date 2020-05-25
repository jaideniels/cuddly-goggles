from app import app, db
from .models import Something


@app.route('/')
def index():
    return db.session.query(Something).first().data + '\n'


@app.route('/createdb/')
def create():
    db.create_all()
    return "created!"

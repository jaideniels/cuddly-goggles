from app import app, db
from .models import Something, User, Stack, UserStack

@app.route('/')
def index():
    return db.session.query(Something).first().data + '\n'


@app.route('/createdb/')
def create():
    db.create_all()
    return "created!"


@app.route('/recreatedb/')
def recreate():
    db.drop_all()
    db.create_all()

    # dummy table records
    something = Something(data="hi jay!")
    db.session.add(something)

    # stacks data
    user = User(name="jay")
    stack = Stack(name="colors")
    userstack = UserStack()
    userstack.stack = stack
    userstack.user = user
    db.session.add(userstack)

    # commit the changes
    db.session.commit()
    return "created!"

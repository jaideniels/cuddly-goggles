from app import app, db
import ptvsd

ptvsd.enable_attach(address=('0.0.0.0', 5678))

@app.route('/')
def index():
    return '<h1>stacks!</h1>'

from app import app, db

@app.route('/')
def index():
    return '<h1>stacks!</h1>'

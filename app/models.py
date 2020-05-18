from app import db

class Something(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(128))

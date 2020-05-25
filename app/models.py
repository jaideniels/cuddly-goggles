from app import db


class Something(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(128))


class UserStack(db.Model):
    __tablename__ = 'user_stack'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), primary_key=True)

    user = db.relationship("User", back_populates="stacks")
    stack = db.relationship("Stack", back_populates="users")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    stacks = db.relationship("UserStack", back_populates="user")


class Stack(db.Model):
    __tablename__ = 'stack'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    users = db.relationship("UserStack", back_populates="stack")

from app import db
from sqlalchemy.ext.associationproxy import association_proxy


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    stacks = association_proxy('user_stacks', 'stack',  creator=lambda stack: UserStack(stack=stack))

    def __init__(self, name):
        self.name = name


class Stack(db.Model):
    __tablename__ = 'stack'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    users = association_proxy('stack_users', 'user', creator=lambda user: UserStack(user=user))
    cards = association_proxy("stack_cards", 'card', creator=lambda card: StackCard(card=card))

    def __init__(self, name):
        self.name = name


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    stacks = association_proxy("card_stacks", 'stack', creator=lambda stack: StackCard(stack=stack))

    def __init__(self, name):
        self.name = name


class UserStack(db.Model):
    __tablename__ = 'user_stack'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), primary_key=True)

    user = db.relationship(User,  backref=db.backref("user_stacks", cascade="all, delete-orphan"))
    stack = db.relationship(Stack, backref=db.backref("stack_users", cascade="all, delete-orphan"))

    def __init__(self, user=None, stack=None):
        self.user = user
        self.stack = stack


class StackCard(db.Model):
    __tablename__ = 'stack_card'
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

    stack = db.relationship(Stack, backref=db.backref("stack_cards", cascade="all, delete-orphan"))
    card = db.relationship(Card, backref=db.backref("card_stacks", cascade="all, delete-orphan"))

    def __init__(self, stack=None, card=None):
        self.stack = stack
        self.card = card

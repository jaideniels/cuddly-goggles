from app import db
from sqlalchemy.ext.associationproxy import association_proxy


class User(db.Model):
    __tablename__ = 'user'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(128), unique=True)

    # Relationship
    stacks = association_proxy('user_stacks', 'stack',  creator=lambda stack: UserStack(stack=stack))
    scores = db.relationship('Score', back_populates='user')

    def __init__(self, name):
        self.name = name


class Stack(db.Model):
    __tablename__ = 'stack'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(128))

    # Reliationships
    users = association_proxy('stack_users', 'user', creator=lambda user: UserStack(user=user))
    cards = association_proxy('stack_cards', 'card', creator=lambda card: StackCard(card=card))

    def __init__(self, name):
        self.name = name


class Card(db.Model):
    __tablename__ = 'card'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(128))

    # Relationships
    stacks = association_proxy('card_stacks', 'stack', creator=lambda stack: StackCard(stack=stack))
    clues = db.relationship('Clue', back_populates='card')
    facts = db.relationship('Fact', back_populates='card')

    def __init__(self, name):
        self.name = name


class Fact(db.Model):
    __tablename__ = 'fact'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))

    # Columns
    fact = db.Column(db.String(128))

    # Relationships
    card = db.relationship('Card', back_populates='facts')
    clues = association_proxy('fact_clues', 'clue', creator=lambda clue: ClueFact(clue=clue))

    def __init__(self, fact):
        self.fact = fact


class Clue(db.Model):
    __tablename__ = 'clue'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))

    # Relationships
    card = db.relationship('Card', back_populates='clues')
    scores = db.relationship('Score', back_populates='clue')
    facts = association_proxy('clue_facts', 'fact', creator=lambda fact: ClueFact(fact=fact))

    def __init__(self, facts):
        for fact in facts:
            self.facts.append(fact)


class Game(db.Model):
    __tablename__ = 'game'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(128))

    # Relationships
    scores = db.relationship('Score', back_populates='game')


class Score(db.Model):
    __tablename__ = 'score'

    # Primary Keys
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clue_id = db.Column(db.Integer, db.ForeignKey('clue.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    # Columns
    score = db.Column(db.Integer)

    # Relationships
    user = db.relationship('User', back_populates='scores')
    clue = db.relationship('Clue', back_populates='scores')
    game = db.relationship('Game', back_populates='scores')

    def __init__(self, score, user=None, clue=None, game=None):
        self.score = score
        self.user = user
        self.clue = clue
        self.game = game


class UserStack(db.Model):
    __tablename__ = 'user_stack'

    # Primary Keys / Foriegn Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), primary_key=True)

    # Relationships
    user = db.relationship('User',  backref=db.backref('user_stacks', cascade='all, delete-orphan'))
    stack = db.relationship('Stack', backref=db.backref('stack_users', cascade='all, delete-orphan'))

    def __init__(self, user=None, stack=None):
        self.user = user
        self.stack = stack


class StackCard(db.Model):
    __tablename__ = 'stack_card'

    # Primary Keys / Foreign Keys
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

    # Relationships
    stack = db.relationship('Stack', backref=db.backref('stack_cards', cascade='all, delete-orphan'))
    card = db.relationship('Card', backref=db.backref('card_stacks', cascade='all, delete-orphan'))

    def __init__(self, stack=None, card=None):
        self.stack = stack
        self.card = card


class ClueFact(db.Model):
    __tablename__ = 'clue_fact'

    # Primary Keys / Foreign Keys
    clue_id = db.Column(db.Integer, db.ForeignKey('clue.id'), primary_key=True)
    fact_id = db.Column(db.Integer, db.ForeignKey('fact.id'), primary_key=True)

    # Relaiionships
    clue = db.relationship('Clue', backref=db.backref('clue_facts', cascade='all, delete-orphan'))
    fact = db.relationship('Fact', backref=db.backref('fact_clues', cascade='all, delete-orphan'))

    def __init__(self, clue=None, fact=None):
        self.clue = clue
        self.fact = fact

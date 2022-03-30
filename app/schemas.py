from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from .models import User, Stack, Card, Clue, Fact, Score
from app import db


class FactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fact
        include_relationship = False
        load_instance = True
        sqla_session = db.session
        #dump_only = ('id')


class ClueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Clue
        include_relationship = False
        load_instance = True
        sqla_session = db.session
        dump_only = ('id')

    facts = fields.Nested(FactSchema, many=True)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True
        sqla_session = db.session
        dump_only = ('id')

class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        ordered = True
        model = Card
        include_relationships = True
        load_instance = True
        sqla_session = db.session
        #dump_only = ('id', 'clues')

    facts = fields.Nested(FactSchema, many=True)
    clues = fields.Nested(ClueSchema, many=True)

class StackSchema(SQLAlchemyAutoSchema): 
    class Meta:
        model = Stack
        include_relationships = False
        load_instance = True
        sqla_session = db.session
        dump_only = ('id')

    cards = fields.Nested(CardSchema, many=True)

class ScoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        include_relationships = True
        load_instance = True
        sqla_session = db.session

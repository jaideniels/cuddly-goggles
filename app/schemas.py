from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from .models import User, Stack, Card, Clue, Fact


class FactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fact
        include_relationship = False
        load_instance = True


class ClueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Clue
        include_relationship = False
        load_instance = True

    facts = fields.Nested(FactSchema, many=True)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True


class StackSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Stack
        include_relationships = False
        load_instance = True


class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        include_relationships = False
        load_instance = True

    facts = fields.Nested(FactSchema, many=True)
    clues = fields.Nested(ClueSchema, many=True)

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User, Stack, Card


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

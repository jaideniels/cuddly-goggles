from flask_smorest import Blueprint
from flask.views import MethodView

from app import db
from .models import User, Stack, Card
from .schemas import UserSchema, StackSchema, CardSchema


blp = Blueprint('root', __name__, url_prefix='/v1')


@blp.route('/users/<user_id>')
class UserById(MethodView):

    @blp.response(UserSchema)
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        return user


@blp.route('/stacks/<stack_id>')
class StackById(MethodView):

    @blp.response(StackSchema)
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        return stack


@blp.route('/stacks/<stack_id>/cards')
class CardsByStackById(MethodView):

    @blp.response(CardSchema(many=True))
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        cards = stack.cards
        return cards


@blp.route('/users/<user_id>/stacks')
class StacksByUserById(MethodView):

    @blp.response(StackSchema(many=True))
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        stacks = user.stacks
        return stacks


@blp.route('/recreatedb/')
def recreate():
    db.drop_all()
    db.create_all()

    # user and stack data
    user = User("jaydan")
    stack = Stack("colors")
    user.stacks.append(stack)
    db.session.add(user)
    db.session.add(stack)

    # card data
    red_card = Card(name="red")
    red_card.stacks.append(stack)
    db.session.add(red_card)

    blue_card = Card(name="blue")
    blue_card.stacks.append(stack)
    db.session.add(blue_card)

    orange_card = Card(name="orange")
    orange_card.stacks.append(stack)
    db.session.add(orange_card)

    # commit the changes
    db.session.commit()
    return "created!"

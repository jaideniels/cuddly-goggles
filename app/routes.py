from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request

from app import db
from .models import User, Stack, Card, Fact, Clue, Game, Score
from .schemas import UserSchema, StackSchema, CardSchema, ScoreSchema


admin_blp = Blueprint('admin', __name__, url_prefix='/v1')
stacks_blp = Blueprint('stacks', __name__, url_prefix="/v1")
cards_blp = Blueprint('cards', __name__, url_prefix="/v1")
scores_blp = Blueprint('scores', __name__, url_prefix="/v1")


@admin_blp.route('/users/')
class Users(MethodView):

    @admin_blp.response(200, UserSchema(many=True))
    def get(self):
        users = User.query.all()
        return users

    @admin_blp.arguments(UserSchema)
    @admin_blp.response(201, UserSchema)
    def post(self, user):
        db.session.add(user)
        db.session.commit()
        return user


@admin_blp.route('/users/<user_id>')
class UserById(MethodView):

    @admin_blp.response(200, UserSchema)
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        return user


@stacks_blp.route('/stacks/')
class Stacks(MethodView):

    @stacks_blp.response(200, StackSchema(many=True))
    def get(self):
        stacks = Stack.query.all()
        return stacks

    @stacks_blp.arguments(StackSchema)
    @stacks_blp.response(201, StackSchema)
    def post(self, stack):
        db.session.add(stack)
        db.session.commit()
        return stack


@stacks_blp.route('/stacks/<stack_id>')
class StackById(MethodView):

    @stacks_blp.response(200, StackSchema)
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        return stack


@cards_blp.route('/cards/')
class Cards(MethodView):

    @cards_blp.response(200, CardSchema(many=True))
    def get(self):
        cards = Card.query.all()
        return cards

    @cards_blp.response(201, CardSchema)
    def post(self):
        json = request.get_json()
        card = Card(name=json['name'])

        for json_fact in json['facts']:
            json_fact_value = json_fact['fact']
            fact = Fact(json_fact_value)
            card.facts.append(fact)
            clue = Clue([fact])
            card.clues.append(clue)

        db.session.add(card)
        db.session.commit()
        return card


@cards_blp.route('/stacks/<stack_id>/cards')
class CardsByStackById(MethodView):

    @cards_blp.response(200, CardSchema(many=True))
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        cards = stack.cards
        return cards


@stacks_blp.route('/users/<user_id>/stacks')
class StacksByUserById(MethodView):

    @stacks_blp.response(200, StackSchema(many=True))
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        stacks = user.stacks
        return stacks


@scores_blp.route('/scores')
class Scores(MethodView):

    @scores_blp.arguments(ScoreSchema)
    @scores_blp.response(201, ScoreSchema)
    def post(self, score):
        db.session.add(score)
        db.session.commit()
        return score


@scores_blp.route('/users/<user_id>/scores')
class ScoresByUserId(MethodView):

    @scores_blp.response(200, ScoreSchema(many=True))
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        scores = user.scores
        return scores


@admin_blp.route('/recreatedb/')
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

    # facts
    english_red_fact = Fact("red")
    zhongwen_red_fact = Fact("红")
    hanyu_red_fact = Fact("hóng")

    english_blue_fact = Fact("blue")
    zhongwen_blue_fact = Fact("蓝")
    hanyu_blue_fact = Fact("lán")

    english_orange_fact = Fact("orange")
    zhongwen_orange_fact = Fact("橙")
    hanyu_orange_fact = Fact("chéng")

    # clues
    english_red_clue = Clue([english_red_fact])
    zhongwen_red_clue = Clue([zhongwen_red_fact])
    hanyu_red_clue = Clue([hanyu_red_fact])

    english_blue_clue = Clue([english_blue_fact])
    zhongwen_blue_clue = Clue([zhongwen_blue_fact])
    hanyu_blue_clue = Clue([hanyu_blue_fact])

    english_orange_clue = Clue([english_orange_fact])
    zhongwen_orange_clue = Clue([zhongwen_orange_fact])
    hanyu_orange_clue = Clue([hanyu_orange_fact])

    # card data
    red_card.clues.append(english_red_clue)
    red_card.clues.append(zhongwen_red_clue)
    red_card.clues.append(hanyu_red_clue)
    red_card.facts.append(english_red_fact)
    red_card.facts.append(zhongwen_red_fact)
    red_card.facts.append(hanyu_red_fact)

    blue_card.clues.append(english_blue_clue)
    blue_card.clues.append(zhongwen_blue_clue)
    blue_card.clues.append(hanyu_blue_clue)
    blue_card.facts.append(english_blue_fact)
    blue_card.facts.append(zhongwen_blue_fact)
    blue_card.facts.append(hanyu_blue_fact)

    orange_card.clues.append(english_orange_clue)
    orange_card.clues.append(zhongwen_orange_clue)
    orange_card.clues.append(hanyu_orange_clue)
    orange_card.facts.append(english_orange_fact)
    orange_card.facts.append(zhongwen_orange_fact)
    orange_card.facts.append(hanyu_orange_fact)

    # game
    game = Game('learn')
    db.session.add(game)

    # scores
    english_red_score = Score(5, user=user, clue=english_red_clue, game=game)
    zhongwen_red_score = Score(5, user=user, clue=zhongwen_red_clue, game=game)
    hanyu_red_score = Score(5, user=user, clue=hanyu_red_clue, game=game)

    db.session.add(english_red_score)
    db.session.add(zhongwen_red_score)
    db.session.add(hanyu_red_score)

    # commit the changes
    db.session.commit()
    return "created!"

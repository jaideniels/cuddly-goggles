from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request

from app import db, auth
from .models import User, Stack, Card, Fact, Clue, Game, Score, UserStack
from .schemas import UserSchema, StackSchema, CardSchema, ScoreSchema


admin_blp = Blueprint('admin', __name__, url_prefix='/v1')
stacks_blp = Blueprint('stacks', __name__, url_prefix="/v1")
cards_blp = Blueprint('cards', __name__, url_prefix="/v1")
scores_blp = Blueprint('scores', __name__, url_prefix="/v1")


@admin_blp.route('/users/')
class Users(MethodView):

    @admin_blp.response(200, UserSchema(many=True))
    @auth.login_required
    def get(self):
        users = User.query.all()
        return users

    @admin_blp.arguments(UserSchema)
    @admin_blp.response(201, UserSchema)
    @auth.login_required
    def post(self, user):
        db.session.add(user)
        db.session.commit()
        return user


@admin_blp.route('/users/<user_id>')
class UserById(MethodView):

    @admin_blp.response(200, UserSchema)
    @auth.login_required
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        return user


@stacks_blp.route('/stacks/')
class Stacks(MethodView):

    @stacks_blp.response(200, StackSchema(many=True))
    @auth.login_required
    def get(self):
        user = db.session.query(User).filter(User.name == auth.current_user()).one()
        print(user.name)
        stacks = db.session.query(Stack).\
            filter(Stack.users.any(User.id == user.id))

        return stacks

    @stacks_blp.arguments(StackSchema)
    @stacks_blp.response(201, StackSchema)
    @auth.login_required
    def post(self, stack):
        user = db.session.query(User).filter(User.name == auth.current_user()).one()
        user.stacks.append(stack)
        db.session.commit()
        return stack


@stacks_blp.route('/stacks/<stack_id>')
class StackById(MethodView):

    @stacks_blp.response(200, StackSchema)
    @auth.login_required
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        return stack


@cards_blp.route('/cards/')
class Cards(MethodView):

    @cards_blp.response(201, CardSchema)
    @auth.login_required
    def post(self):
        # delete this - can't add orphaned cards
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
    @auth.login_required
    def get(self, stack_id):
        stack = db.session.query(Stack).get_or_404(stack_id)
        cards = stack.cards
        return cards

    @auth.login_required
    @stacks_blp.arguments(CardSchema)
    @stacks_blp.response(200, CardSchema)
    def post(self, card, stack_id):
        print("stack_id: " + stack_id)

        user = db.session.query(User).filter(User.name == auth.current_user()).one()
        # TODO: confirm user is actually allowed to do this

        stack = db.session.query(Stack).filter(Stack.id == stack_id).one()

        json = request.get_json()
        card = Card(name=json['name'])

        for json_fact in json['facts']:
            json_fact_value = json_fact['fact']
            print("json_fact_value: " + json_fact_value)
            fact = Fact(fact=json_fact_value)
            card.facts.append(fact)
            clue = Clue(facts=[fact])
            card.clues.append(clue)

        stack.cards.append(card)

        db.session.commit()
        return card



@scores_blp.route('/scores')
class Scores(MethodView):

    @scores_blp.arguments(ScoreSchema)
    @scores_blp.response(201, ScoreSchema)
    @auth.login_required
    def post(self, score):
        db.session.add(score)
        db.session.commit()
        return score


@scores_blp.route('/users/<user_id>/scores')
class ScoresByUserId(MethodView):

    @scores_blp.response(200, ScoreSchema(many=True))
    @auth.login_required
    def get(self, user_id):
        user = db.session.query(User).get_or_404(user_id)
        scores = user.scores
        return scores


@admin_blp.route('/recreatedb/')
@auth.login_required
def recreate():
    db.drop_all()
    db.create_all()

    # user and stack data
    user = User(name="jaydan")
    stack = Stack(name="colors")
    user.stacks.append(stack)
    db.session.add(user)
    db.session.add(stack)

    # card data
    red_card = Card(name="红")
    red_card.stacks.append(stack)
    db.session.add(red_card)

    blue_card = Card(name="蓝")
    blue_card.stacks.append(stack)
    db.session.add(blue_card)

    orange_card = Card(name="橙")
    orange_card.stacks.append(stack)
    db.session.add(orange_card)

    # facts
    zhongwen_red_fact = Fact(fact="红")
    english_red_fact = Fact(fact="red")
    hanyu_red_fact = Fact(fact="hóng")

    zhongwen_blue_fact = Fact(fact="蓝")
    english_blue_fact = Fact(fact="blue")
    hanyu_blue_fact = Fact(fact="lán")

    zhongwen_orange_fact = Fact(fact="橙")
    english_orange_fact = Fact(fact="orange")
    hanyu_orange_fact = Fact(fact="chéng")

    # clues
    zhongwen_red_clue = Clue(facts=[zhongwen_red_fact])
    english_red_clue = Clue(facts=[english_red_fact])
    hanyu_red_clue = Clue(facts=[hanyu_red_fact])

    zhongwen_blue_clue = Clue(facts=[zhongwen_blue_fact])
    english_blue_clue = Clue(facts=[english_blue_fact])
    hanyu_blue_clue = Clue(facts=[hanyu_blue_fact])

    zhongwen_orange_clue = Clue(facts=[zhongwen_orange_fact])
    english_orange_clue = Clue(facts=[english_orange_fact])
    hanyu_orange_clue = Clue(facts=[hanyu_orange_fact])

    # card data
    red_card.clues.append(zhongwen_red_clue)
    red_card.clues.append(english_red_clue)
    red_card.clues.append(hanyu_red_clue)
    red_card.facts.append(english_red_fact)
    red_card.facts.append(zhongwen_red_fact)
    red_card.facts.append(hanyu_red_fact)

    blue_card.clues.append(zhongwen_blue_clue)
    blue_card.clues.append(english_blue_clue)
    blue_card.clues.append(hanyu_blue_clue)
    blue_card.facts.append(english_blue_fact)
    blue_card.facts.append(zhongwen_blue_fact)
    blue_card.facts.append(hanyu_blue_fact)

    orange_card.clues.append(zhongwen_orange_clue)
    orange_card.clues.append(english_orange_clue)
    orange_card.clues.append(hanyu_orange_clue)
    orange_card.facts.append(english_orange_fact)
    orange_card.facts.append(zhongwen_orange_fact)
    orange_card.facts.append(hanyu_orange_fact)

    #hangul stack
    hangul_stack = Stack(name="hangul")
    user.stacks.append(hangul_stack)
    db.session.add(hangul_stack)

    #hangul cards
    gk_card = Card(name="ㄱ")
    hangul_stack.cards.append(gk_card)
    db.session.add(gk_card)

    n_card = Card(name="ㄴ")
    hangul_stack.cards.append(n_card)
    db.session.add(n_card)

    d_card = Card(name="ㄷ")
    hangul_stack.cards.append(d_card)
    db.session.add(d_card)

    rl_card = Card(name="ㄹ")
    hangul_stack.cards.append(rl_card)
    db.session.add(rl_card)

    m_card = Card(name="ㅁ")
    hangul_stack.cards.append(m_card)
    db.session.add(m_card)

    # hangul facts
    hangul_gk_fact = Fact(fact="ㄱ")
    english_gk_fact = Fact(fact="g/k")

    hangul_n_fact = Fact(fact="ㄴ")
    english_n_fact = Fact(fact="n")

    hangul_d_fact = Fact(fact="ㄷ")
    english_d_fact = Fact(fact="d")

    hangul_rl_fact = Fact(fact="ㄹ")
    english_rl_fact = Fact(fact="r/l")

    hangul_m_fact = Fact(fact="ㅁ")
    english_m_fact = Fact(fact="m")

    # clues
    hangul_gk_clue = Clue(facts=[hangul_gk_fact])
    english_gk_clue = Clue(facts=[english_gk_fact])

    hangul_n_clue = Clue(facts=[hangul_n_fact])
    english_n_clue = Clue(facts=[english_n_fact])

    hangul_d_clue = Clue(facts=[hangul_d_fact])
    english_d_clue = Clue(facts=[english_d_fact])

    hangul_rl_clue = Clue(facts=[hangul_rl_fact])
    english_rl_clue = Clue(facts=[english_rl_fact])

    hangul_m_clue = Clue(facts=[hangul_m_fact])
    english_m_clue = Clue(facts=[english_m_fact])

    # card data
    gk_card.clues.append(hangul_gk_clue)
    gk_card.clues.append(english_gk_clue)
    gk_card.facts.append(hangul_gk_fact)
    gk_card.facts.append(english_gk_fact)

    n_card.clues.append(hangul_n_clue)
    n_card.clues.append(english_n_clue)
    n_card.facts.append(hangul_n_fact)
    n_card.facts.append(english_n_fact)

    d_card.clues.append(hangul_d_clue)
    d_card.clues.append(english_d_clue)
    d_card.facts.append(hangul_d_fact)
    d_card.facts.append(english_d_fact)

    rl_card.clues.append(hangul_rl_clue)
    rl_card.clues.append(english_rl_clue)
    rl_card.facts.append(hangul_rl_fact)
    rl_card.facts.append(english_rl_fact)

    m_card.clues.append(hangul_m_clue)
    m_card.clues.append(english_m_clue)
    m_card.facts.append(hangul_m_fact)
    m_card.facts.append(english_m_fact)

    # game
    game = Game(name='learn')
    db.session.add(game)

    # commit the changes
    db.session.commit()
    return "created!"

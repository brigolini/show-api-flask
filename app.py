from datetime import datetime, timedelta

import jwt
from flask import Flask, jsonify, request
from flask_jwt import jwt_required, JWT
from werkzeug.security import safe_str_cmp

from data import alchemy
from model import show, episode, user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'supersecreto'


@app.before_first_request
def create_tables():
    alchemy.create_all()


@app.route('/', methods=['GET'])
@jwt_required()
def home():
    return "API Funcionando", 200


def authenticate(username, password):
    auth_user = user.UserModel.find_by_name(username)
    if auth_user and safe_str_cmp(auth_user.password.encode('utf-8'), password.encode('utf-8')):
        return auth_user


def identity(payload):
    user_id = payload['identity']
    return user.UserModel.find_by_name(user_id)


jwt = JWT(app, authenticate, identity)


@jwt.jwt_payload_handler
def make_payload(jwt_identity):
    expiration = datetime.now() + timedelta(minutes=1)
    nbf = (datetime.now() + timedelta(seconds=50))
    return {'user_id': jwt_identity.id,
            'user_name': jwt_identity.name,
            'iat':datetime.now(),
            'exp': expiration,
            'nbf' : nbf}



# post /signup data: {username,password}
@app.route('/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    new_user = user.UserModel(name=request_data["username"], password=request_data["password"])
    new_user.save_to_db()


# post /show data: {name :}
@app.route('/show', methods=['POST'])
def create_show():
    request_data = request.get_json()
    new_show = show.ShowModel(request_data['name'])
    new_show.save_to_db()
    result = show.ShowModel.find_by_id(new_show.id)
    return jsonify(result.json())


# get /show/<name> data: {name :}
@app.route('/show/<string:name>')
def get_show(name):
    result = show.ShowModel.find_by_name(name);
    if result:
        return result.json();
    return {'message': 'Série não encontrada'}, 404


# post /show/<name> data: {name :}
@app.route('/show/<string:name>/item', methods=['POST'])
def create_episode_in_show(name):
    request_data = request.get_json()
    parent = show.ShowModel.find_by_name(name)
    if parent:
        new_episode = episode.EpisodeModel(name=request_data['name'], season=request_data['season'], show_id=parent.id)
        new_episode.save_to_db()
        return new_episode.json()
    else:
        return {'message': 'Não existe a série'}, 404

    # pass


#
# #get /show/<name>/item data: {name :}
# @app.route('/show/<string:name>/item')
# def get_item_in_show(name):
#   for show in shows:
#     if show['name'] == name:
#         return jsonify( {'episodes':show['episodes'] } )
#   return jsonify ({'message':'Série não existe'}),401

if __name__ == '__main__':
    from data import alchemy

    alchemy.init_app(app)
    app.run(port=5000, debug=True)

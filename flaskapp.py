from datetime import datetime, timedelta
import os
import uuid
import jwt
import json
import requests
from functools import wraps
from urlparse import parse_qs, parse_qsl
from urllib import urlencode
from flask import Flask, g, send_file, request, redirect, url_for, jsonify, send_from_directory, Response
from requests_oauthlib import OAuth1
from jwt import DecodeError, ExpiredSignature
import sys
from model.user import User
from service.waston import RelationshipExtraction,PersonalityInsights
import tweepy

from py2neo import Graph, Node, Relationship

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
auth = tweepy.OAuthHandler("VGbGua2zcrvAt8q7rFzYcF7Pp", "LC7DxOcHjzaoHH61MjlWwJvkERWhvnNIHKIasvvvDq9i3J8fGf")
auth.set_access_token("273164662-rcIu2uf0crCAolbKpGJETrU9iMc5XhDHjEo2Oupq",
                      "QxjyYfMQlK83GqwxVZmD4AZFIjtVNTbALFmrGLFdfjfjo")

api = tweepy.API(auth)
graph = Graph(
    "https://551293319a25f:2nKvJUg3aU5jNdRuRjGdIKEG5Kf5GoP4tyrI8WQc@neo-551293319a25f-364459c455.do-stories.graphstory.com:7473/db/data")
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

relationshipExtration = RelationshipExtraction(user="de7bcf6d-01d9-4226-932f-b283302af6a2",
                                                            password="orAuI8JJLynS")

personalityInsights = PersonalityInsights(user="0e7de0e3-03bd-457b-846a-e068ffde5e4e", password="dUDa53BTYORi")

def create_token(user):
    payload = {
        'sub': user['id'],
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function


# Routes

@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/api/me')
@login_required
def me():
    user = User().get_user_by_id(graph, g.user_id)
    return jsonify(User().to_json(user))


@app.route('/api/me/update', methods=['PUT'])
@login_required
def update_me():
    user = User().get_user_by_id(graph, g.user_id)
    user["email"] = request.json['email']
    user["display_name"] = request.json['displayName']
    user.push()
    return jsonify(User().to_json(user))


@app.route('/auth/login', methods=['POST'])
def login():
    user = User().get_user_by_email(graph, request.json['email'])
    print(user['password'])
    if not user or not User().check_password(user, request.json['password']):
        response = jsonify(message='Wrong Email or Password')
        response.status_code = 401
        return response
    token = create_token(user)
    return jsonify(token=token)


@app.route('/auth/signup', methods=['POST'])
def signup():
    user = User().save_user(graph, email=request.json['email'], name=request.json['displayName'],
                            password=request.json['password'])

    token = create_token(user)
    return jsonify(token=token)


@app.route('/auth/facebook', methods=['POST'])
def facebook():
    access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.3/me'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': app.config['FACEBOOK_SECRET'],
        'code': request.json['code']
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.get(access_token_url, params=params)
    print r.text
    access_token = dict(parse_qsl(r.text))
    token = json.loads(r.text)
    print(token)
    # Step 2. Retrieve information about the current user.
    r = requests.get(graph_api_url, params=token)
    profile = json.loads(r.text)
    print profile
    # Step 3. (optional) Link accounts.
    if request.headers.get('Authorization'):
        user = graph.find_one("User", "facebook", profile['id'])
        if user:
            response = jsonify(message='There is already a Facebook account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        user = User().get_user_by_id(graph, payload['sub'])
        if not user:
            response = jsonify(message='User not found')
            response.status_code = 400
            return response

        u = Node("User", id=str(uuid.uuid4()), email=profile['email'], facebook=profile['id'],
                 display_name=profile['name'])
        graph.create(u)
        token = create_token(u)
        return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.
    user = graph.find_one("User", "facebook", profile['id'])
    if user:
        token = create_token(user)
        return jsonify(token=token)

    u = Node("User", id=str(uuid.uuid4()), email=profile['email'], facebook=profile['id'], display_name=profile['name'])
    graph.create(u)
    token = create_token(u)
    return jsonify(token=token)


@app.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['GOOGLE_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)
    print profile
    user = graph.find_one("User", "google", profile['sub'])
    if user:
        token = create_token(user)
        return jsonify(token=token)
    u = Node("User", id=str(uuid.uuid4()), email=profile['email'], google=profile['sub'], display_name=profile['name'])

    graph.create(u)
    token = create_token(u)
    return jsonify(token=token)


@app.route('/auth/linkedin', methods=['POST'])
def linkedin():
    access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    people_api_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,email-address)'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=app.config['LINKEDIN_SECRET'],
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    access_token = json.loads(r.text)
    params = dict(oauth2_access_token=access_token['access_token'],
                  format='json')

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, params=params)
    profile = json.loads(r.text)
    print profile
    user = graph.find_one("User", 'linkedin', profile['id'])
    if user:
        token = create_token(user)
        return jsonify(token=token)
    u = Node("User", id=str(uuid.uuid4()), email=profile['emailAddress'], linkedin=profile['id'],
             display_name=profile['lastName'] + " " + profile['firstName'])
    graph.create(u)
    token = create_token(u)
    return jsonify(token=token)


@app.route('/api/v1/getpeople')
def searchUser():
    users = api.search_users(request.args['name'])
    return jsonify({'users': [
        {'name': user.name,
         'description': user.description,
         'profile_image_url': user.profile_image_url,
         'screen_name': user.screen_name
        } for user in users
    ]})


@app.route('/api/v1/interests/<screen_name>')
def parseInterests(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(40)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    relationship = relationshipExtration.extractRelationship(text)
    nodes, edges = relationshipExtration.parseMentions(relationship)

    return jsonify({'nodes': nodes,
                    'edges': edges})

@app.route('/api/v1/personality/<screen_name>')
def getPersonaliy(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(200)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    profile = personalityInsights.getProfile(text)
    nodes, edges = personalityInsights.flattenPortrait(profile["tree"])

    return jsonify({'nodes': nodes,
                    'edges': edges})

@app.route('/api/v1/viz/<screen_name>')
def getViz(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(200)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    profile = personalityInsights.getProfile(text)
    viz = personalityInsights.requestVisualization(profile)
    return viz

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()

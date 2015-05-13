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
from service.waston import RelationshipExtraction, PersonalityInsights
import tweepy
import facebook as fb

from py2neo import Graph, Node, Relationship

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
auth = tweepy.OAuthHandler("VGbGua2zcrvAt8q7rFzYcF7Pp", "LC7DxOcHjzaoHH61MjlWwJvkERWhvnNIHKIasvvvDq9i3J8fGf")
auth.set_access_token("273164662-rcIu2uf0crCAolbKpGJETrU9iMc5XhDHjEo2Oupq",
                      "QxjyYfMQlK83GqwxVZmD4AZFIjtVNTbALFmrGLFdfjfjo")

api = tweepy.API(auth)
graph = Graph("https://551293319a25f:2nKvJUg3aU5jNdRuRjGdIKEG5Kf5GoP4tyrI8WQc@neo-551293319a25f-364459c455.do-stories.graphstory.com:7473/db/data")
#graph = Graph()
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

relationshipExtration = RelationshipExtraction(user="de7bcf6d-01d9-4226-932f-b283302af6a2",
                                               password="orAuI8JJLynS")

personalityInsights = PersonalityInsights(user="0e7de0e3-03bd-457b-846a-e068ffde5e4e", password="dUDa53BTYORi")

profileee = {
    "id": "sbh",
    "source": "*UNKNOWN*",
    "tree": {
        "children": [
            {
                "children": [
                    {
                        "category": "personality",
                        "children": [
                            {
                                "category": "personality",
                                "children": [
                                    {
                                        "category": "personality",
                                        "id": "Adventurousness",
                                        "name": "Adventurousness",
                                        "percentage": 0.7160526489554446,
                                        "sampling_error": 0.10711332800000001
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Artistic interests",
                                        "name": "Artistic interests",
                                        "percentage": 0.3181832458983307,
                                        "sampling_error": 0.20641926400000002
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Emotionality",
                                        "name": "Emotionality",
                                        "percentage": 0.2515172364058379,
                                        "sampling_error": 0.115189568
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Imagination",
                                        "name": "Imagination",
                                        "percentage": 0.8641701428422862,
                                        "sampling_error": 0.145667632
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Intellect",
                                        "name": "Intellect",
                                        "percentage": 0.8908186242106095,
                                        "sampling_error": 0.128763392
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Liberalism",
                                        "name": "Authority-challenging",
                                        "percentage": 0.898454169007272,
                                        "sampling_error": 0.168568352
                                    }
                                ],
                                "id": "Openness",
                                "name": "Openness",
                                "percentage": 0.8507771685899128,
                                "sampling_error": 0.130284112
                            },
                            {
                                "category": "personality",
                                "children": [
                                    {
                                        "category": "personality",
                                        "id": "Achievement striving",
                                        "name": "Achievement striving",
                                        "percentage": 0.6585127054883937,
                                        "sampling_error": 0.13753696
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Cautiousness",
                                        "name": "Cautiousness",
                                        "percentage": 0.8063779039161849,
                                        "sampling_error": 0.160483392
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Dutifulness",
                                        "name": "Dutifulness",
                                        "percentage": 0.3181116384939571,
                                        "sampling_error": 0.206189696
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Orderliness",
                                        "name": "Orderliness",
                                        "percentage": 0.3165304417521884,
                                        "sampling_error": 0.135897936
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Self-discipline",
                                        "name": "Self-discipline",
                                        "percentage": 0.3153744839220475,
                                        "sampling_error": 0.16816399999999998
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Self-efficacy",
                                        "name": "Self-efficacy",
                                        "percentage": 0.7088051511152613,
                                        "sampling_error": 0.175623264
                                    }
                                ],
                                "id": "Conscientiousness",
                                "name": "Conscientiousness",
                                "percentage": 0.5435483133388536,
                                "sampling_error": 0.152381088
                            },
                            {
                                "category": "personality",
                                "children": [
                                    {
                                        "category": "personality",
                                        "id": "Activity level",
                                        "name": "Activity level",
                                        "percentage": 0.35820197882231886,
                                        "sampling_error": 0.216853088
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Assertiveness",
                                        "name": "Assertiveness",
                                        "percentage": 0.2838920867984583,
                                        "sampling_error": 0.208304352
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Cheerfulness",
                                        "name": "Cheerfulness",
                                        "percentage": 0.14455233450895522,
                                        "sampling_error": 0.16188628800000002
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Excitement-seeking",
                                        "name": "Excitement-seeking",
                                        "percentage": 0.17235759199332115,
                                        "sampling_error": 0.161049568
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Friendliness",
                                        "name": "Outgoing",
                                        "percentage": 0.21600564357324195,
                                        "sampling_error": 0.1768172
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Gregariousness",
                                        "name": "Gregariousness",
                                        "percentage": 0.13842598921316177,
                                        "sampling_error": 0.196135264
                                    }
                                ],
                                "id": "Extraversion",
                                "name": "Extraversion",
                                "percentage": 0.23726267395633333,
                                "sampling_error": 0.18413272
                            },
                            {
                                "category": "personality",
                                "children": [
                                    {
                                        "category": "personality",
                                        "id": "Altruism",
                                        "name": "Altruism",
                                        "percentage": 0.2754933265004837,
                                        "sampling_error": 0.202923504
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Cooperation",
                                        "name": "Cooperation",
                                        "percentage": 0.6307012919481465,
                                        "sampling_error": 0.188078544
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Modesty",
                                        "name": "Modesty",
                                        "percentage": 0.22002846111606778,
                                        "sampling_error": 0.195163392
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Morality",
                                        "name": "Uncompromising",
                                        "percentage": 0.29521221940977527,
                                        "sampling_error": 0.17199344
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Sympathy",
                                        "name": "Sympathy",
                                        "percentage": 0.8963908479208201,
                                        "sampling_error": 0.20470824
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Trust",
                                        "name": "Trust",
                                        "percentage": 0.4465068968715436,
                                        "sampling_error": 0.19620072
                                    }
                                ],
                                "id": "Agreeableness",
                                "name": "Agreeableness",
                                "percentage": 0.197592943914049,
                                "sampling_error": 0.17107476800000002
                            },
                            {
                                "category": "personality",
                                "children": [
                                    {
                                        "category": "personality",
                                        "id": "Anger",
                                        "name": "Fiery",
                                        "percentage": 0.46038608777319856,
                                        "sampling_error": 0.107145328
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Anxiety",
                                        "name": "Prone to worry",
                                        "percentage": 0.2925613308885644,
                                        "sampling_error": 0.120479872
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Depression",
                                        "name": "Melancholy",
                                        "percentage": 0.4058642362110278,
                                        "sampling_error": 0.14824848
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Immoderation",
                                        "name": "Immoderation",
                                        "percentage": 0.16728870664411802,
                                        "sampling_error": 0.10801417599999999
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Self-consciousness",
                                        "name": "Self-consciousness",
                                        "percentage": 0.5367949472615889,
                                        "sampling_error": 0.170005808
                                    },
                                    {
                                        "category": "personality",
                                        "id": "Vulnerability",
                                        "name": "Susceptible to stress",
                                        "percentage": 0.41333637268687284,
                                        "sampling_error": 0.123342656
                                    }
                                ],
                                "id": "Neuroticism",
                                "name": "Emotional range",
                                "percentage": 0.4782057339658776,
                                "sampling_error": 0.10990580800000001
                            }
                        ],
                        "id": "Openness_parent",
                        "name": "Openness",
                        "percentage": 0.8507771685899128
                    }
                ],
                "id": "personality",
                "name": "Big 5 "
            },
            {
                "children": [
                    {
                        "category": "needs",
                        "children": [
                            {
                                "category": "needs",
                                "id": "Challenge",
                                "name": "Challenge",
                                "percentage": 0.9454631311618445,
                                "sampling_error": 0.571675504
                            },
                            {
                                "category": "needs",
                                "id": "Closeness",
                                "name": "Closeness",
                                "percentage": 0.37430779536880737,
                                "sampling_error": 0.664986656
                            },
                            {
                                "category": "needs",
                                "id": "Curiosity",
                                "name": "Curiosity",
                                "percentage": 0.8974415472114874,
                                "sampling_error": 0.601831648
                            },
                            {
                                "category": "needs",
                                "id": "Excitement",
                                "name": "Excitement",
                                "percentage": 0.46240646412915437,
                                "sampling_error": 0.597841328
                            },
                            {
                                "category": "needs",
                                "id": "Harmony",
                                "name": "Harmony",
                                "percentage": 0.8769879010128687,
                                "sampling_error": 0.656984848
                            },
                            {
                                "category": "needs",
                                "id": "Ideal",
                                "name": "Ideal",
                                "percentage": 0.06182001068498667,
                                "sampling_error": 0.5687984159999999
                            },
                            {
                                "category": "needs",
                                "id": "Liberty",
                                "name": "Liberty",
                                "percentage": 0.8842968320182879,
                                "sampling_error": 0.5426626720000001
                            },
                            {
                                "category": "needs",
                                "id": "Love",
                                "name": "Love",
                                "percentage": 0.4198132194180422,
                                "sampling_error": 0.695262304
                            },
                            {
                                "category": "needs",
                                "id": "Practicality",
                                "name": "Practicality",
                                "percentage": 0.2510956138665641,
                                "sampling_error": 0.632711856
                            },
                            {
                                "category": "needs",
                                "id": "Self-expression",
                                "name": "Self-expression",
                                "percentage": 0.8612635859116711,
                                "sampling_error": 0.618786896
                            },
                            {
                                "category": "needs",
                                "id": "Stability",
                                "name": "Stability",
                                "percentage": 0.7455088528118455,
                                "sampling_error": 0.6569906719999999
                            },
                            {
                                "category": "needs",
                                "id": "Structure",
                                "name": "Structure",
                                "percentage": 0.9856815998415455,
                                "sampling_error": 0.023924848
                            }
                        ],
                        "id": "Structure_parent",
                        "name": "Structure",
                        "percentage": 0.9856815998415455
                    }
                ],
                "id": "needs",
                "name": "Needs"
            },
            {
                "children": [
                    {
                        "category": "values",
                        "children": [
                            {
                                "category": "values",
                                "id": "Conservation",
                                "name": "Conservation",
                                "percentage": 0.1590310821416115,
                                "sampling_error": 0.228751744
                            },
                            {
                                "category": "values",
                                "id": "Openness to change",
                                "name": "Openness to change",
                                "percentage": 0.5969809255902321,
                                "sampling_error": 0.241299504
                            },
                            {
                                "category": "values",
                                "id": "Hedonism",
                                "name": "Hedonism",
                                "percentage": 0.11680072978737648,
                                "sampling_error": 0.234514768
                            },
                            {
                                "category": "values",
                                "id": "Self-enhancement",
                                "name": "Self-enhancement",
                                "percentage": 0.7972447610009217,
                                "sampling_error": 0.22006544
                            },
                            {
                                "category": "values",
                                "id": "Self-transcendence",
                                "name": "Self-transcendence",
                                "percentage": 0.5762760484207429,
                                "sampling_error": 0.21310896
                            }
                        ],
                        "id": "Hedonism_parent",
                        "name": "Hedonism",
                        "percentage": 0.11680072978737648
                    }
                ],
                "id": "values",
                "name": "Values"
            }
        ],
        "id": "r",
        "name": "root"
    },
    "word_count": 2953
}


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

@app.route('/barviz')
def bar():
    return send_file('static/bar.html')


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
    access_token = dict(parse_qsl(r.text))
    token = json.loads(r.text)
    print token
    facebook_token = Node("FBToken", access_token=token['access_token'], expires_in=token['expires_in'])
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
    user_facebook_token = Relationship(u, "HAS", facebook_token, since=datetime.now())

    graph.create(user_facebook_token)
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


@app.route('/api/v1/gettwitteruser')
def searchtwitterUser():
    users = api.search_users(request.args['name'])
    return jsonify({'users': [
        user for user in users
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


# @app.route('/api/v1/personality/<screen_name>')
# def getPersonaliy(screen_name):
#     # tweets = api.user_timeline(id=screen_name,  )
#     tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(200)
#     text = ""
#     for tweet in tweets:
#         text += tweet.text + "\n " + "\n"
#     profile = personalityInsights.getProfile(text)
#     nodes, edges = personalityInsights.flattenPortrait(profile["tree"])
#
#     return jsonify({'nodes': nodes,'edges': edges})


@app.route('/api/v1/personality')
def getPersonaliy():

    nodes, edges = personalityInsights.flattenPortrait(profileee["tree"])

    return jsonify({'nodes': nodes,'edges': edges})

@app.route('/api/v1/bar')
def getBar():

    data= personalityInsights.datadata(profileee["tree"])
    return jsonify({'data': data})


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


@app.route('/api/v1/fbpost')
def getfbposts():
    graph = fb.GraphAPI(
        access_token='CAACEdEose0cBACq4yTU8mZAVAImodeQTssBBvSBMZBHg6z7cJSzHyZCWMPCitZBZCpzgCTvrcvxdoAQfTXjyII8LeOUKH6tzb4PxzK1ZAm3xpur0uxFZBzFnBpc2gZBvvUh1XR8PBt9WGxvWEtghcHptRrCcHUQnlbaMKw4KCNq5djd5E1IxePyzfVZCMXiSq8kYVBeBowdeZCr3zAyZBfnD1KL16iiaVTxUkMZD')
    friends = graph.get_connections(id='me', connection_name='friends')
    return jsonify({'fiends': friends})



@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()

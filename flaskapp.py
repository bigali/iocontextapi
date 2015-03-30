import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, abort, send_from_directory, send_file, jsonify

import tweepy

app = Flask(__name__)
auth = tweepy.OAuthHandler("VGbGua2zcrvAt8q7rFzYcF7Pp", "LC7DxOcHjzaoHH61MjlWwJvkERWhvnNIHKIasvvvDq9i3J8fGf")
auth.set_access_token("273164662-rcIu2uf0crCAolbKpGJETrU9iMc5XhDHjEo2Oupq",
                      "QxjyYfMQlK83GqwxVZmD4AZFIjtVNTbALFmrGLFdfjfjo")

api = tweepy.API(auth)

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    return send_file("static/index.html")


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


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()

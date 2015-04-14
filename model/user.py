from py2neo import Node, Relationship
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User():
    def get_user_by_id(self, graph, id):
        user = graph.find_one("User", "id", id)
        return user

    def get_user_by_email(self, graph, email):
        user = graph.find_one("User", "email", email)
        return user


    def save_user(self, graph, email, name, password):
        if not self.get_user_by_email(graph, email):
            user = Node("User",
                        id=str(uuid.uuid4()),
                        email=email,
                        display_name=name,
                        password=self.set_password(password))
            graph.create(user)
            return user



    def update_user(self, graph, userId, email, name):
        user = graph.find_one("User", "id", userId)
        user["email"] = email
        user["display_name"] = name
        user.push()
        return user

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, user, password):
        return check_password_hash(user['password'], password)

    def to_json(self, user):
        return dict(id=user['id'], email=user['email'], displayName=user['display_name'],
                    facebook=user['facebook'], google=user['google'],
                    linkedin=user['linkedin'], twitter=user['twitter'])
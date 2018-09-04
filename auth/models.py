from sqlalchemy import or_

from auth import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    email_verification_key = db.Column(db.String)
    last_login = db.Column(db.DateTime)

    def __init__(self, id, email, password, name):
        self.id = id.lower()
        self.name = name
        self.set_email(email.lower())
        self.set_password(password)
        last_login = None

    def set_email(self, email):
        self.email = email
        self.email_verification_key = str(uuid4())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def activated(self):
        return self.last_login is not None

    @property
    def email_verified(self):
        return not self.email_verification_key

    def __repr__(self):
        return '<User {}>'.format(self.id)


def find_user(user):
    return User.query.filter(
        or_(User.id == user.lower(), User.email == user.lower())
    ).one_or_none()

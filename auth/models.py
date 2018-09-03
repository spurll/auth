from sqlalchemy import or_

from auth import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    name = db.Column(db.String, index=True)
    email_verification_key = db.Column(db.String)

    def __init__(self, id, email, password, name):
        self.id = id.lower()
        self.set_email(email.lower())
        self.set_password(password)
        self.name = name

    def set_email(self, email):
        self.email = email
        self.email_verification_key = str(uuid4())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def email_verified(self):
        return not self.email_verification_key

    def __repr__(self):
        return '<User {}>'.format(self.id)


def find_user(id):
    return User.query.filter(
        or_(User.id == id.lower(), User.email == id.lower())
    ).one_or_none()

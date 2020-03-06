from flask import redirect, request
from string import ascii_letters, digits
from urllib.parse import urljoin
from random import SystemRandom
from json import dumps
from datetime import datetime

from auth import app, db
from auth.models import User, find_user
from auth.email import Email


email = Email(
    app.config['SMTP_HOST'],
    app.config['SMTP_USER'],
    app.config['SMTP_PASSWORD']
)


@app.route('/', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'you must verify your email before logging in'
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'invalid password'
        print(message)
        return message, 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    return dumps({'id': user.id, 'email': user.email, 'name': user.name}), 200


@app.route('/new', methods=['POST'])
def new():
    data = request.get_json()

    # Ensure that one user can't use another user's email as their ID
    if '@' in data['id']:
        message = 'username cannot contain "@"'
        print(message)
        return message, 400

    id_user = User.query.get(data['id'])
    email_user = User.query.filter_by(email=data['email']).one_or_none()

    if id_user and id_user.activated:
        message = 'user "{}" already exists'.format(data['id'])
        print(message)
        return message, 400

    elif email_user and email_user.activated:
        message = 'email "{}" already exists'.format(data['email'])
        print(message)
        return message, 400

    else:
        if email_user:
            print('removing inactive user "{}"'.format(email_user))
            db.session.delete(email_user)

        if id_user:
            print('removing inactive user "{}"'.format(id_user))
            db.session.delete(id_user)

        db.session.commit()

    user = User(data['id'], data['email'], data['password'], data['name'])

    db.session.add(user)
    db.session.commit()

    next = data.get('next')
    url = urljoin(
        app.config['BASE_URL'],
        'verify-email/{}{}'.format(
            user.email_verification_key, '?next=' + next if next else ''
        )
    )

    email.send_verification(user, url)

    return 'please check your email to verify your account', 200


@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    user = find_user(data['id'])

    if not user.check_password(data['password']):
        message = 'invalid password'
        print(message)
        return message, 403

    if not user:
        message = 'user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    print('removing verified user "{}"'.format(user))
    db.session.delete(user)
    db.session.commit()

    return 'success', 200


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'you must verify email before resetting your password'
        print(message)
        return message, 400

    rng = SystemRandom()
    password = ''.join(rng.choice(ascii_letters + digits) for _ in range(30))

    user.set_password(password)
    db.session.commit()

    email.send_password(user, password)

    return 'success', 200


@app.route('/update-password', methods=['POST'])
def update_password():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'you must verify your email before updating your password'
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'invalid password'
        print(message)
        return message, 403

    user.set_password(data['new-password'])
    db.session.commit()

    return 'success', 200


@app.route('/update-email', methods=['POST'])
def update_email():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'invalid password'
        print(message)
        return message, 403

    user.set_email(data['email'])
    db.session.commit()

    next = data.get('next')
    url = urljoin(
        app.config['BASE_URL'],
        'verify-email/{}{}'.format(
            user.email_verification_key, '?next=' + next if next else ''
        )
    )

    email.send_verification(user, url)

    return 'success', 200


@app.route('/verify-email/<key>', methods=['GET'])
def verify_email(key):
    user = User.query.filter_by(email_verification_key=key).one_or_none()

    if not user:
        message = 'invalid verification key'
        print(message)
        return message, 400

    user.email_verification_key = None
    db.session.commit()

    next = request.args.get('next')
    return redirect(next) if next else 'success', 200


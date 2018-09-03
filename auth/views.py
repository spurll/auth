from flask import redirect, request
from string import ascii_letters, digits
from urllib.parse import urljoin
from random import SystemRandom
from json import dumps

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
        message = 'Error: user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'Error: user "{}" must verify their email'.format(data['id'])
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'Error: invalid password'
        print(message)
        return message, 403

    return dumps({'id': user.id, 'email': user.email, 'name': user.name}), 200


@app.route('/new', methods=['POST'])
def new():
    data = request.get_json()

    # Ensure that one user can't use another user's email as their ID
    if '@' in data['id']:
        message = 'Error: username cannot contain "@"'
        print(message)
        return message, 400

    if User.query.get(data['id']):
        message = 'Error: user "{}" already exists'.format(data['id'])
        print(message)
        return message, 400

    if User.query.filter_by(email=data['email']).one_or_none():
        message = 'Error: email "{}" already exists'.format(data['email'])
        print(message)
        return message, 400

    user = User(data['id'], data['email'], data['password'], data['name'])

    db.session.add(user)
    db.session.commit()

    next = data.get('next')
    url = urljoin(
        app.config['BASE_URL'],
        '/verify-email/{}{}'.format(
            user.email_verification_key, '?next=' + next if next else ''
        )
    )

    email.send_verification(user, url)

    return 'Success', 200


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'Error: user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'Error: user "{}" must verify their email'.format(data['id'])
        print(message)
        return message, 400

    rng = SystemRandom()
    password = ''.join(rng.choice(ascii_letters + digits) for _ in range(30))

    user.set_password(password)
    db.session.commit()

    email.send_password(user, password)

    return 'Success', 200


@app.route('/update-password', methods=['POST'])
def update_password():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'Error: user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'Error: user "{}" must verify their email'.format(data['id'])
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'Error: invalid password'
        print(message)
        return message, 403

    user.set_password(data['new-password'])
    db.session.commit()

    return 'Success', 200


@app.route('/update-email', methods=['POST'])
def update_email():
    data = request.get_json()
    user = find_user(data['id'])

    if not user:
        message = 'Error: user "{}" does not exist'.format(data['id'])
        print(message)
        return message, 400

    if not user.email_verified:
        message = 'Error: user "{}" must verify their email'.format(data['id'])
        print(message)
        return message, 400

    if not user.check_password(data['password']):
        message = 'Error: invalid password'
        print(message)
        return message, 403

    user.set_email(data['email'])
    db.session.commit()

    next = data.get('next')
    url = urljoin(
        app.config['BASE_URL'],
        '/verify-email/{}{}'.format(
            user.email_verification_key, '?next=' + next if next else ''
        )
    )

    email.send_verification(user, url)

    return 'Success', 200


@app.route('/verify-email/<key>', methods=['GET'])
def verify_email(key):
    user = User.query.filter_by(email_verification_key=key).one_or_none()

    if not user:
        message = 'Error: invalid verification key'
        print(message)
        return message, 400

    user.email_verification_key = None
    db.session.commit()

    next = request.args.get('next')
    return redirect(next) if next else 'Success', 200


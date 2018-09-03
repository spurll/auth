from os import path


# Web Server
CSRF_ENABLED = True
PROPAGATE_EXCEPTIONS = True
BASE_URL = 'http://localhost:9999/'

# SQLAlchemy
basedir = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path.join(basedir, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email
SMTP_HOST = 'smtp.gmail.com:587'
SMTP_USER = 'your.email@gmail.com'
SMTP_PASSWORD = 'app.specific.password'


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Ensure that tables are created. The order in which this occurs is important:
# 1. Initialize the SQLAlchemy object.
# 2. Import the models. (The schema will need to import the SQLAlchemy object.)
# 3. Ensure that the tables are created. (Models must be imported first.)
from auth import models
with app.app_context():
    db.create_all()


from auth import views

#!/venv/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'home'

from reddit import views,models #views imports app, so we need to put this at the end

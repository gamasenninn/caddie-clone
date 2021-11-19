# 本体
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask_sample.db"

db = SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)

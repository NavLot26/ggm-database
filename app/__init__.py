from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__) # app instances 
app.config.from_object(Config) # use the configuration class to set configure the app 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from app import routes, models
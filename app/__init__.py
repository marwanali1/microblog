from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# MARK: App configurations
app = Flask(__name__)
app.config.from_object(Config)

# MARK: Database configurations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MARK: User authentication
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

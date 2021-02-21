import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from flask import Flask
from api.errors.handlers import jwt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()
swag = Swagger()


def create_app(config_class=Config):
    """
    App Factory pattern - returns the app with all extensions registered.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app=app)
    ma.init_app(app=app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app=app)
    cors.init_app(app=app)
    swag.init_app(app=app)

    from .home.routes import home_bp
    from .dealers.routes import dealers_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(dealers_bp)

    return app


from api.models import *

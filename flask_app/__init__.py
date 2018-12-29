from flask import Flask
from flask_bootstrap import Bootstrap
from flask_app.app.views import main
from flask_app.auth.views import auth
from flask_app.api.views import api
from flask_app.extensions import (
    cache,
    debug_toolbar,
    login_manager,
    db,
    ma
)


def create_app(object_name=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(object_name)
    if not object_name:
        app.config.from_pyfile('config.py')

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    ma.init_app(app)

    login_manager.init_app(app)

    Bootstrap(app)

    # register our blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    return app

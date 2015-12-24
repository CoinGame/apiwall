import os
from flask import Flask
from apiwall.settings import Config, ProdConfig, DevConfig, TestConfig
from flask_debugtoolbar import DebugToolbarExtension

from apiwall.extensions import (
    db,
    migrate,
    mapi
)

from apiwall.modules import (
    mod_api,
    mod_home,
 )

from apiwall.context_processors import (
    utility_processor
)

def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_blueprints(app)
    register_extensions(app)
    register_context_processors(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    mapi.init_app(app)
    toolbar = DebugToolbarExtension(app)
    return None

def register_blueprints(app):
    app.register_blueprint(mod_api.controllers.mod_api)
    app.register_blueprint(mod_home.controllers.mod_home)
    return None

def register_context_processors(app):
    app.context_processor(utility_processor)
    return None



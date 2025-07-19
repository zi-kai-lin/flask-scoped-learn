""" App.py contains factory function for app """


from flask import Flask
from silver_app import default
from silver_app.extensions import db, migrate
from silver_app.settings import DevConfig

def create_app(config_object = DevConfig):

    """ __name__ parameter determines the root path of the Application. In this case it is silver_app/app.py """
    app = Flask(__name__)
    """ Flask ignores trailing flashes """
    app.url_map.strict_slashes = False 
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)


    return app



def register_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):

    from silver_app import user
    from silver_app import task


    app.register_blueprint(default.views.blueprint)
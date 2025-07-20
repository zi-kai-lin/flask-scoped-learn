""" App.py contains factory function for app """


from flask import Flask
from flask import g
from silver_app import default
from silver_app.extensions import db, migrate
from silver_app.settings import DevConfig
from silver_app.utils.request_helper import generate_request_id
from werkzeug.exceptions import HTTPException
from silver_app.utils.errors import SilverAppException
from silver_app.utils.responses import handle_generic_exception, handle_http_exception, handle_silver_app_exception

def create_app(config_object = DevConfig):

    """ __name__ parameter determines the root path of the Application. In this case it is silver_app/app.py """
    app = Flask(__name__)
    """ Flask ignores trailing flashes """
    app.url_map.strict_slashes = False 
    app.config.from_object(config_object)
    register_request_handlers(app)
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


def register_request_handlers(app):

    @app.before_request
    def set_request_id():
        g.request_id = generate_request_id()


"""Register error handlers for standardized error responses."""

# Add this function to your app.py
def register_error_handlers(app):
    
    # Handle all custom SilverAppException instances
    app.errorhandler(SilverAppException)(handle_silver_app_exception)
    
    # Handle all HTTP exceptions (404, 500, 400, 401, etc.)
    app.errorhandler(HTTPException)(handle_http_exception)
    
    # Handle any other unhandled exceptions (catch-all)
    app.errorhandler(Exception)(handle_generic_exception)

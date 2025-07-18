""" App.py contains factory function for app """


from flask import Flask
from silver_app import default


def create_app():

    """ __name__ parameter determines the root path of the Application. In this case it is silver_app/app.py """
    app = Flask(__name__)
    """ Flask ignores trailing flashes """
    app.url_map.strict_slashes = False

    app.register_blueprint(default.views.blueprint)


    return app


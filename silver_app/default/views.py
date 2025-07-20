from flask import Blueprint, request
from silver_app.utils.responses import success_response_decorator

blueprint = Blueprint("default", __name__)

@blueprint.route("/", methods = ["GET"])
@success_response_decorator("Default route")
def default_response():
    return ({"greeting": "Hello from Silver App"},)

from flask import Blueprint, request

blueprint = Blueprint("default", __name__)

@blueprint.route("/", methods = ["GET"])
def default_response():
    return "hello there"

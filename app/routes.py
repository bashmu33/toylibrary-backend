from flask import Blueprint, jsonify

hello_world_bp = Blueprint("hello_world", __name__)

@hello_world_bp.route("/hello-world", methods=["GET"])
def endpoint_name():
    my_beautiful_response_body = "Hello World!"
    return my_beautiful_response_body
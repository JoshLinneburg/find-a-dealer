from flask import jsonify, make_response
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def make_error(status_code=400, status_text="NOT OK!", message="ERROR!"):
    return make_response(
        jsonify(
            {"status_code": status_code, "status_text": status_text, "message": message}
        ),
        status_code,
    )


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    """
    By default, if an expired token attempts to access a protected endpoint,
    we return a generic error message with a 401 status
    """
    token_type = expired_token["type"]
    return (
        jsonify(
            {
                "status_code": 401,
                "status_text": "NOT OK!",
                "message": f"Expired {token_type} token!",
            }
        ),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    """
    By default, if an invalid token attempts to access a protected endpoint, we
    return the error string for why it is not valid with a 422 status code
    :param error_string: String indicating why the token is invalid
    """
    return (
        jsonify(
            {
                "status_code": 422,
                "status_text": "NOT OK!",
                "message": error_string,
            }
        ),
        422,
    )


@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    """
    By default, if a protected endpoint is accessed without a JWT, we return
    the error string indicating why this is unauthorized, with a 401 status code
    :param error_string: String indicating why this request is unauthorized
    """
    return (
        jsonify(
            {"status_code": 401, "status_text": "NOT OK!", "message": error_string}
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    """
    By default, if a non-fresh jwt is used to access a ```fresh_jwt_required```
    endpoint, we return a general error message with a 401 status code
    """
    return (
        jsonify(
            {
                "status_code": 401,
                "status_text": "NOT OK!",
                "message": "Fresh token required found!",
            }
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    """
    By default, if a revoked token is used to access a protected endpoint, we
    return a general error message with a 401 status code
    """
    return (
        jsonify(
            {
                "status_code": 401,
                "status_text": "NOT OK!",
                "message": "Token has been revoked!",
            }
        ),
        401,
    )

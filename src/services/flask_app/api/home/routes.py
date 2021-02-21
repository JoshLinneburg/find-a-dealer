from flask import Blueprint, make_response, jsonify

home_bp = Blueprint("home_bp", __name__, url_prefix="/")


@home_bp.route("", methods=["GET"])
def get_status():
    """
    Returns 200 OK if the app is running, 400 NOT OK if not.
    """

    try:
        response = make_response(
            jsonify(
                {
                    "status_code": 200,
                    "status_text": "OK!",
                    "message": "The API is working",
                }
            ),
            200,
        )

    except:
        response = make_response(
            jsonify(
                {
                    "status_code": 400,
                    "status_text": "NOT OK!",
                    "message": "The API is not working",
                }
            ),
            400,
        )

    return response

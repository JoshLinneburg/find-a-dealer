import sys
import traceback

from flask import Blueprint, make_response, jsonify, request

from api import db
from api.dealers.utils import (
    get_dealer_if_exists,
    create_dealer,
    create_dealer_hours,
    create_dealer_service,
)
from api.schemas import DealerOutputSchema

dealers_bp = Blueprint("dealers_bp", __name__, url_prefix="/api/v1/dealers")


@dealers_bp.route("", methods=["POST"])
def create_new_dealer():
    try:
        data = request.get_json()

        dealer = get_dealer_if_exists(
            phone=data.get("phone", None),
            email=data.get("email", None),
            latitude=data.get("latitude", None),
            longitude=data.get("longitude", None)
        )

        if dealer:
            return make_response(
                jsonify(
                    {
                        "status_text": "NOT OK!",
                        "status_code": 400,
                        "message": "Dealer already exists!"
                    }
                ),
                400
            )

        new_dealer = create_dealer(input_data=data)

        if data.get("sales_hours", None):
            create_dealer_hours(
                dealer_id=new_dealer.id,
                hours=data["sales_hours"],
                hours_type="sales",
            )

        if data.get("service_hours", None):
            create_dealer_hours(
                dealer_id=new_dealer.id,
                hours=data["service_hours"],
                hours_type="service",
            )

        if data.get("services", None):
            create_dealer_service(
                dealer_id=new_dealer.id,
                services=data["services"]
            )

        dealer_schema = DealerOutputSchema()
        dealer_data = dealer_schema.dump(new_dealer)

        db.session.commit()

        return make_response(
            jsonify(
                {
                    "status_code": 201,
                    "status_text": "OK!",
                    "message": "Dealer created!",
                    "results": dealer_data
                }
            ),
            201
        )

    except Exception as e:

        db.session.rollback()

        return make_response(
            jsonify(
                {
                    "status_code": 400,
                    "status_text": "NOT OK!",
                    "message": str(e),
                    "stacktrace": traceback.format_exc(),
                }
            ),
            400
        )


@dealers_bp.route("", methods=["GET"])
def get_dealers():
    pass


@dealers_bp.route("/<public_id>", methods=["GET"])
def get_dealer():
    pass

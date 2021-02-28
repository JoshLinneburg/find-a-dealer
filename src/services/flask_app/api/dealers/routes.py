import logging
import os
import traceback

from flask import Blueprint, make_response, jsonify, request

from api import db
from api.dealers.utils import (
    get_dealer_by_public_id,
    get_dealer_if_exists,
    create_dealer,
    create_dealer_hours,
    create_dealer_service,
    return_exception_as_json,
)
from api.schemas import DealerOutputSchema

dealers_bp = Blueprint("dealers_bp", __name__, url_prefix="/api/v1/dealers")


logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@dealers_bp.route("", methods=["POST"])
def create_new_dealer():
    try:
        data = request.get_json()

        dealer = get_dealer_if_exists(
            brand=data.get("brand"),
            internal_id=data.get("internal_id"),
            latitude=round(float(data.get("latitude", None)), 4),
            longitude=round(float(data.get("longitude", None)), 4)
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
def get_dealer(public_id):
    try:
        dealer = get_dealer_by_public_id(dealer_public_id=public_id)
        dealer_schema = DealerOutputSchema()
        dealer_data = dealer_schema.dump(dealer)

        return make_response(
            jsonify(
                {
                    "status_code": 200,
                    "status_text": "OK!",
                    "message": "Dealer found and returned!",
                    "results": dealer_data
                }
            ),
            200
        )

    except LookupError as e:
        return return_exception_as_json(
            exception=e,
            status_code=404,
        )

    except Exception as e:
        db.session.rollback()

        return return_exception_as_json(
            exception=e,
            status_code=400,
        )


@dealers_bp.route("/<public_id>", methods=["PUT"])
def update_dealer(public_id):

    data = request.get_json()

    immutable_fields = [
        "id",
        "public_id",
        "created_datetime",
        "modified_datetime",
    ]

    try:
        dealer = get_dealer_by_public_id(dealer_public_id=public_id)

        for key, value in data.items():
            if key in immutable_fields:
                continue
            else:
                setattr(dealer, key, value)

        db.session.commit()

    except LookupError as e:
        return return_exception_as_json(
            exception=e,
            status_code=404,
        )

    except Exception as e:
        db.session.rollback()

        return return_exception_as_json(
            exception=e,
            status_code=400,
        )


@dealers_bp.route("/<public_id>", methods=["DELETE"])
def delete_dealer(public_id):
    pass

import datetime
import uuid

from api import db
from api.models import Dealer, Dealer_Hours, Dealer_Service, Service
from api.schemas import DealerSchema, HoursSchema, ServiceSchema, DealerServiceSchema
from flask import Blueprint, make_response, jsonify, request
from sqlalchemy import or_, and_

dealers_bp = Blueprint("dealers_bp", __name__, url_prefix="/api/v1/dealers")


@dealers_bp.route("", methods=["POST"])
def create_new_dealer():
    data = request.get_json()

    dealer = Dealer.query.filter(
        or_(
            Dealer.phone == data["phone"],
            Dealer.email == data["email"],
            and_(Dealer.latitude == data["latitude"], Dealer.longitude == data["longitude"])
        )
    ).first()

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

    new_dealer = Dealer(
        public_id=str(uuid.uuid4()),
        internal_id=data["sales_code"],
        brand=data["brand"].upper(),
        name=data["name"].upper(),
        street_address=data["street_address"].upper(),
        city=data["city"].upper(),
        state=data["state"],
        postal_code=data["postal_code"],
        country=data["country"].upper(),
        latitude=data["latitude"],
        longitude=data["longitude"],
        phone=data["phone"],
        email=data["email"],
        website=data["url"]
    )

    db.session.add(new_dealer)
    db.session.flush()

    if "sales_hours" in data.keys():
        for entry in data["sales_hours"]:
            new_hours = Dealer_Hours(
                public_id=str(uuid.uuid4()),
                dealer_id=new_dealer.id,
                day_of_week=entry["day_of_week"],
                open_time=datetime.time.fromisoformat(entry["open"]),
                close_time=datetime.time.fromisoformat(entry["close"]),
                schedule_type="sales",
            )

            db.session.add(new_hours)
        db.session.flush()

    if "service_hours" in data.keys():
        for entry in data["service_hours"]:
            new_hours = Dealer_Hours(
                public_id=str(uuid.uuid4()),
                dealer_id=new_dealer.id,
                day_of_week=entry["day_of_week"],
                open_time=datetime.time.fromisoformat(entry["open"]),
                close_time=datetime.time.fromisoformat(entry["close"]),
                schedule_type="service",
            )

            db.session.add(new_hours)
        db.session.flush()

    if "services" in data.keys():
        for entry in data["services"]:
            service = Service.query.filter(Service.service_name == entry).first()

            if not service:
                service = Service(
                    public_id=str(uuid.uuid4()),
                    service_name=entry
                )

                db.session.add(service)
                db.session.flush()

            new_dealer_service = Dealer_Service(
                dealer_id=new_dealer.id,
                service_id=service.id,
            )

            db.session.add(new_dealer_service)
            db.session.flush()

    dealer_schema = DealerSchema()
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


@dealers_bp.route("", methods=["GET"])
def get_dealers():
    pass


@dealers_bp.route("/<public_id>", methods=["GET"])
def get_dealer():
    pass

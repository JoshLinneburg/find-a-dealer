import datetime
import traceback
import uuid

from api import db
from api.models import Dealer, DealerHours, DealerService, Service
from flask import jsonify, make_response
from sqlalchemy import and_, or_, func
from typing import Dict, List, Type


def get_dealer_if_exists(
        brand: str,
        internal_id: str,
        latitude: float,
        longitude: float,
):
    response = Dealer.query.filter(
        and_(
            Dealer.brand == brand,
            Dealer.internal_id == internal_id,
            func.abs(Dealer.latitude - round(float(latitude), 4)) < 0.0001,
            func.abs(Dealer.longitude - round(float(longitude), 4)) < 0.0001,
        )
    ).all()

    # print(response[0].latitude, response[0].longitude, latitude, longitude)

    return response


def get_dealer_by_public_id(
        dealer_public_id: str
):
    response = Dealer.query.filter(
        Dealer.public_id == dealer_public_id
    ).first()

    if not response:
        raise LookupError("Dealer not found!")

    return response


def create_dealer(
        input_data: Dict,
):
    new_dealer = Dealer(
        public_id=str(uuid.uuid4()),
        internal_id=input_data["internal_id"],
        brand=input_data["brand"].upper(),
        name=input_data["name"].upper(),
        street_address=input_data["street_address"].upper(),
        city=input_data["city"].upper(),
        state=input_data["state"],
        postal_code=input_data["postal_code"],
        country=input_data["country"].upper(),
        latitude=round(float(input_data["latitude"]), 4),
        longitude=round(float(input_data["longitude"]), 4),
        phone=input_data["phone"],
        email=input_data["email"],
        website=input_data["url"]
    )

    db.session.add(new_dealer)
    db.session.flush()

    return new_dealer


def create_dealer_hours(
        dealer_id: int,
        hours: List[Dict],
        hours_type: str
):
    results = []

    for entry in hours:
        new_hours = DealerHours(
            public_id=str(uuid.uuid4()),
            dealer_id=dealer_id,
            day_of_week=entry["day_of_week"],
            open_time=datetime.time.fromisoformat(entry["open"]) if entry["open"] else None,
            close_time=datetime.time.fromisoformat(entry["close"]) if entry["close"] else None,
            schedule_type=hours_type,
        )

        db.session.add(new_hours)
        db.session.flush()
        results.append(new_hours)

    return results


def create_service(
        service_name: str
):
    service = Service(
        public_id=str(uuid.uuid4()),
        service_name=service_name
    )

    db.session.add(service)
    db.session.flush()

    return service


def create_dealer_service(
        dealer_id: int,
        services: List,
):
    results = []

    for service_name in services:
        response = Service.query.filter(Service.service_name == service_name).first()

        if not response:
            response = create_service(service_name=service_name)

        new_dealer_service = DealerService(
            dealer_id=dealer_id,
            service_id=response.id,
        )

        db.session.add(new_dealer_service)
        db.session.flush()
        results.append(new_dealer_service)

    return results


def return_exception_as_json(
        exception: Exception,
        status_code: int,
        status_text: str = "NOT OK!"
):
    return make_response(
        jsonify(
            {
                "status_code": status_code,
                "status_text": status_text,
                "message": str(exception),
            }
        ),
        status_code
    )

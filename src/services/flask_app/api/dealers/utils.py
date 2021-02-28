import datetime
import uuid

from api import db
from api.models import Dealer, DealerHours, DealerService, Service
from sqlalchemy import and_, or_
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
            Dealer.latitude - round(latitude, 4) < 0.0001,
            Dealer.longitude - round(longitude, 4) < 0.0001,
        )
    ).all()

    return response


def create_dealer(
        input_data: Dict,
):
    new_dealer = Dealer(
        public_id=str(uuid.uuid4()),
        internal_id=input_data["sales_code"],
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

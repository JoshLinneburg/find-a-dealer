import datetime

from api import db
from sqlalchemy import Column, String, Integer, ForeignKey, Float


class Dealer(db.Model):
    __tablename__ = "dealer"

    id = Column(Integer, primary_key=True)
    internal_id = Column(String(100), nullable=False)
    brand = Column(String(50), nullable=False)
    name = Column(String(128), nullable=False)
    street_address = Column(String(250))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(Integer)
    country = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(25))
    email = Column(String(50))
    website = Column(String(50))

    sales_hours = db.relationship(
        "Dealer_Schedule",
        primaryjoin="and_(dealer.id==dealer_schedule.dealer_id, "
        "dealer_schedule.schedule_type=='sales')",
    )

    service_hours = db.relationship(
        "Dealer_Schedule",
        primaryjoin="and_(dealer.id==dealer_schedule.dealer_id, "
        "dealer_schedule.schedule_type=='service')",
    )

    services = db.relationship(
        "Dealer_Service", backref="dealer", lazy="dynamic", passive_deletes=True
    )

    created_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Service(db.Model):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True)
    service_name = Column(String(250), nullable=False)

    services = db.relationship(
        "Dealer_Service", backref="service", lazy="dynamic", passive_deletes=True
    )

    created_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Dealer_Service(db.Model):
    __tablename__ = "dealer_service"

    dealer_id = Column(
        Integer, ForeignKey("dealer.id", ondelete="CASCADE"), primary_key=True
    )
    service_id = Column(
        Integer, ForeignKey("service.id", ondelete="CASCADE"), primary_key=True
    )
    created_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class Dealer_Schedule(db.Model):
    __tablename__ = "dealer_schedule"

    id = Column(String(128), primary_key=True)
    dealer_id = Column(
        Integer, ForeignKey("dealer.id", ondelete="CASCADE"), nullable=False
    )
    day_of_week = Column(String(25), nullable=False)
    open_time = Column(db.Time)
    close_time = Column(db.Time)
    schedule_type = Column(String(25), nullable=False)
    created_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

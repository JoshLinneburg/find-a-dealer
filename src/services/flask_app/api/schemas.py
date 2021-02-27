from api import ma
from api.models import Dealer, Service, DealerHours, DealerService
from marshmallow import fields


class DealerSchema(ma.Schema):
    class Meta:

        model = Dealer

        fields = (
            "public_id",
            "internal_id",
            "brand",
            "name",
            "phone",
            "email",
            "website",
            "street_address",
            "city",
            "state",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "sales_hours",
            "service_hours",
            "services",
        )

        ordered = True

    sales_hours = ma.Nested("HoursSchema", many=True)
    service_hours = ma.Nested("HoursSchema", many=True)
    services = fields.Pluck("DealerServiceSchema", "service", many=True)


class HoursSchema(ma.Schema):
    class Meta:

        model = DealerHours

        fields = (
            "day_of_week",
            "open_time",
            "close_time",
            "schedule_type",
        )

        ordered = True


class DealerServiceSchema(ma.Schema):
    class Meta:
        fields = ("service",)

    service = fields.Pluck("ServiceSchema", "service_name")


class ServiceSchema(ma.Schema):
    class Meta:

        fields = ("service_name",)




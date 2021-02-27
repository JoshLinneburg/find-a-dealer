import datetime
import logging
import os
import unittest

from src.services.flask_app import config
from api import create_app
from api import db
from api.models import Dealer, DealerService, Service

from api.dealers.utils import (
    get_dealer_if_exists,
    create_dealer,
    create_service,
    create_dealer_hours,
    create_dealer_service,
)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger()


class TestConfig(config.Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(config.basedir, 'test.db')


class TestDealerCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestDealerCreation, cls).setUpClass()
        cls.app = create_app(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        for file in ["dealer_table.sql", "service_table.sql", "dealer_hours_table.sql", "dealer_service_table.sql"]:
            with open(f"../sql/{file}", "r") as f:
                for line in f:
                    if "INSERT" not in line:
                        continue
                    else:
                        db.session.execute(line)

            db.session.commit()

        logger.info("Ran the setUp method")

    @classmethod
    def tearDownClass(cls) -> None:
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        os.remove(os.path.join(config.basedir, 'test.db'))

        logger.info("Ran the tearDown method")

    def test_get_dealer_by_phone(self) -> None:
        response = get_dealer_if_exists(
            phone="(800) 610-3781",
        )

        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == 1)
        self.assertTrue(isinstance(response[0], Dealer))
        self.assertTrue(hasattr(response[0], "sales_hours"))
        self.assertTrue(hasattr(response[0], "service_hours"))
        self.assertTrue(hasattr(response[0], "services"))
        self.assertEqual(response[0].name, "DEAN ARBOUR FORD OF TAWAS, INC.")

    def test_get_dealer_by_email(self) -> None:
        response = get_dealer_if_exists(
            email="tawas@deanarbour.com",
        )

        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == 1)
        self.assertTrue(isinstance(response[0], Dealer))
        self.assertTrue(hasattr(response[0], "sales_hours"))
        self.assertTrue(hasattr(response[0], "service_hours"))
        self.assertTrue(hasattr(response[0], "services"))
        self.assertEqual(response[0].name, "DEAN ARBOUR FORD OF TAWAS, INC.")

    def test_get_dealer_by_coordinates(self) -> None:
        response = get_dealer_if_exists(
            latitude=44.279951,
            longitude=-83.523281,
        )

        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == 1)
        self.assertTrue(isinstance(response[0], Dealer))
        self.assertTrue(hasattr(response[0], "sales_hours"))
        self.assertTrue(hasattr(response[0], "service_hours"))
        self.assertTrue(hasattr(response[0], "services"))
        self.assertEqual(response[0].name, "DEAN ARBOUR FORD OF TAWAS, INC.")

    def test_get_dealer_when_not_exists(self) -> None:
        response = get_dealer_if_exists(
            phone="notarealphonenumber",
            email="notarealemail",
        )

        self.assertTrue(not response)

    def test_create_dealer(self) -> None:

        input_data = {
            "sales_code": "12345",
            "brand": "Ford",
            "name": "Josh Linneburg Ford",
            "email": "joshlinneburg@forddealers.com",
            "phone": "(123) 456-7890",
            "url": "https://joshlinneburgford.com",
            "street_address": "123 Main Street",
            "city": "Ann Arbor",
            "state": "MI",
            "postal_code": "00000",
            "country": "USA",
            "latitude": "00.00000",
            "longitude": "00.00000"
        }

        response = create_dealer(input_data=input_data)

        self.assertTrue(isinstance(response, Dealer))
        self.assertEqual(response.internal_id, "12345")
        self.assertEqual(response.name, "JOSH LINNEBURG FORD")
        self.assertEqual(float(response.latitude), 0.0)
        self.assertEqual(float(response.longitude), 0.0)

    def test_create_dealer_hours(self) -> None:
        input_data = {
            "dealer_id": 3603,
            "hours": [
                {
                    "day_of_week": "Sunday",
                    "open": None,
                    "close": None
                },
                {
                    "day_of_week": "Monday",
                    "open": "09:00",
                    "close": "19:00"
                },
                {
                    "day_of_week": "Tuesday",
                    "open": "09:00",
                    "close": "19:00"
                },
                {
                    "day_of_week": "Wednesday",
                    "open": "09:00",
                    "close": "19:00"
                },
                {
                    "day_of_week": "Thursday",
                    "open": "09:00",
                    "close": "19:00"
                },
                {
                    "day_of_week": "Friday",
                    "open": "09:00",
                    "close": "19:00"
                },
                {
                    "day_of_week": "Saturday",
                    "open": "09:00",
                    "close": "18:00"
                }
            ],
            "hours_type": "service"
        }

        response = create_dealer_hours(**input_data)

        self.assertTrue(isinstance(response, list))
        self.assertTrue(len(response) == len(input_data["hours"]))
        self.assertEqual(response[0].dealer_id, input_data["dealer_id"])
        self.assertEqual(response[0].day_of_week, "Sunday")
        self.assertTrue(not response[0].open_time)
        self.assertTrue(isinstance(response[1].open_time, datetime.time))
        self.assertTrue(isinstance(response[1].close_time, datetime.time))
        self.assertEqual(response[1].open_time, datetime.time(9, 0))
        self.assertEqual(response[1].close_time, datetime.time(19, 0))
        self.assertEqual(response[1].schedule_type, "service")

    def test_create_new_service(self) -> None:
        input_data = {
            "service_name": "'The Works' Package"
        }

        response = create_service(**input_data)

        self.assertTrue(isinstance(response, Service))
        self.assertEqual(response.service_name, input_data["service_name"])

    def test_create_new_dealer_service(self) -> None:
        input_data = {
            "dealer_id": 3603,
            "services": [
                "Medium Duty Service",  # THIS ONE ALREADY EXISTS
                "Some other service",
                "Another new service",
            ]
        }

        response = create_dealer_service(**input_data)

        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 3)
        self.assertTrue(isinstance(response[0], DealerService))
        self.assertEqual(response[0].dealer_id, 3603)
        self.assertEqual(response[0].service_id, 119)
        self.assertEqual(response[0].service.service_name, "Medium Duty Service")
        self.assertTrue(response[1].service_id)
        self.assertEqual(response[1].service.service_name, "Some other service")
        self.assertTrue(response[2].service_id)
        self.assertEqual(response[2].service.service_name, "Another new service")


if __name__ == "__main__":
    unittest.main()

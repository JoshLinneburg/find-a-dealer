import config
import datetime
import json
import logging
import os
import unittest

from api import create_app
from api import db

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

        cls.testing_client = cls.app.test_client()

        logger.info("Ran the setUp method")

    @classmethod
    def tearDownClass(cls) -> None:
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        os.remove(os.path.join(config.basedir, 'test.db'))

        logger.info("Ran the tearDown method")

    def test_create_dealer_1(self) -> None:

        headers = {"Content-Type": "application/json"}

        payload = {
            "internal_id": "LOL",
            "brand": "Ford",
            "name": "Joshua Linneburg Ford",
            "email": "joshualinneburg@gmail.com",
            "phone": "(586) 651-4071",
            "url": "https://www.joshualinneburg.com",
            "street_address": "1471 First Street North",
            "city": "Alabaster",
            "state": "AL",
            "postal_code": "35007",
            "country": "USA",
            "full_address": {
                "street_address": "1471 First Street North",
                "city": "Alabaster",
                "state": "AL",
                "postal_code": "35007",
                "country": "USA"
            },
            "latitude": "00.0000",
            "longitude": "00.0000",
            "sales_hours": [
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
            "service_hours": [
                {
                    "day_of_week": "Sunday",
                    "open": None,
                    "close": None
                },
                {
                    "day_of_week": "Monday",
                    "open": "07:00",
                    "close": "18:00"
                },
                {
                    "day_of_week": "Tuesday",
                    "open": "07:00",
                    "close": "18:00"
                },
                {
                    "day_of_week": "Wednesday",
                    "open": "07:00",
                    "close": "18:00"
                },
                {
                    "day_of_week": "Thursday",
                    "open": "07:00",
                    "close": "18:00"
                },
                {
                    "day_of_week": "Friday",
                    "open": "07:00",
                    "close": "18:00"
                },
                {
                    "day_of_week": "Saturday",
                    "open": "07:00",
                    "close": "14:00"
                }
            ],
            "services": [
                "National fleet Pricing",
                "Aluminum F-Series Repair",
                "Accepts Online Reservations For Ford",
                "Light Truck",
                "New Vehicle Inventory Online",
                "Extended Service Hours",
                "EV Certified Dealers",
                "Dealers That Sell Tires",
                "Quick Lane",
                "Courtesy Delivery",
                "National Fleet Parts Pricing",
                "SVT",
                "Blue Oval Certified",
                "Accepts Online Orders For Ford"
            ]
        }

        response = self.testing_client.post(
            "/api/v1/dealers", data=json.dumps(payload, indent=2), headers=headers
        )
        data = json.loads(response.data)

        self.assertTrue(data)
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(["status_code", "status_text", "message" in data.keys()])
        self.assertEqual(data["status_code"], 201)
        self.assertEqual(data["status_text"], "OK!")
        self.assertEqual(data["message"], "Dealer created!")
        self.assertTrue("results" in data.keys())
        self.assertTrue(isinstance(data["results"], dict))
        self.assertEqual(data["results"]["internal_id"], "LOL")
        self.assertEqual(data["results"]["brand"], "FORD")
        self.assertEqual(data["results"]["name"], "JOSHUA LINNEBURG FORD")
        self.assertTrue("sales_hours" in data["results"].keys())
        self.assertEqual(len(data["results"]["sales_hours"]), len(payload["sales_hours"]))
        self.assertTrue("service_hours" in data["results"].keys())
        self.assertEqual(len(data["results"]["service_hours"]), len(payload["service_hours"]))
        self.assertTrue("services" in data["results"].keys())
        self.assertEqual(len(data["results"]["services"]), len(payload["services"]))

    def test_create_dealer_2(self) -> None:

        headers = {"Content-Type": "application/json"}

        payload = {
            "internal_id": "48W610",
            "brand": "Ford",
            "name": "Joshua Linneburg Ford",
            "email": "joshualinneburg@gmail.com",
            "phone": "(586) 651-4071",
            "url": "https://www.joshualinneburg.com",
            "street_address": "1471 First Street North",
            "city": "Alabaster",
            "state": "AL",
            "postal_code": "35007",
            "country": "USA",
            "full_address": {
                "street_address": "1471 First Street North",
                "city": "Alabaster",
                "state": "AL",
                "postal_code": "35007",
                "country": "USA"
            },
            "latitude": "44.279951",
            "longitude": "-83.523281",
        }

        response = self.testing_client.post(
            "/api/v1/dealers", data=json.dumps(payload, indent=2), headers=headers
        )
        data = json.loads(response.data)

        self.assertTrue(data)
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(["status_code", "status_text", "message" in data.keys()])
        self.assertEqual(data["status_code"], 400)
        self.assertEqual(data["status_text"], "NOT OK!")
        self.assertEqual(data["message"], "Dealer already exists!")

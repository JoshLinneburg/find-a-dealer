import logging
import os
import unittest

from src.services.flask_app import config
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

        cls.client = cls.app.testing_client()

        logger.info("Ran the setUp method")

    @classmethod
    def tearDownClass(cls) -> None:
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        os.remove(os.path.join(config.basedir, 'test.db'))

        logger.info("Ran the tearDown method")
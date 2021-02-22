import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import datetime

from api import db, create_app
from api.models import (
    Dealer,
    Dealer_Service,
    Dealer_Hours,
    Service
)
from config import Config
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def test_client():
    """
    Initializes the testing environment for PyTest.
    Creates the Flask app with the application factory.
    Drops all the tables in the local Postgres DB, creates them again, inserts
    data from the `data.sql` file line-by-line. Then yields the testing_client
    for testing purposes. After the tests have been run,
    the session is closed and the tables are all dropped.
    Yields:
        testing_client: Flask.test_client
            A test client for making requests and retrieving data from
            an isolated version of our Flask app.
    """
    app = create_app()

    testing_client = app.test_client()

    with app.app_context():

        yield testing_client  # this is where the testing happens!

        db.session.close()

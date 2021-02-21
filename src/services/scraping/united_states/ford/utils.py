import logging
import os
import requests
import random
import time

states = [
    "ALABAMA",
    "ALASKA",
    "ARIZONA",
    "ARKANSAS",
    "CALIFORNIA",
    "COLORADO",
    "CONNECTICUT",
    "DELAWARE",
    "FLORIDA",
    "GEORGIA",
    "HAWAII",
    "IDAHO",
    "ILLINOIS",
    "INDIANA",
    "IOWA",
    "KANSAS",
    "KENTUCKY",
    "LOUISIANA",
    "MAINE",
    "MARYLAND",
    "MASSACHUSETTS",
    "MICHIGAN",
    "MINNESOTA",
    "MISSISSIPPI",
    "MISSOURI",
    "MONTANA",
    "NEBRASKA",
    "NEVADA",
    "NEW HAMPSHIRE",
    "NEW JERSEY",
    "NEW MEXICO",
    "NEW YORK",
    "NORTH CAROLINA",
    "NORTH DAKOTA",
    "OHIO",
    "OKLAHOMA",
    "OREGON",
    "PENNSYLVANIA",
    "RHODE ISLAND",
    "SOUTH CAROLINA",
    "SOUTH DAKOTA",
    "TENNESSEE",
    "TEXAS",
    "UTAH",
    "VERMONT",
    "VIRGINIA",
    "WASHINGTON",
    "WEST VIRGINIA",
    "WISCONSIN",
    "WYOMING",
]

api_key = "0d571406-82e4-2b65-cc885011-048eb263"

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger()


def parse_ford_address(address):
    """
    Parses a Ford-formatted address.
    """
    street = address["Street1"] + address["Street2"] + address["Street3"]
    city = address["City"]
    state = address["State"]
    postal_code = address["PostalCode"]
    country = address["Country"]
    return f"{street} {city}, {state} {postal_code}, {country}"


def parse_ford_day_hours(hours_dict):
    """
    Parses a Ford-formatted hours dictionary.
    """
    if "closed" in hours_dict.keys():
        return {"open": None, "close": None}
    else:
        return {
            "open": hours_dict["open"],
            "close": hours_dict["close"]
        }


def parse_ford_hours(hours_by_day):
    """
    Parses a list of Ford-formatted dictionaries.
    """
    return {
        day["name"]: parse_ford_day_hours(day)
        for day in hours_by_day
    }


def get_ford_dealers():
    """
    Gets all Ford dealers by each state.
    """
    data = []
    params = {
        "api_key": api_key,
        "maxDealers": 200,
        "make": "Ford",
    }

    for state in states:

        logger.info(f"Scraping {state} for Ford dealerships.")

        params["state"] = state
        response = requests.get(url="https://www.ford.com/services/dealer/Dealers.json", params=params)
        dealers = response.json()["Response"]["Dealer"]
        data += dealers

        logger.info(f"Found {len(dealers)} dealerships in {state}.")

        time.sleep(random.randrange(1, 5))

    logger.info(f"Found {len(data)} dealerships in total.")

    return data


def clean_ford_data(data):
    """
    Cleans the Ford dealership data
    """
    return [
        {
            "brand": "Ford",
            "name": dealer["Name"],
            "email": dealer["Email"],
            "phone": dealer["Phone"],
            "url": dealer["URL"],
            "address": parse_ford_address(dealer["Address"]),
            "latitude": dealer["Latitude"],
            "longitude": dealer["Longitude"],
            "sales_hours": parse_ford_hours(dealer["SalesHours"]["Day"]) if dealer["SalesHours"] else None,
            "service_hours": parse_ford_hours(dealer["ServiceHours"]["Day"]) if dealer["ServiceHours"] else None,
            "specialties": dealer["Specialties"]["Specialty"],
            "sales_code": dealer["SalesCode"]
        } for dealer in data
    ]
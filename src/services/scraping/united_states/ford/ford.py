import json
import logging
import os
from utils import get_ford_dealers, clean_ford_data

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger()


def main():
    """
    Gets all Ford dealerships and cleans the data
    """
    data = get_ford_dealers()
    cleaned_data = clean_ford_data(data=data)

    with open("ford_cleaned.json", "w") as f:
        json.dump(cleaned_data, f, indent=4)


if __name__ == "__main__":
    main()

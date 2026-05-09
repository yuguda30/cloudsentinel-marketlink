import json
import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOCATION_FILE = os.path.join(BASE_DIR, "data", "nigeria_locations.json")


def load_locations():
    try:
        with open(LOCATION_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def get_states():
    locations = load_locations()
    return sorted(locations.keys())


def get_lgas_by_state(state_name):
    locations = load_locations()

    if not state_name:
        return []

    return locations.get(state_name, [])


def is_valid_state_lga(state_name, lga_name):
    locations = load_locations()

    if state_name not in locations:
        return False

    return lga_name in locations[state_name]
import json
import os

def load_json_file(file_path):
    with open(file_path, encoding='utf-8') as file:
        return json.load(file)

def load_npcs_data():
    return load_json_file(os.path.join("resources", "data", "npcs.json"))

def load_features_data():
    return load_json_file(os.path.join("resources", "data", "features.json"))

def load_personalities_data():
    return load_json_file(os.path.join("resources", "data", "personalities.json"))

def load_places_data():
    return load_json_file(os.path.join("resources", "data", "places.json"))

def load_weapons_data():
    return load_json_file(os.path.join("resources", "data", "weapons.json"))

def load_names_data():
    return load_json_file(os.path.join("resources", "data", "names.json"))

def load_wealth_data():
    return load_json_file(os.path.join("resources", "data", "wealth.json"))

def load_scenarios_data():
    return load_json_file(os.path.join("resources", "data", "scenarios.json"))

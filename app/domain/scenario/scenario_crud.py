import random

from .schema import scenario_crud_schema
from app.lib import const

characters_data = scenario_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = scenario_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name: str):
    """
    Retrieve information for a character by name.
    If the character does not exist, returns None.

    Args:
        name (str): The name of the character to find.

    Returns:
        Character object or None if not found.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def get_character_criminal_scenario(name: str):
    """
    Fetch criminal scenario details for a given character by name.
    If no matching character is found, returns None.

    Args:
        name (str): The name of the character whose criminal scenario is sought.

    Returns:
        CriminalScenario object or None if not found.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character.criminalScenario
    return None

def select_crime_scene(place_data: list):
    """
    Randomly selects a crime scene from a list of possible places.

    Args:
        place_data (list): Data structure containing potential crime scenes.

    Returns:
        A randomly selected Place object.
    """
    return random.choice(place_data)

def select_random_character(candidates: list, excluded_characters: list):
    """
    Selects a random character from a list, excluding specified characters.

    Args:
        candidates (list): List of candidate Characters to select from.
        excluded_characters (list): List of character names to exclude from selection.

    Returns:
        A randomly selected Character object, or None if no valid characters are found.
    """
    filtered_candidates = [character.name for character in candidates if character.name not in excluded_characters]

    valid_characters = [get_character_info(character) for character in filtered_candidates if get_character_info(character)]

    if valid_characters:
        return random.choice(valid_characters)
    return None

def get_characters_info(candidates: list, excluded_characters: list):
    """
    Retrieves information for a list of characters, excluding specified characters.

    Args:
        candidates (list): List of candidate Characters for retrieving information.
        excluded_characters (list): List of character names to exclude from the retrieval.

    Returns:
        List of Character objects with detailed information, excluding the specified characters.
    """
    names = [character.name for character in candidates if character.name not in excluded_characters]

    characters_info = []
    for name in names:
        character_info = get_character_info(name)
        if character_info:
            characters_info.append(character_info)
    return characters_info

def validate_living_characters(living_characters):
    """
    Validates that all characters in the living characters list exist in the characters data.

    Args:
        living_characters (list): List of character names to validate.

    Returns:
        bool: True if all characters exist, False otherwise.
    """
    living_characters_names = [character.name for character in living_characters]
    for character_name in living_characters_names:
        if not get_character_info(character_name):
            return False
    return True

def translate_place_name_ko_to_en(place_list: list, ko_name: str):
    """
    Checks if all provided characters exist.

    Args:
        living_characters (object): Characters to validate.

    Returns:
        bool: True if all exist, False otherwise.
    """
    for place in place_list:
        if place.placeNameKo == ko_name:
            return place.placeNameEn
    return "Not Found"


# IO
def generate_victim_input(victim_generation_data):
    """
    Generates input data required for victim generation in both JSON format and Pydantic model format.
    Validates the existence of characters involved and selects random characters for victim and witness roles.

    Args:
        victim_generation_data (object): Data structure containing information for victim generation.

    Returns:
        Tuple containing input data in JSON format and Pydantic model format, or (None, None) if validation fails.
    """
    muderer_info = get_character_criminal_scenario(victim_generation_data.murderer)

    crime_scene = select_crime_scene(place_data.places)
    victim = select_random_character(victim_generation_data.livingCharacters, victim_generation_data.murderer)

    excluded_characters = [victim_generation_data.murderer, victim.name]
    witness = select_random_character(victim_generation_data.livingCharacters, excluded_characters)
    
    living_characters_info = get_characters_info(victim_generation_data.livingCharacters, excluded_characters)
    living_characters_info = [{
            "name": living_character.name, 
            "personalityDescription": living_character.personalityDescription,
            "featureDescription": living_character.featureDescription,
            } for living_character in living_characters_info]
    
    input_data_json = {
        "information": {
            "day": victim_generation_data.day,
            "murderer": {
                "name": victim_generation_data.murderer,
                "motivation": muderer_info.motivation,
                "procedure": muderer_info.procedure,
                },
            "crimeScene": crime_scene.placeNameKo,
            "method": "칼",
            "victim": victim.name,
            "witness": witness.name,
            "livingCharacters": living_characters_info,
            "previousStory": victim_generation_data.previousStory
        }
    }
    input_data_pydantic = scenario_crud_schema.VictimGenerationContainer(**input_data_json)
    return input_data_json, input_data_pydantic

def generate_victim_output(answer, input_data, origin_data):
    """
    Processes the results of the victim generation scenario, producing output data in JSON format.

    Args:
        answer (object): The output from the victim generation process.
        input_data (object): The input data used for generating the scenario.
        origin_data (object): The original data structure containing characters' information.

    Returns:
        JSON formatted output data based on the scenario generation results.
    """
    game_npc_no_mapping = {character.name : character.gameNpcNo for character in origin_data.livingCharacters}

    alibi_list = [{
                "name": alibi.name,
                "alibi": alibi.alibi,
                "gameNpcNo": game_npc_no_mapping[alibi.name]
                } for alibi in answer.alibis if alibi.name in game_npc_no_mapping]
    
    crimeScene_en = translate_place_name_ko_to_en(place_data.places, input_data.information.crimeScene)
    
    output_data_json = {
        "victim": input_data.information.victim,
        "crimeScene": crimeScene_en,
        "method": input_data.information.method,
        "witness": input_data.information.witness,
        "eyewitnessInformation": answer.eyewitnessInformation,
        "dailySummary": answer.dailySummary,
        "alibis": alibi_list
    }

    return output_data_json

def generate_final_words_input(final_words_generation_data):
    """
    Prepares input data for final words generation in a game scenario. It checks for the murderer's criminal
    scenario details and constructs input data in JSON and Pydantic model formats. If the murderer's details
    are missing, it returns (None, None) to signal failure.

    Args:
        final_words_generation_data (object): Contains information for final words generation, including the
                                               murderer's name, game result, and previous story.

    Returns:
        Tuple (input_data_json, input_data_pydantic): JSON and Pydantic formatted data for final words generation,
                                                      or (None, None) if critical information is missing.
    """
    muderer_info = get_character_criminal_scenario(final_words_generation_data.murderer)
    if not muderer_info:
        return None, None
    
    input_data_json = {
        "information": {
            "murderer": {
                "name": final_words_generation_data.murderer,
                "motivation": muderer_info.motivation,
                "procedure": muderer_info.procedure,
                },
            "gameResult": final_words_generation_data.gameResult,
            "previousStory": final_words_generation_data.previousStory
        }
    }
    input_data_pydantic = scenario_crud_schema.FinalWordsGenerationContainer(**input_data_json)
    return input_data_json, input_data_pydantic
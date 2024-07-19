import random

from ..schemas import scenario_crud_schema
from ..lib import const

characters_data = scenario_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = scenario_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name: str):
    """
    캐릭터 이름으로 캐릭터 정보를 가져옵니다.
    캐릭터가 존재하지 않으면 None을 반환합니다.

    Args:
        name (str): 찾고자 하는 캐릭터의 이름.

    Returns:
        캐릭터 객체 또는 찾지 못한 경우 None.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def get_character_criminal_scenario(name: str):
    """
    주어진 이름의 캐릭터에 대한 범죄 시나리오 세부 정보를 가져옵니다.
    일치하는 캐릭터를 찾지 못한 경우 None을 반환합니다.

    Args:
        name (str): 범죄 시나리오를 찾고자 하는 캐릭터의 이름.

    Returns:
        CriminalScenario 객체 또는 찾지 못한 경우 None.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character.criminalScenario
    return None

def select_crime_scene(place_data: list):
    """
    가능한 장소 목록에서 무작위로 범죄 현장을 선택합니다.

    Args:
        place_data (list): 잠재적인 범죄 현장이 포함된 데이터 구조.

    Returns:
        무작위로 선택된 Place 객체.
    """
    return random.choice(place_data)

def select_random_character(candidates: list, excluded_characters: list):
    """
    지정된 캐릭터를 제외하고 목록에서 무작위로 캐릭터를 선택합니다.

    Args:
        candidates (list): 선택할 후보 캐릭터 목록.
        excluded_characters (list): 선택에서 제외할 캐릭터 이름 목록.

    Returns:
        무작위로 선택된 Character 객체 또는 유효한 캐릭터가 없는 경우 None.
    """
    filtered_candidates = [character.name for character in candidates if character.name not in excluded_characters]

    valid_characters = [get_character_info(character) for character in filtered_candidates if get_character_info(character)]

    if valid_characters:
        return random.choice(valid_characters)
    return None

def get_characters_info(candidates: list, excluded_characters: list):
    """
    지정된 캐릭터를 제외하고 캐릭터 목록에 대한 정보를 가져옵니다.

    Args:
        candidates (list): 정보 가져올 후보 캐릭터 목록.
        excluded_characters (list): 가져오기를 제외할 캐릭터 이름 목록.

    Returns:
        지정된 캐릭터를 제외한 상세 정보를 가진 Character 객체 목록.
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
    생존 캐릭터 목록에 있는 모든 캐릭터가 캐릭터 데이터에 존재하는지 확인합니다.

    Args:
        living_characters (list): 확인할 캐릭터 이름 목록.

    Returns:
        bool: 모든 캐릭터가 존재하면 True, 그렇지 않으면 False.
    """
    living_characters_names = [character.name for character in living_characters]
    for character_name in living_characters_names:
        if not get_character_info(character_name):
            return False
    return True

def translate_place_name_ko_to_en(place_list: list, ko_name: str):
    """
    제공된 장소 이름의 한국어를 영어로 번역합니다.

    Args:
        place_list (list): 장소 목록.
        ko_name (str): 번역할 장소의 한국어 이름.

    Returns:
        영어 이름 또는 찾지 못한 경우 "Not Found".
    """
    for place in place_list:
        if place.placeNameKo == ko_name:
            return place.placeNameEn
    return "Not Found"


# IO
def generate_victim_input(victim_generation_data):
    """
    피해자 생성을 위해 필요한 입력 데이터를 JSON 형식과 Pydantic 모델 형식으로 생성합니다.
    관련된 캐릭터의 존재 여부를 확인하고 피해자와 목격자 역할을 위한 무작위 캐릭터를 선택합니다.

    Args:
        victim_generation_data (object): 피해자 생성에 필요한 정보를 포함하는 데이터 구조.

    Returns:
        JSON 형식 및 Pydantic 모델 형식의 입력 데이터 튜플 또는 검증 실패 시 (None, None).
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
    피해자 생성 시나리오 결과를 처리하여 JSON 형식의 출력 데이터를 생성합니다.

    Args:
        answer (object): 피해자 생성 프로세스의 출력.
        input_data (object): 시나리오 생성을 위해 사용된 입력 데이터.
        origin_data (object): 캐릭터 정보를 포함하는 원본 데이터 구조.

    Returns:
        시나리오 생성 결과를 기반으로 한 JSON 형식의 출력 데이터.
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
    게임 시나리오에서 마지막 말을 생성하기 위한 입력 데이터를 준비합니다.
    살인자의 범죄 시나리오 세부 정보를 확인하고 JSON 및 Pydantic 모델 형식으로 입력 데이터를 구성합니다.
    살인자의 세부 정보가 누락된 경우, (None, None)을 반환하여 실패를 신호합니다.

    Args:
        final_words_generation_data (object): 살인자의 이름, 게임 결과, 이전 이야기 등을 포함한 마지막 말 생성 정보를 포함하는 객체.

    Returns:
        최종 말 생성용 JSON 및 Pydantic 형식의 데이터 튜플 또는 중요한 정보가 누락된 경우 (None, None).
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

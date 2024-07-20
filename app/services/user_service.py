from ..schemas import user_crud_schema
from ..lib import const

characters_data = user_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = user_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name):
    """
    로드된 캐릭터 데이터에서 이름으로 캐릭터 정보를 가져옵니다.

    Args:
        name (str): 정보를 가져올 캐릭터의 이름.

    Returns:
        찾은 경우 캐릭터 객체, 그렇지 않으면 None.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def format_previous_chat_contents(conversation_user_schema):
    """
    주어진 대화 스키마에 대해 이전 채팅 내용을 형식화하며, MAX_CHAT_CONTENTS로 정의된 가장 최근 항목들로 제한합니다.

    Args:
        conversation_user_schema (object): 이전 채팅 내용을 포함하는 대화 스키마.

    Returns:
        보낸 사람 유형, 이름 및 내용을 포함하는 사전 형식의 채팅 내용 목록.
    """
    formatted_chat_contents = []
    for chat_content in conversation_user_schema.previousChatContents[-const.MAX_CHAT_CONTENTS:]:
        chat_content_dict = {
            "type": "user" if chat_content.sender == conversation_user_schema.sender else "character",
            "name": chat_content.sender,
            "content": chat_content.chatContent
        }
        formatted_chat_contents.append(chat_content_dict)
    return formatted_chat_contents

def validate_npc_names(living_characters):
    """
    생존 캐릭터 목록에 있는 모든 캐릭터가 캐릭터 데이터에 존재하는지 확인합니다.

    Args:
        living_characters (list): 검증할 캐릭터 이름 목록.

    Returns:
        bool: 모든 캐릭터가 존재하면 True, 그렇지 않으면 False.
    """
    for character_name in living_characters:
        if not get_character_info(character_name):
            return False
    return True

def conversation_with_user_input(conversation_user_schema):
    """
    사용자와의 대화를 위한 입력 데이터를 준비하며, 캐릭터 세부 정보 및 이전 채팅 내용을 포함하여 JSON 및 Pydantic 모델로 형식화합니다.

    Args:
        conversation_user_schema (object): 사용자와의 대화 정보를 포함하는 스키마.

    Returns:
        대화용 JSON 및 Pydantic 형식의 입력 데이터 튜플.
    """
    character_info = get_character_info(conversation_user_schema.receiver.name)

    previous_chat_contents_formatted = format_previous_chat_contents(conversation_user_schema)

    input_data_json = {
        "information": {
            "user": conversation_user_schema.sender,
            "character": {
                "name": character_info.name,
                "personalityDescription": character_info.personalityDescription,
                "featureDescription": character_info.featureDescription,
                "alibi": conversation_user_schema.receiver.alibi
            },
            "chatContent": conversation_user_schema.chatContent,
            "previousStory": conversation_user_schema.previousStory,
            "previousChatContents": previous_chat_contents_formatted
        }
    }
    input_data_pydantic = user_crud_schema.ConversationWithUserContainer(**input_data_json)
    return input_data_json, input_data_pydantic

def conversation_between_npc_input(conversation_npc_schema):
    """
    두 NPC 간의 대화를 위한 입력 데이터를 준비하며, JSON 및 Pydantic 모델로 형식화합니다.

    Args:
        conversation_npc_schema (object): 두 NPC 간의 대화 정보를 포함하는 스키마.

    Returns:
        NPC 대화용 JSON 및 Pydantic 형식의 입력 데이터 튜플.
    """
    character_info_1 = get_character_info(conversation_npc_schema.npcName1.name)
    character_info_2 = get_character_info(conversation_npc_schema.npcName2.name)

    input_data_json = {
        "information": {
            "character1": {
                "name": character_info_1.name,
                "personalityDescription": character_info_1.personalityDescription,
                "featureDescription": character_info_1.featureDescription,
                "alibi": conversation_npc_schema.npcName1.alibi
            },
            "character2": {
                "name": character_info_2.name,
                "personalityDescription": character_info_2.personalityDescription,
                "featureDescription": character_info_2.featureDescription,
                "alibi": conversation_npc_schema.npcName2.alibi
            },
            "previousStory": conversation_npc_schema.previousStory
        }
    }
    input_data_pydantic = user_crud_schema.ConversationBetweenNPCContainer(**input_data_json)
    return input_data_json, input_data_pydantic

def conversation_between_npc_each_input(conversation_npc_schema):
    """
    두 NPC 간의 대화를 위한 입력 데이터를 준비하며, 개별 응답 및 이전 채팅 내용을 포함하여 JSON 및 Pydantic 모델로 형식화합니다.

    Args:
        conversation_npc_schema (object): 두 NPC 간의 상세 대화 정보를 포함하는 스키마.

    Returns:
        상세 NPC 대화용 JSON 및 Pydantic 형식의 입력 데이터 튜플.
    """
    character_info_1 = get_character_info(conversation_npc_schema.npcName1.name)
    character_info_2 = get_character_info(conversation_npc_schema.npcName2.name)

    previous_chat_contents_formatted = format_previous_chat_contents(conversation_npc_schema)

    input_data_json = {
        "information": {
            "character1": {
                "name": character_info_1.name,
                "personalityDescription": character_info_1.personalityDescription,
                "featureDescription": character_info_1.featureDescription,
                "alibi": conversation_npc_schema.npcName1.alibi
            },
            "character2": {
                "name": character_info_2.name,
                "personalityDescription": character_info_2.personalityDescription,
                "featureDescription": character_info_2.featureDescription,
                "alibi": conversation_npc_schema.npcName2.alibi
            },
            "previousStory": conversation_npc_schema.previousStory,
            "previousChatContents": previous_chat_contents_formatted
        }
    }
    input_data_pydantic = user_crud_schema.ConversationBetweenNPCEachContainer(**input_data_json)
    return input_data_json, input_data_pydantic

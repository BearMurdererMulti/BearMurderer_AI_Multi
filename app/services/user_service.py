from ..schemas import user_crud_schema
from ..lib import const

characters_data = user_crud_schema.CharactersSchema(**const.CHARACTERS)
place_data = user_crud_schema.PlacesSchema(**const.PLACES)


def get_character_info(name):
    """
    Retrieves character information by name from the loaded character data.

    Args:
        name (str): Name of the character to retrieve information for.

    Returns:
        Character object if found, otherwise None.
    """
    for character in characters_data.npcs:
        if character.name == name:
            return character
    return None

def format_previous_chat_contents(conversation_user_schema):
    """
    Formats previous chat contents for a given conversation schema, limiting to the most recent entries as defined by MAX_CHAT_CONTENTS.

    Args:
        conversation_user_schema (object): The conversation schema containing previous chat contents.

    Returns:
        List of dictionaries with formatted chat content, including sender type, name, and content.
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
    Validates that all characters in the living characters list exist in the characters data.

    Args:
        living_characters (list): List of character names to validate.

    Returns:
        bool: True if all characters exist, False otherwise.
    """
    for character_name in living_characters:
        if not get_character_info(character_name):
            return False
    return True

def conversation_with_user_input(conversation_user_schema):
    """
    Prepares input data for a conversation with a user, including character details and previous chat content, formatted as JSON and a Pydantic model.

    Args:
        conversation_user_schema (object): Schema containing conversation information with a user.

    Returns:
        Tuple (input_data_json, input_data_pydantic): JSON and Pydantic formatted input data for the conversation.
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
    Prepares input data for a conversation between two NPCs, formatted as JSON and a Pydantic model.

    Args:
        conversation_npc_schema (object): Schema containing conversation information between two NPCs.

    Returns:
        Tuple (input_data_json, input_data_pydantic): JSON and Pydantic formatted input data for the NPC conversation.
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
    Prepares input data for a conversation between two NPCs, including their individual responses and previous chat content, formatted as JSON and a Pydantic model.

    Args:
        conversation_npc_schema (object): Schema containing detailed conversation information between two NPCs.

    Returns:
        Tuple (input_data_json, input_data_pydantic): JSON and Pydantic formatted input data for detailed NPC conversation.
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
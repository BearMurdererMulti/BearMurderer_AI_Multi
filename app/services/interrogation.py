import random
import json
from app.utils.gpt_helper import get_gpt_response
from app.utils.memory import add_conversation, get_conversation_chain
from app.utils.game_utils import (
    create_context,
    get_name,
    get_personality_detail,
    get_feature_detail,
    get_weapon_name,
    get_location_name
)
from app.core.logger_config import setup_logger
logger = setup_logger()

class Interrogation:
    def __init__(self, game_state, personalities, features, weapons, places, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.names = names

    def start_interrogation(self, npc_name, weapon):
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], self.game_state["language"], self.names) == npc_name), None)
        weapon_en = next((w['id'] for w in self.weapons if w['weapon']['ko'] == weapon), None)

        heart_rate = 60
        if weapon_en in npc['preferredWeapons']:
            heart_rate = 80

        self.game_state['interrogation'] = {
            "heart_rate": heart_rate,
            "suspect_name": npc_name,
            "weapon": weapon,
            "conversation_history": []
            }

    def generate_interrogation_response(self, npc_name: str, content: str):
        logger.info(f"▶️  User message received: npc_name: {npc_name}, contents: {content}")

        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], self.game_state["language"], self.names) == npc_name), None)

        conversation_history = self.game_state['interrogation']['conversation_history']
        formatted_conversation_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])

        current_heart_rate = self.game_state['interrogation']['heart_rate']
        # print(f"current_heart_rate: {current_heart_rate}")

        response_prompt = (
            f"Based on the conversation history below, generate a response in {self.game_state['language']} "
            f"for an NPC named {npc_name} who has the personality '{npc['personality']}' and the feature '{npc['feature']}'. "
            f"The NPC is currently being interrogated, accused of being the murderer in the village. "
            f"The NPC's current heart rate is {current_heart_rate} bpm. The NPC's heart rate changes depending on the sharpness of the question. "
            f"Sharp questions will increase the heart rate, while irrelevant questions will decrease it. "
            f"The change in heart rate (delta) ranges from -10 to +10 bpm but cannot be 0. The delta must be at least -1 or +1. "
            f"If the heart rate is below 80, respond in a dismissive and arrogant manner with a short answer. "
            f"If the heart rate is between 80 and 120, respond normally and cooperatively. "
            f"If the heart rate is above 120, refuse to answer and show signs of distress. "
            f"The response should clearly reflect their personality and feature. "
            f'The murdered person was {self.game_state["murdered_npc"]}, the murder weapon was {self.game_state["murder_weapon"]}, and the murder took place at {self.game_state["murder_location"]}. '
            f'Provide the response in the format(json): {{"response": str, "heartRateDelta": int}}\n\n'
            f"Conversation History:\n{formatted_conversation_history}\n\n"
            f"The NPC is asked: '{content}'"
        )

        response_content = get_gpt_response(response_prompt, max_tokens=150)
        response = json.loads(response_content)


        current_heart_rate += int(response['heartRateDelta'])
        current_heart_rate = 130 if current_heart_rate > 130 else current_heart_rate
        current_heart_rate = 60 if current_heart_rate < 60 else current_heart_rate
        self.game_state['interrogation']['heart_rate'] = current_heart_rate

        conversation_history.append({"role": "user", "content": content})
        conversation_history.append({"role": npc_name, "content": response_content})

        logger.info(f"▶️  Bot response sent: npc_name: {npc_name}, heart_rate: {current_heart_rate}, response: {response['response']}")
        return {"response": response['response'], "heartRate": current_heart_rate}

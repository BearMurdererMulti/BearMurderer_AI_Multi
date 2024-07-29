import random
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

# NPC 대화 생성
class QuestionGeneration:
    def __init__(self, game_state, personalities, features, weapons, places, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.names = names

    # NPC에게 질문을 생성하는 메서드
    def generate_questions(self, npc_name, keyword=None, keyword_type=None):
        if 'scenario' not in self.game_state:
            self.game_state['scenario'] = {}

        lang = self.game_state["language"]
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        if not npc:
            raise ValueError("NPC not found")

        personality_key = npc["personality"]
        feature_key = npc["feature"]

        personality = next((p for p in self.personalities if p["id"] == personality_key), None)
        feature = next((f for f in self.features if f["id"] == feature_key), None)

        if personality is None or feature is None:
            raise ValueError("Personality or feature not found in NPC data")

        scenario_description = self.game_state["scenario"].get("description", "")

        # 범행 시간에 대한 알리바이 질문 생성
        alibi_question_prompt = (
            f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
            f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
            f"Ask about their alibi for the time of the murder."
        )

        # 키워드가 있을 때
        if keyword and keyword_type:
            # 키워드가 무기 일때
            if keyword_type == "weapon":
                weapon_question_prompt = (
                    f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                    f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                    f"Ask them about their knowledge or possession of the weapon '{keyword}'."
                )
                location_question_prompt = (
                    f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                    f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                    f"Ask them about their preferred locations."
                )
            # 키워드가 장소 일때
            elif keyword_type == "place":
                location_question_prompt = (
                    f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                    f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                    f"Ask them about their connection to the location '{keyword}'."
                )
                weapon_question_prompt = (
                    f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                    f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                    f"Ask them about their preferred weapons."
                )
        # 키워드가 없을 때
        else:
            weapon_question_prompt = (
                f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                f"Ask them about their preferred weapons."
            )
            location_question_prompt = (
                f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                f"Ask them about their preferred locations."
            )

        alibi_question = get_gpt_response(alibi_question_prompt, max_tokens=80)
        weapon_question = get_gpt_response(weapon_question_prompt, max_tokens=80)
        location_question = get_gpt_response(location_question_prompt, max_tokens=80)

        questions = [
            {"number": 1, "question": alibi_question},
            {"number": 2, "question": weapon_question},
            {"number": 3, "question": location_question}
        ]

        self.game_state["current_questions"] = questions
        return questions

    # NPC와 대화를 진행하는 메서드
    def talk_to_npc(self, npc_name, question_index, keyword=None, keyword_type=None):
        if "current_questions" not in self.game_state:
            raise ValueError("No questions generated")

        question = self.game_state["current_questions"][question_index - 1]["question"]
        conversation_chain = get_conversation_chain()

        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], self.game_state["language"], self.names) == npc_name), None)
        if not npc:
            raise ValueError("NPC not found")

        if 'scenario' not in self.game_state:
            self.game_state['scenario'] = {}

        scenario_description = self.game_state["scenario"].get("description", "")

        # 범행 도구에 대한 질문이고 키워드가 무기 일때
        if question_index == 2 and keyword and keyword_type == "weapon":
            # 키워드가 NPC의 선호하는 무기 중 하나일 경우 그 무기에 대한 대답을 생성
            if any(get_weapon_name(wpn, self.weapons, self.game_state["language"]) == keyword for wpn in npc["preferredWeapons"]):
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the weapon '{keyword}' which they like and use often. The response should clearly indicate their preference for this weapon."
                )
            # 키워드가 NPC의 선호하는 무기 중 하나가 아닐 경우 그 무기에 대한 대답을 생성
            else:
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the weapon '{keyword}' which they dislike or rarely use. The response should clearly indicate their lack of preference for this weapon."
                )
        # 범행 장소에 대한 질문이고 키워드가 장소 일때
        elif question_index == 3 and keyword and keyword_type == "place":
            # 키워드가 NPC의 선호하는 장소 중 하나일 경우 그 장소에 대한 대답을 생성
            if any(get_location_name(loc, self.places, self.game_state["language"]) == keyword for loc in npc["preferredLocations"]):
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the location '{keyword}' which they like and visit often. The response should clearly indicate their preference for this place."
                )
            # 키워드가 NPC의 선호하는 장소 중 하나가 아닐 경우 그 장소에 대한 대답을 생성
            else:
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the location '{keyword}' which they dislike or rarely visit. The response should clearly indicate their lack of preference for this place."
                )
        else:
            # 범행 장소에 대한 질문이고 키워드가 없을 때나 키워드가 범행 도구일 경우 선호하는 장소 중 하나를 선택하여 응답하도록 함
            if question_index == 3 and (not keyword or keyword_type == "weapon"):
                preferred_location = random.choice(npc["preferredLocations"])
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about their preferred locations. "
                    f"The response should include their preference for '{get_location_name(preferred_location, self.places, self.game_state['language'])}'."
                )
            # 범행 도구에 대한 질문이고 키워드가 없을 때나 키워드가 범행 장소일 경우 선호하는 무기 중 하나를 선택하여 응답하도록 함
            elif question_index == 2 and (not keyword or keyword_type == "place"):
                preferred_weapon = random.choice(npc["preferredWeapons"])
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about their preferred weapons. "
                    f"The response should include their preference for '{get_weapon_name(preferred_weapon, self.weapons, self.game_state['language'])}'."
                )
            else:
                # 그 외의 경우에는 일반적인 대화를 생성
                response_prompt = (
                    f"Generate a concise response in {self.game_state['language']} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked: '{question}'. The response should clearly indicate their personality and feature."
                )

        response_content = get_gpt_response(response_prompt, max_tokens=150)

        add_conversation(question, response_content)
        self.game_state["conversations_left"] -= 1

        return response_content

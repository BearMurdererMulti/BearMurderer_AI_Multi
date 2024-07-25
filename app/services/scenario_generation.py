import random
from app.utils.gpt_helper import get_gpt_response
from app.utils.game_utils import (
    create_context,
    get_feature_detail,
    get_name,
    get_personality_detail
)

# 게임 시나리오 생성
class ScenarioGeneration:
    def __init__(self, game_state, personalities, features, weapons, places, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.names = names

    # 초기 게임 시나리오를 생성하는 메서드
    def create_initial_scenario(self):
        lang = self.game_state["language"]
        context = create_context(self.game_state, self.personalities, self.features, self.weapons, self.places, self.names)
        
        # 선택된 NPC들로 시나리오를 생성하도록 설정
        selected_npcs = random.sample(self.game_state["npcs"], min(5, len(self.game_state["npcs"])))
        npc_descriptions = "\n".join(
            [f"{idx+1}. **{get_name(npc['name'], lang, self.names)}** - {get_personality_detail(npc['personality'], self.personalities, lang)}, {get_feature_detail(npc['feature'], self.features, lang)}."
            for idx, npc in enumerate(selected_npcs)]
        )

        # 시나리오 생성
        prompt = (
            f"Create a detailed story in {lang} for a murder mystery game set in the village of Bear Town. "
            f"The story should include only the following characters and their interactions:\n\n{npc_descriptions}\n\n"
            f"The murder victim is {context['murdered_npc']['name']} who was killed with {context['murder_weapon']} at {context['murder_location']}. "
            f"The story should be intriguing and provide depth to each character's background and potential motives, without revealing the murderer. "
            f"Write the story in {lang}."
        )

        scenario_description = get_gpt_response(prompt, max_tokens=500)

        return {
            "description": scenario_description
        }

    # 게임 진행 중 시나리오를 생성하는 메서드
    def create_progress_scenario(self):
        lang = self.game_state["language"]
        previous_scenarios = self.game_state.get('scenarios', [])
        previous_scenarios_text = "\n".join(previous_scenarios)
        
        new_victim = self.game_state["murdered_npcs"][-1]["name"]
        new_weapon = self.game_state["murder_weapons"][-1]
        new_location = self.game_state["murder_locations"][-1]
        
        selected_npcs = random.sample(self.game_state["npcs"], min(5, len(self.game_state["npcs"])))
        npc_descriptions = "\n".join(
            [f"{idx+1}. **{get_name(npc['name'], lang, self.names)}** - {get_personality_detail(npc['personality'], self.personalities, lang)}, {get_feature_detail(npc['feature'], self.features, lang)}."
            for idx, npc in enumerate(selected_npcs)]
        )

        prompt = (
            f"Create a detailed story in {lang} for a murder mystery game set in the village of Bear Town. "
            f"The story so far is as follows:\n\n{previous_scenarios_text}\n\n"
            f"On the {self.get_day_description(self.game_state['current_day'], lang)}, another murder has occurred. "
            f"The new victim is {new_victim}, who was killed with {new_weapon} at {new_location}. "
            f"The story should continue to be intriguing and provide depth to each character's background and potential motives, without revealing the murderer. "
            f"Include only the following characters and their interactions:\n\n{npc_descriptions}\n\n"
            f"Write the story in {lang}."
        )

        scenario_description = get_gpt_response(prompt, max_tokens=500)
        self.game_state.setdefault('scenarios', []).append(scenario_description)

        return {
            "description": scenario_description
        }

    def get_day_description(self, day, lang):
        day_descriptions_ko = ["첫째날", "둘째날", "셋째날", "넷째날", "다섯째날"]
        day_descriptions_en = ["first day", "second day", "third day", "fourth day", "fifth day"]

        if lang == "ko":
            return f"{day_descriptions_ko[day - 1]} 아침"
        else:
            return f"the {day_descriptions_en[day - 1]} morning"

    # 촌장의 편지를 생성하는 메서드
    def generate_chief_letter(self):
        lang = self.game_state["language"]
        context = create_context(self.game_state, self.personalities, self.features, self.weapons, self.places, self.names)

        prompt = (
            f"Write a brief letter in {lang} from the village chief to a detective, requesting help with solving a recent murder in Bear Town. "
            f"The letter should be concise and not reveal any details about the suspects, the murder weapon, or the location of the murder. "
            f"Sign the letter as '촌장 올림'."
        )

        chief_letter = get_gpt_response(prompt, max_tokens=250)

        return {
            "letter": chief_letter
        }

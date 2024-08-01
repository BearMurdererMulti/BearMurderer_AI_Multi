import random
import json
import re
from app.utils.gpt_helper import get_gpt_response
from app.utils.game_utils import (
    create_context,
    get_feature_detail,
    get_name,
    get_weapon_name,
    get_location_name,
    get_personality_detail,
    get_feature_detail
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

        scenario_description = get_gpt_response(prompt, max_tokens=1000)

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

        scenario_description = get_gpt_response(prompt, max_tokens=1000)
        self.game_state.setdefault('scenarios', []).append(scenario_description)

        return {
            "description": scenario_description
        }

    # 시나리오에 날짜 삽입
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

        if lang == "ko":
            closing_example = "베어 타운 촌장 올림"
        else:
            closing_example = "Sincerely, Village Chief of Bear Town"

        prompt = f"""
        Write a brief, urgent letter in {lang} from the village chief to a detective, desperately requesting help with solving a recent murder in Bear Town.
        The letter should be concise but convey a sense of fear, urgency, and desperation. Do not reveal any details about the suspects, the murder weapon, or the location of the murder.
        Structure the letter in three parts:
        1. Greeting: A formal but urgent salutation to the detective.
        2. Content: The main body of the letter explaining the dire situation, the fear gripping the village, and pleading for immediate help. Emphasize the potential for more danger if help doesn't arrive soon.
        3. Closing: A desperate closing plea, followed by a signature similar to "{closing_example}" but not necessarily identical.

        Return the letter in the following format, without any additional formatting or code blocks:
        {{
            "greeting": "Urgent greeting text here",
            "content": "Desperate main content of the letter here",
            "closing": "Final plea and signature here"
        }}
        """

        chief_letter = get_gpt_response(prompt, max_tokens=300)

        # Remove any code block formatting
        chief_letter = re.sub(r'```json\s*|\s*```', '', chief_letter)

        try:
            letter_parts = json.loads(chief_letter)
        except json.JSONDecodeError:
            # If parsing fails, we'll use a simple split method as fallback
            parts = chief_letter.split("\n")
            letter_parts = {
                "greeting": parts[0] if len(parts) > 0 else "",
                "content": " ".join(parts[1:-1]) if len(parts) > 2 else "",
                "closing": parts[-1] if len(parts) > 1 else closing_example
            }

        return letter_parts

    # 알리바이와 목격자 정보를 생성하는 메서드
    def generate_alibis_and_witness(self):
        lang = self.game_state["language"]
        alive_npcs = [npc for npc in self.game_state["npcs"] if self.game_state['alive'][npc['name']]]
        victim_name = get_name(self.game_state["murdered_npc"]["name"], lang, self.names)
        murder_location = get_location_name(self.game_state["murder_location"], self.places, lang)
        murder_weapon = get_weapon_name(self.game_state["murder_weapon"], self.weapons, lang)

        # 목격자 선택
        witness = random.choice(alive_npcs)
        witness_name = get_name(witness['name'], lang, self.names)
        
        alibis = {}
        for npc in alive_npcs:
            npc_name = get_name(npc['name'], lang, self.names)
            personality = get_personality_detail(npc['personality'], self.personalities, lang)
            feature = get_feature_detail(npc['feature'], self.features, lang)
            
            if npc == witness:
                prompt = f"""
                As an eyewitness in a murder mystery game set in Bear Town, create a brief account in {lang}.
                You are {npc_name}, with the personality trait of being {personality} and the feature of {feature}.
                You witnessed the murder of {victim_name} at {murder_location}.
                Your account should:
                1. Be vague about the killer's identity
                2. Mention something unusual you noticed
                3. Reflect your personality and feature in your statement
                4. Be no longer than 3 sentences

                Respond only with the eyewitness account, without any additional text.
                """
                eyewitness_info = get_gpt_response(prompt, max_tokens=150)
                self.game_state['witness'] = {
                    'name': npc_name,
                    'information': eyewitness_info
                }
                alibis[npc_name] = f"{eyewitness_info}"
            else:
                prompt = f"""
                Create a brief alibi in {lang} for an NPC named {npc_name} in a murder mystery game set in Bear Town.
                The murder of {victim_name} occurred at {murder_location} using {murder_weapon}.
                {npc_name} has the personality trait of being {personality} and the feature of {feature}.
                The alibi should:
                1. Be plausible but vague
                2. Not provide a solid alibi for the time of the murder
                3. Reflect the NPC's personality and feature
                4. Be no longer than 2 sentences

                Respond only with the alibi, without any additional text.
                """
                alibi = get_gpt_response(prompt, max_tokens=100)
                alibis[npc_name] = alibi

        self.game_state['alibis'] = alibis

        return {
            "witness": self.game_state['witness'],
            "alibis": alibis
        }

    def update_game_state_with_murder(self):
        lang = self.game_state["language"]
        remaining_npcs = [npc for npc in self.game_state['npcs'] if self.game_state['alive'][npc['name']]]
        if len(remaining_npcs) <= 2:
            raise ValueError("Not enough NPCs to continue the game")

        new_victim = random.choice(remaining_npcs)
        for npc in self.game_state["npcs"]:
            if npc["name"] == new_victim["name"]:
                self.game_state['alive'][npc['name']] = False
                break
        self.game_state['murdered_npcs'].append({"name": new_victim['name'], "order": self.game_state['current_day'] + 1})

        # 새로운 범행 도구와 장소를 할당
        murderer = self.game_state['murderer']
        new_weapon = random.choice(murderer["preferredWeapons"])
        new_location = random.choice(murderer["preferredLocations"])
        if 'murder_weapons' not in self.game_state:
            self.game_state['murder_weapons'] = [new_weapon]
        else:
            self.game_state['murder_weapons'].append(new_weapon)
        if 'murder_locations' not in self.game_state:
            self.game_state['murder_locations'] = [new_location]
        else:
            self.game_state['murder_locations'].append(new_location)

        self.game_state['current_day'] += 1

        return {
            "victim": get_name(new_victim['name'], lang, self.names),
            "method": get_weapon_name(new_weapon, self.weapons, lang),
            "crimeScene": get_location_name(new_location, self.places, lang),
            "current_day": self.game_state['current_day']
        }

    def proceed_to_next_day(self):
        murder_summary = self.update_game_state_with_murder()
        alibis_and_witness = self.generate_alibis_and_witness()
        
        lang = self.game_state["language"]
        victim_name = get_name(self.game_state["murdered_npc"]["name"], lang, self.names)
        crime_scene = get_location_name(self.game_state["murder_location"], self.places, lang)
        murder_weapon = get_weapon_name(self.game_state["murder_weapon"], self.weapons, lang)
        
        daily_summary = f"day {self.game_state['current_day']} - {crime_scene}에서 {victim_name}이(가) {murder_weapon}에 의해 살해됨."
        
        result = {
            "answer": {
                "victim": victim_name,
                "crimeScene": crime_scene,
                "method": murder_weapon,
                "witness": alibis_and_witness["witness"]["name"],
                "eyewitnessInformation": alibis_and_witness["witness"]["information"],
                "dailySummary": daily_summary,
                "alibis": [{"name": name, "alibi": alibi} for name, alibi in alibis_and_witness["alibis"].items()]
            }
        }
        
        # new_scenario = self.create_progress_scenario()
        # result["answer"]["scenario"] = new_scenario
        
        return result
    
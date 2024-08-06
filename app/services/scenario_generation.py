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

        # 목격자 선택 (범인 제외)
        potential_witnesses = [npc for npc in alive_npcs if npc['name'] != self.game_state['murderer']['name']]
        witness = random.choice(potential_witnesses)
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
            elif npc['name'] == self.game_state['murderer']['name']:
                prompt = f"""
                Create a convincing alibi in {lang} for the murderer {npc_name} in a murder mystery game set in Bear Town.
                {npc_name} has the personality trait of being {personality} and the feature of {feature}.
                The alibi should:
                1. Be plausible and avoid any connection to the crime scene ({murder_location})
                2. Reflect the NPC's personality and feature
                3. Be detailed enough to seem credible
                4. Be no longer than 3 sentences

                Respond only with the alibi, without any additional text.
                """
            else:
                prompt = f"""
                Create a brief alibi in {lang} for an NPC named {npc_name} in a murder mystery game set in Bear Town.
                {npc_name} has the personality trait of being {personality} and the feature of {feature}.
                The alibi should:
                1. Be plausible and can be related to any location or activity
                2. Not necessarily provide a solid alibi for the time of the murder
                3. Reflect the NPC's personality and feature
                4. Be no longer than 2 sentences

                Respond only with the alibi, without any additional text.
                """
            
            if npc != witness:
                alibi = get_gpt_response(prompt, max_tokens=100)
                alibis[npc_name] = alibi

        self.game_state['alibis'] = alibis

        return {
            "witness": self.game_state['witness'],
            "alibis": alibis
        }

    def update_game_state_with_murder(self):
        lang = self.game_state["language"]
        
        print("Current npcs:", [get_name(npc['name'], 'ko', self.names) for npc in self.game_state['npcs']])
        print("Current alive:", {get_name(name, 'ko', self.names): status for name, status in self.game_state['alive'].items()})
        
        remaining_npcs = [npc for npc in self.game_state['npcs'] if self.game_state['alive'][npc['name']]]
        print("Remaining NPCs:", [get_name(npc['name'], 'ko', self.names) for npc in remaining_npcs])
        
        if len(remaining_npcs) <= 2:
            raise ValueError(f"Not enough NPCs to continue the game. Only {len(remaining_npcs)} NPCs left.")

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

    # 다음 날로 넘어가는 메서드
    def proceed_to_next_day(self, living_characters):
        print("Initial living_characters:", [npc['name'] for npc in living_characters])

        # 게임 상태 업데이트
        self.update_game_state(living_characters)

        # 새로운 피해자 선택
        self.select_new_victim()

        # 새로운 범행 도구와 장소 선택
        self.select_new_murder_details()

        # 게임 상태 추가 업데이트
        self.game_state['current_day'] += 1

        # 시나리오 생성 및 알리바이 생성
        murder_summary = self.create_murder_summary()
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

        return result

    def update_game_state(self, living_characters):
        for npc in self.game_state['npcs']:
            npc_korean_name = get_name(npc['name'], self.game_state['language'], self.names)
            living_npc = next((lc for lc in living_characters if lc['name'] == npc_korean_name), None)
            
            if living_npc:
                npc['alive'] = living_npc['status'] == "ALIVE"
            else:
                npc['alive'] = False
            
            self.game_state['alive'][npc['name']] = npc['alive']

        # NPC 목록 업데이트
        self.game_state['alive'][npc['name']] = npc['alive']
        print("Updated npcs:", [f"{get_name(npc['name'], self.game_state['language'], self.names)} - Alive: {npc['alive']}" for npc in self.game_state['npcs']])
        print("Updated alive:", self.game_state['alive'])

    def select_new_victim(self):
        murderer_id = self.game_state['murderer']['name']
        potential_victims = [npc for npc in self.game_state['npcs'] if npc['name'] != murderer_id and npc['alive']]
        
        if not potential_victims:
            raise ValueError("No potential victims left")

        new_victim = random.choice(potential_victims)
        new_victim['alive'] = False
        self.game_state['alive'][new_victim['name']] = False
        self.game_state['murdered_npc'] = new_victim
        self.game_state['murdered_npcs'].append({"name": new_victim['name'], "day": self.game_state['current_day'] + 1})

    def select_new_murder_details(self):
        self.game_state['murder_weapon'] = random.choice(self.game_state['murderer']["preferredWeapons"])
        self.game_state['murder_location'] = random.choice(self.game_state['murderer']["preferredLocations"])

    def create_murder_summary(self):
        # 이 메서드는 필요에 따라 구현하세요. 현재는 빈 딕셔너리를 반환합니다.
        return {}

    # 게임 생성 직후 첫번째 희생자를 반환하는 메서드
    def get_first_blood(self):
        lang = self.game_state["language"]
        victim_name = get_name(self.game_state['murdered_npc']["name"], lang, self.names)
        crime_scene = get_location_name(self.game_state["murder_location"], self.places, lang)
        murder_weapon = get_weapon_name(self.game_state["murder_weapon"], self.weapons, lang)

        result = {
            "victim": victim_name,
            "crimeScene": crime_scene,
            "method": murder_weapon,
        }
        return result

    # NPC 한글 이름을 ID로 변환하는 메서드
    def get_npc_id_by_korean_name(self, korean_name):
        for name in self.names:
            if name['name']['ko'] == korean_name:
                return name['id']
        print(f"Warning: No matching ID found for Korean name '{korean_name}'")
        return None

    # 편지 내용을 생성하고 형식을 맞추는 메서드
    def generate_letter(self, prompt, receiver, sender, max_tokens=300):
        content = get_gpt_response(prompt, max_tokens=max_tokens)
        
        letter_parts = {
            "receiver": f"{receiver}\n",
            "content": f"{content.strip()}\n",
            "sender": f"{sender}\n"
        }
        
        return letter_parts

    # 승리 시 촌장의 감사 편지를 생성하는 메서드
    def generate_chief_win_letter(self):
        lang = self.game_state["language"]
        receiver = "탐정" if lang == "ko" else "Detective"
        sender = "베어타운 촌장" if lang == "ko" else "Chief of Bear Town"

        prompt = f"""
        Write a thank you letter in {lang} from the village chief of Bear Town to the detective who solved the murder case.
        The letter should:
        1. Express deep gratitude for solving the case
        2. Mention the relief and joy of the villagers
        3. Invite the detective to visit again under better circumstances
        4. Be entirely in {'Korean' if lang == 'ko' else 'English'}
        5. Do not include any closing remarks like '올림' or 'Sincerely'
        """

        return self.generate_letter(prompt, receiver, sender)

    # 패배 시 촌장의 원망 편지를 생성하는 메서드
    def generate_chief_lose_letter(self):
        lang = self.game_state["language"]
        receiver = "탐정" if lang == "ko" else "Detective"
        sender = "베어타운 촌장" if lang == "ko" else "Chief of Bear Town"

        prompt = f"""
        Task: Write a disappointed and accusatory letter from the village chief to the detective who failed to solve the murder case.
        Language: {"Korean" if lang == "ko" else "English"}

        Letter requirements:
        1. Start with a cold and formal greeting
        2. Express deep disappointment and frustration about the detective's failure
        3. Emphasize the consequences of the detective's incompetence (e.g., more victims, widespread fear)
        4. Directly blame the detective for the continued suffering of the villagers
        5. Mention how the village trusted and depended on the detective, only to be let down
        6. Suggest that the detective's reputation will be ruined because of this failure
        7. End with a bitter and regretful tone, implying the detective should feel guilty
        8. Be 2-3 sentences long
        9. Do not include any closing remarks like '올림' or 'Sincerely'

        The letter should make the detective (player) feel responsible and guilty for failing the village.
        Do not include any explanations or additional text. Write only the letter content.
        """

        return self.generate_letter(prompt, receiver, sender)

    # 승리 시 생존자들의 감사 편지를 생성하는 메서드
    def generate_survivors_letter(self):
        lang = self.game_state["language"]
        murderer = self.game_state["murderer"]
        surviving_npcs = [npc for npc in self.game_state["npcs"] if self.game_state['alive'][npc['name']] and npc != murderer]
        dead_npcs = [npc for npc in self.game_state["npcs"] if not self.game_state['alive'][npc['name']] and npc != murderer]
        
        letters = []
        for npc in surviving_npcs:
            npc_name = get_name(npc['name'], lang, self.names)
            personality = get_personality_detail(npc['personality'], self.personalities, lang)
            feature = get_feature_detail(npc['feature'], self.features, lang)
            
            # 25% 확률로 죽은 NPC에게 편지 작성
            if random.random() < 0.25 and dead_npcs:
                dead_npc = random.choice(dead_npcs)
                dead_npc_name = get_name(dead_npc['name'], lang, self.names)
                receiver = dead_npc_name
                sender = npc_name
                prompt = f"""
                Write a short, deeply emotional letter in {lang} from {npc_name} to the deceased NPC {dead_npc_name}.
                The writer has the personality trait of being {personality} and the feature of {feature}.
                The letter should:
                1. Express profound grief and longing for the deceased friend
                2. Recall a specific, touching memory or shared experience
                3. Convey how much the deceased meant to the writer and the community
                4. Include a heartfelt wish or promise to honor the deceased's memory
                5. Reflect the writer's unique personality and feature in a subtle way
                6. Be entirely in {'Korean' if lang == 'ko' else 'English'}
                7. Be about 1-2 sentences long, each sentence filled with emotion
                8. Be so poignant that it might move readers to tears
                9. Do not include any closing remarks like '올림' or 'Sincerely'

                The letter should make the reader feel the depth of the writer's sorrow and the impact of the loss.
                """
            else:
                receiver = "탐정" if lang == "ko" else "Detective"
                sender = npc_name
                prompt = f"""
                Write a short thank you letter in {lang} from {npc_name} to the detective who solved the murder case.
                The NPC has the personality trait of being {personality} and the feature of {feature}.
                The letter should:
                1. Express gratitude and relief
                2. Mention how the detective's work has affected them personally
                3. Reflect the NPC's unique personality and feature
                4. Be entirely in {'Korean' if lang == 'ko' else 'English'}
                5. Be about 1-2 sentences long
                6. Do not include any closing remarks like '올림' or 'Sincerely'
                """
            
            letter = self.generate_letter(prompt, receiver, sender, max_tokens=150)
            letters.append({"name": sender, "letter": letter})
        
        return letters

    # 승리 시 범인의 협박 편지를 생성하는 메서드
    def generate_murderer_win_letter(self):
        lang = self.game_state["language"]
        murderer = self.game_state["murderer"]
        murderer_name = get_name(murderer['name'], lang, self.names)
        personality = get_personality_detail(murderer['personality'], self.personalities, lang)
        feature = get_feature_detail(murderer['feature'], self.features, lang)

        receiver = "탐정" if lang == "ko" else "Detective"
        sender = f"{murderer_name}" if lang == "ko" else f"{murderer_name}"

        prompt = f"""
        Task: Write a provocative and taunting letter from a caught murderer to the detective who solved the case.
        Murderer's name: {murderer_name}
        Murderer's personality: {personality}
        Murderer's unique feature: {feature}
        Language: {"Korean" if lang == "ko" else "English"}

        Letter requirements:
        1. Start with a mocking, sarcastic greeting that belittles the detective's achievement
        2. Express fake admiration for the detective's skills, but imply it was mostly luck
        3. Strongly emphasize the murderer's personality trait ({personality}) and unique feature ({feature}) in a way that shows they are superior to the detective
        4. Include at least one explicit threat of future revenge or hint at a bigger plan, even from prison
        5. Taunt the detective by revealing a disturbing detail about the crime that wasn't discovered
        6. End with a provocative statement that leaves the detective feeling uneasy and doubting their success
        7. Be 2-3 sentences long, each designed to irritate and unsettle the detective
        8. Do not include any closing remarks like '올림' or 'Sincerely'

        The letter should make the detective (player) feel angry, unsettled, and questioning their victory.
        Do not include any explanations or additional text. Write only the letter content.
        """

        return self.generate_letter(prompt, receiver, sender, max_tokens=250)

    # 패배 시 범인의 놀림 편지를 생성하는 메서드
    def generate_murderer_lose_letter(self):
        lang = self.game_state["language"]
        murderer = self.game_state["murderer"]
        murderer_name = get_name(murderer['name'], lang, self.names)
        personality = get_personality_detail(murderer['personality'], self.personalities, lang)
        feature = get_feature_detail(murderer['feature'], self.features, lang)

        receiver = "탐정" if lang == "ko" else "Detective"
        sender = f"{murderer_name}" if lang == "ko" else f"{murderer_name}"

        prompt = f"""
        Task: Write an extremely provocative and mocking letter from an escaped murderer to the detective who failed to solve the case.
        Murderer's name: {murderer_name}
        Murderer's personality: {personality}
        Murderer's unique feature: {feature}
        Language: {"Korean" if lang == "ko" else "English"}

        Letter requirements:
        1. Begin with an overly cheerful, sarcastic greeting that emphasizes the detective's failure
        2. Openly ridicule the detective's incompetence, using the murderer's personality ({personality}) to make it more insulting
        3. Boast about outsmarting the detective, incorporating the murderer's unique feature ({feature}) as a key to their success
        4. Include at least two taunts about future crimes the detective won't be able to stop, making them sound inevitable
        5. Mock the detective's investigation process, pointing out obvious clues they missed
        6. Hint at a larger conspiracy or plan that the detective is too incompetent to uncover
        7. End with a challenge or dare that makes the detective feel powerless and frustrated
        8. Be 2-3 sentences long, each crafted to maximally provoke and anger the detective
        9. Do not include any closing remarks like '올림' or 'Sincerely'

        The letter should make the detective (player) feel enraged, humiliated, and desperate to catch the murderer.
        Do not include any explanations or additional text. Write only the letter content.
        """

        return self.generate_letter(prompt, receiver, sender, max_tokens=250)

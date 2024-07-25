import random
from app.utils.data_loader import (
    load_npcs_data,
    load_features_data,
    load_personalities_data,
    load_places_data,
    load_weapons_data,
    load_names_data,
    load_wealth_data,
    load_scenarios_data
)
from app.utils.game_utils import get_name, get_weapon_name, get_location_name, get_personality_detail, get_feature_detail

# 개별 게임 상태 관리
class GameManagement:
    def __init__(self):
        self.npcs = load_npcs_data()["npcs"]
        self.features = load_features_data()["features"]
        self.personalities = load_personalities_data()["personalities"]
        self.places = load_places_data()["places"]
        self.weapons = load_weapons_data()["weapons"]
        self.names = load_names_data()["names"]
        self.wealth = load_wealth_data()["wealth"]
        self.scenarios = load_scenarios_data()["scenarios"]
        self.game_state = None

    # 새로운 게임을 초기화하는 메서드
    def initialize_game(self, language, npc_count):
        if npc_count > len(self.npcs):
            raise ValueError("NPC count exceeds available NPCs")

        selected_npcs = random.sample(self.npcs, npc_count)
        murderer = random.choice(selected_npcs)
        remaining_npcs = [npc for npc in self.npcs if npc not in selected_npcs]
        murdered_npc = random.choice(remaining_npcs)

        # 무기를 랜덤으로 할당
        weapons = load_weapons_data()["weapons"]
        for npc in selected_npcs:
            npc["preferredWeapons"] = random.sample([weapon["id"] for weapon in weapons], 3)

        # 장소를 랜덤으로 할당
        places = load_places_data()["places"]
        for npc in selected_npcs:
            npc["preferredLocations"] = random.sample([place["id"] for place in places], 3)

        murder_weapon = random.choice(murderer["preferredWeapons"])
        murder_location = random.choice(murderer["preferredLocations"])

        self.game_state = {
            "language": language,
            "suspects": selected_npcs.copy(),
            "murderer": murderer,
            "murdered_npc": murdered_npc,
            "murder_weapon": murder_weapon,
            "murder_location": murder_location,
            "conversations_left": 5,
            "npcs": selected_npcs,
            "places": self.places,
            "weapons": self.weapons,
            "conversations": [],
            "current_day": 1,
            "alive": {npc["name"]: True for npc in selected_npcs},
            "murdered_npcs": [{"name": murdered_npc["name"], "day": 1}]
        }
        for npc in self.game_state["npcs"]:
            if npc["name"] == murdered_npc["name"]:
                npc["alive"] = False

    # 게임 상태를 반환하는 메서드
    def get_game_status(self):
        lang = self.game_state["language"]
        npc_info = [
            {
                "name": get_name(npc["name"], lang, self.names),
                "age": npc["age"],
                "gender": npc["gender"],
                "personality": get_personality_detail(npc["personality"], self.personalities, lang),
                "feature": get_feature_detail(npc["feature"], self.features, lang),
                "preferredWeapons": [get_weapon_name(weapon, self.weapons, lang) for weapon in npc["preferredWeapons"]],
                "preferredLocations": [get_location_name(location, self.places, lang) for location in npc["preferredLocations"]],
                "alive": self.game_state['alive'][npc['name']]
            }
            for npc in self.game_state["npcs"]
        ]
        murderer_info = {
            "name": get_name(self.game_state["murderer"]["name"], lang, self.names),
            "age": self.game_state["murderer"]["age"],
            "gender": self.game_state["murderer"]["gender"],
            "personality": get_personality_detail(self.game_state["murderer"]["personality"], self.personalities, lang),
            "feature": get_feature_detail(self.game_state["murderer"]["feature"], self.features, lang)
        }
        murdered_npc_info = {
            "name": get_name(self.game_state["murdered_npc"]["name"], lang, self.names),
            "age": self.game_state["murdered_npc"]["age"],
            "gender": self.game_state["murdered_npc"]["gender"],
            "personality": get_personality_detail(self.game_state["murdered_npc"]["personality"], self.personalities, lang),
            "feature": get_feature_detail(self.game_state["murdered_npc"]["feature"], self.features, lang)
        }
        return {
            "suspects": npc_info,
            "murderer": murderer_info,
            "murdered_npc": murdered_npc_info,
            "murder_weapon": get_weapon_name(self.game_state["murder_weapon"], self.weapons, lang),
            "murder_location": get_location_name(self.game_state["murder_location"], self.places, lang),
            "current_day": self.game_state["current_day"],
            "alive": self.game_state["alive"],
            "murdered_npcs": self.game_state["murdered_npcs"]
        }

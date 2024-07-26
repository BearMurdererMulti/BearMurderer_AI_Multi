from app.utils.game_utils import get_weapon_name, get_location_name

# 게임 진행 중 힌트 조사
class HintInvestigation:
    def __init__(self, game_state, weapons, places):
        self.game_state = game_state
        self.weapons = weapons
        self.places = places

    # 주어진 장소를 조사하여 단서를 찾는 메서드
    def investigate_location(self, location_name):
        location = next((loc for loc in self.places if get_location_name(loc["id"], self.places, self.game_state["language"]) == location_name), None)
        if not location:
            raise ValueError("Location not found")

        clues = f"You found clues related to the murder at {location['place'][self.game_state['language']]}."
        return clues

    # 주어진 아이템을 찾아 설명을 제공하는 메서드
    def find_item(self, item_name):
        item = next((itm for itm in self.weapons if get_weapon_name(itm["id"], self.weapons, self.game_state["language"]) == item_name), None)
        if not item:
            raise ValueError("Item not found")

        description = f"The item is a {item['weapon'][self.game_state['language']]} and it seems suspicious."
        return description

    # 주어진 무기와 장소를 기준으로 용의자를 필터링하는 메서드
    def filter_suspects(self, weapon, location):
        suspects = []
        for npc in self.game_state["npcs"]:
            if any(get_weapon_name(wpn, self.weapons, self.game_state["language"]) == weapon for wpn in npc["preferredWeapons"]) and any(get_location_name(loc, self.places, self.game_state["language"]) == location for loc in npc["preferredLocations"]):
                suspects.append(npc)
        return suspects

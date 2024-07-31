import random
from app.services.game_management import GameManagement
from app.services.question_generation import QuestionGeneration
from app.services.hint_investigation import HintInvestigation
from app.services.scenario_generation import ScenarioGeneration

# 여러 게임 상태 관리
class GameService:
    def __init__(self):
        self.game_managements: dict[int, GameManagement] = {}
        self.question_generations: dict[int, QuestionGeneration] = {}
        self.hint_investigations: dict[int, HintInvestigation] = {}
        self.scenario_generations: dict[int, ScenarioGeneration] = {}
        self.game_states: dict[int, dict] = {}

    # 새로운 게임을 시작하고 초기화하는 메서드
    def initialize_new_game(self, gameNo, language):
        game_management = GameManagement()
        game_management.initialize_game(language, 9)
        game_state = game_management.game_state
        game_state['current_day'] = 1
        game_state['alive'] = {npc["name"]: True for npc in game_state["npcs"]}
        game_state['murdered_npcs'] = []

        # 첫 번째 희생자 설정
        first_victim = game_state['murdered_npc']
        for npc in game_state["npcs"]:
            if npc["name"] == first_victim["name"]:
                npc["alive"] = False
                break
        game_state['alive'][first_victim['name']] = False
        game_state['murdered_npcs'].append({"name": first_victim['name'], "order": 1})

        self.game_managements[gameNo] = game_management
        self.game_states[gameNo] = game_state
        self.question_generations[gameNo] = QuestionGeneration(
            game_state,
            game_management.personalities,
            game_management.features,
            game_management.weapons,
            game_management.places,
            game_management.names
        )
        self.hint_investigations[gameNo] = HintInvestigation(
            game_state,
            game_management.places,
            game_management.weapons
        )
        self.scenario_generations[gameNo] = ScenarioGeneration(
            game_state,
            game_management.personalities,
            game_management.features,
            game_management.weapons,
            game_management.places,
            game_management.names
        )

    # 게임 상태를 반환하는 메서드
    def get_game_status(self, gameNo):
        game_state = self.game_states.get(gameNo)
        if not game_state:
            raise ValueError("Game ID not found")
        game_management = self.game_managements[gameNo]
        status = game_management.get_game_status()
        status['current_day'] = game_state['current_day']
        status['alive'] = game_state['alive']
        status['murdered_npcs'] = game_state['murdered_npcs']
        return status

    # 게임 진행 상황을 저장하는 메서드
    def save_game_progress(self, gameNo, game_state):
        self.game_states[gameNo] = game_state
        return {"message": "Progress saved successfully"}

    # 초기 게임 시나리오를 생성하는 메서드
    def generate_game_scenario(self, gameNo):
        return self.scenario_generations[gameNo].create_initial_scenario()

    # 촌장의 편지를 생성하는 메서드
    def generate_chief_letter(self, gameNo):
        return self.scenario_generations[gameNo].generate_chief_letter()

    # 질문을 생성하는 메서드
    def generate_npc_questions(self, gameNo, npc_name, keyword, keyword_type):
        if gameNo not in self.question_generations:
            raise ValueError(f"Game ID {gameNo} not found in question generations.")
        return self.question_generations[gameNo].generate_questions(npc_name, keyword, keyword_type)

    # NPC와 대화를 진행하는 메서드
    def talk_to_npc(self, gameNo, npc_name, question_index, keyword, keyword_type):
        if gameNo not in self.question_generations:
            raise ValueError(f"Game ID {gameNo} not found in question generations.")
        return self.question_generations[gameNo].talk_to_npc(npc_name, question_index, keyword, keyword_type)

    # 범행 장소를 조사하는 메서드
    def investigate_location(self, gameNo, location_name):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].investigate_location(location_name)

    # 범행 도구를 조사하는 메서드
    def find_game_item(self, gameNo, item_name):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].find_item(item_name)

    # 용의자를 필터링하는 메서드
    def filter_game_suspects(self, gameNo, weapon, location):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].filter_suspects(weapon, location)

    # 다음 날로 넘어가는 메서드
    def proceed_to_next_day(self, gameNo):
        game_state = self.game_states.get(gameNo)
        if not game_state:
            raise ValueError("Game ID not found")

        remaining_npcs = [npc for npc in game_state['npcs'] if game_state['alive'][npc['name']]]
        if len(remaining_npcs) <= 2:
            raise ValueError("Not enough NPCs to continue the game")

        new_victim = random.choice(remaining_npcs)
        for npc in game_state["npcs"]:
            if npc["name"] == new_victim["name"]:
                game_state['alive'][npc['name']] = False
                break
        game_state['murdered_npcs'].append({"name": new_victim['name'], "order": game_state['current_day'] + 1})

        # 새로운 범행 도구와 장소를 할당
        murderer = game_state['murderer']
        new_weapon = random.choice(murderer["preferredWeapons"])
        new_location = random.choice(murderer["preferredLocations"])
        if 'murder_weapons' not in game_state:
            game_state['murder_weapons'] = [new_weapon]
        else:
            game_state['murder_weapons'].append(new_weapon)
        if 'murder_locations' not in game_state:
            game_state['murder_locations'] = [new_location]
        else:
            game_state['murder_locations'].append(new_location)

        game_state['current_day'] += 1
        new_scenario = self.scenario_generations[gameNo].create_progress_scenario()

        return {
            "new_victim": new_victim['name'],
            "new_weapon": new_weapon,
            "new_location": new_location,
            "current_day": game_state['current_day'],
            "scenario": new_scenario
        }

from pydantic import BaseModel
from typing import List, Dict

class NPC(BaseModel):
    name: str
    personality: str
    is_alive: bool = True
    alibi: str = None

class Location(BaseModel):
    name: str
    description: str
    clues: List[str] = []

class Item(BaseModel):
    name: str
    description: str
    related_to: str = None

class GameState(BaseModel):
    npcs: List[NPC]
    locations: List[Location]
    items: List[Item]
    murderer: NPC
    days_passed: int
    conversations_left: int
    game_over: bool
    current_questions: List[str] = []
    user_language: str = "en"

class GameStartRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    npc_count: int = 6

class GameRequest(BaseModel):
    gameNo: int

class QuestionRequest(BaseModel):
    gameNo: int
    npc_name: str
    keyword: str
    keyword_type: str = "weapon"

class AnswerRequest(BaseModel):
    gameNo: int
    npc_name: str
    question_index: int
    keyword: str
    keyword_type: str = "weapon"
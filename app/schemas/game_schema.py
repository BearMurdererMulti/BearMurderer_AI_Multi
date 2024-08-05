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

class NPCInfo(BaseModel):
    npcName: str
    npcJob: str

class GameStartRequest(BaseModel):
    gameNo: int = 0
    language: str = "ko"
    characters: List[NPCInfo] = [
    {
        "npcName": "김쿵야",
        "npcJob": "Resident"
    },
    {
        "npcName": "박동식",
        "npcJob": "Resident"
    },
    {
        "npcName": "짠짠영",
        "npcJob": "Murderer"
    },
    {
        "npcName": "태근티비",
        "npcJob": "Resident"
    },
    {
        "npcName": "박윤주",
        "npcJob": "Resident"
    },
    {
        "npcName": "테오",
        "npcJob": "Resident"
    },
    {
        "npcName": "소피아",
        "npcJob": "Resident"
    },
    {
        "npcName": "마르코",
        "npcJob": "Resident"
    },
    {
        "npcName": "알렉스",
        "npcJob": "Resident"
    }
]

class GameRequest(BaseModel):
    gameNo: int

class QuestionRequest(BaseModel):
    gameNo: int
    npcName: str
    keyWord: str
    keyWordType: str = "weapon"

class AnswerRequest(BaseModel):
    gameNo: int
    npcName: str
    questionIndex: int
    keyWord: str
    keyWordType: str = "weapon"

class LivingNPCInfo(BaseModel):
    name: str
    job: str
    status: str

class NextDayRequest(BaseModel):
    gameNo: int
    livingCharacters: List[LivingNPCInfo] = [
    {
        "name": "김쿵야",
        "job": "Resident",
        "status": "ALIVE"
    },
    {
        "name": "박동식",
        "job": "Resident",
        "status": "ALIVE"
    },
    {
        "name": "짠짠영",
        "job": "Murderer",
        "status": "ALIVE"
    },
    {
        "name": "태근티비",
        "job": "Resident",
        "status": "ALIVE"
    },
    {
        "name": "박윤주",
        "job": "Resident",
        "status": "ALIVE"
    },
    {
        "name": "테오",
        "job": "Resident",
        "status": "DEAD"
    },
    {
        "name": "소피아",
        "job": "Resident",
        "status": "DEAD"
    },
    {
        "name": "마르코",
        "job": "Resident",
        "status": "DEAD"
    },
    {
        "name": "알렉스",
        "job": "Resident",
        "status": "DEAD"
    }
]

class GameEndRequest(BaseModel):
    gameNo: int
    gameResult: str = "WIN"
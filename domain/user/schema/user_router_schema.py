from typing import List, Optional
from pydantic import BaseModel


class Tokens(BaseModel):
    totalTokens: int
    promptTokens: int
    completionTokens: int

class GenerateInput(BaseModel):
    gameNo: int
    secretKey: str

class GenerateOutput(BaseModel):
    tokens: Tokens

    class Config:
        arbitrary_types_allowed = True


# router input
class CharacterInfo(BaseModel):
    name: str
    alibi: Optional[str]

class PreviousChatContent(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int

class ConversationUserInput(GenerateInput):
    sender: str
    receiver: CharacterInfo
    chatContent: str
    chatDay: int
    previousStory: Optional[str] = None
    previousChatContents: List[PreviousChatContent]

class ConversationNPCInput(GenerateInput):
    sender: str
    npcName1: CharacterInfo
    npcName2: CharacterInfo
    chatDay: int
    previousStory: Optional[str] = None

class ConversationNPCEachInput(GenerateInput):
    sender: str
    npcName1: CharacterInfo
    npcName2: CharacterInfo
    chatDay: int
    previousChatContents: List[PreviousChatContent]
    previousStory: Optional[str] = None
    state: str


# router output
class ConversationUserAnswer(BaseModel):
    chatContent: str

class ConversationNPC(BaseModel):
    sender: str
    receiver: str
    chatContent: str

class ConversationNPCAnswer(BaseModel):
    chatContent: List[ConversationNPC]

class ConversationUserOutput(GenerateOutput):
    answer: ConversationUserAnswer

class ConversationNPCOutput(GenerateOutput):
    answer: ConversationNPCAnswer

class ConversationNPCEachOutput(GenerateOutput):
    answer: ConversationNPC


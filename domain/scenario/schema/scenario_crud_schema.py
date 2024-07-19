from typing import List, Optional
from pydantic import BaseModel


# characters information schema
class CriminalScenarioSchema(BaseModel):
    motivation: str
    procedure: str

class CharacterSchema(BaseModel):
    name: str
    age: int
    gender: str
    wealth: str
    personality: str
    personalityDescription: str
    feature: str
    featureDescription: str
    criminalScenario: CriminalScenarioSchema

class CharactersSchema(BaseModel):
    npcs: List[CharacterSchema]


# places schema
class PlaceName(BaseModel):
    placeNameEn: str
    placeNameKo: str

class PlacesSchema(BaseModel):
    places: List[PlaceName]


# prompt input schema
class MurdererInfo(BaseModel):
    name: str
    motivation: str
    procedure: str

class CharacterInfo(BaseModel):
    name: str
    # personality: str
    personalityDescription: str
    # feature: str
    featureDescription: str


# generate_victim prompt input schema
class VictimGeneration(BaseModel):
    day: int
    murderer: MurdererInfo
    crimeScene: str
    method: str
    victim: str
    witness: str
    livingCharacters: List[CharacterInfo]
    previousStory: Optional[str]

class VictimGenerationContainer(BaseModel):
    information: VictimGeneration


# generate_final_words prompt input schema
class FinalWordsGeneration(BaseModel):
    murderer: MurdererInfo
    gameResult: str
    previousStory: Optional[str]

class FinalWordsGenerationContainer(BaseModel):
    information: FinalWordsGeneration
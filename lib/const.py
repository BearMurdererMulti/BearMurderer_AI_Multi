from pathlib import Path
import json


# NPC data
CHARACTERS = json.load((Path(__file__).resolve().parents[1] / "resources/data/npc.json").open('r', encoding='utf-8'))
PLACES = json.load((Path(__file__).resolve().parents[1] / "resources/data/places.json").open('r', encoding='utf-8'))


# LLMS/langchan/chains.py
MODELS = ["gpt-3.5-turbo-1106", "gpt-4", "gpt-4-1106-preview"]


# LLMs/langchan/chatbot.py
MAX_RETRY_LIMIT = 2


# domain/user/user_crud.py
MAX_CHAT_CONTENTS = 5


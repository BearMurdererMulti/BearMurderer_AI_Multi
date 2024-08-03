from fastapi.testclient import TestClient
from dotenv import load_dotenv
import logging
import json
import os

from app.main import app

load_dotenv()
MY_KEY = os.getenv('MY_KEY')

client = TestClient(app)
logger = logging.getLogger('test')

def test_get_test_token():
    game_no = 0

    request_body = {
        "gameNo": game_no,
        "language": "ko",
        "characters": [
            {"npcName": "김쿵야", "npcJob": "Resident"},
            {"npcName": "박동식", "npcJob": "Resident"},
            {"npcName": "짠짠영", "npcJob": "Murderer"},
            {"npcName": "태근티비", "npcJob": "Resident"},
            {"npcName": "박윤주", "npcJob": "Resident"},
            {"npcName": "테오", "npcJob": "Resident"},
            {"npcName": "소피아", "npcJob": "Resident"},
            {"npcName": "마르코", "npcJob": "Resident"},
            {"npcName": "알렉스", "npcJob": "Resident"}
        ]
    }
    response = client.post("/api/v2/new-game/start", json=request_body)
    assert response.status_code == 200
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    request_body = {"gameNo": game_no}
    response = client.post("/api/v2/new-game/generate-scenario", json=request_body)
    assert response.status_code == 200
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    request_body = {"gameNo": game_no}
    response = client.post("/api/v2/new-game/generate-chief-letter", json=request_body)
    assert response.status_code == 200
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    request_body = {"gameNo": game_no}
    response = client.post("/api/v2/new-game/status", json=request_body)
    assert response.status_code == 200
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))


    assert False

    # request_body = {"secretKey": MY_KEY}
    # response = client.post("/api/etc/secret_key_validation", json=request_body)
    # pretty_response = json.dumps(response.json(), indent=4)
    # assert response.status_code == 200
    # response_data = response.json()
    # assert response_data['message'] == "OpenAI API key is valid."
    # assert response_data['valid'] == True

    # logger.warning(pretty_response)

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
    request_body = {"secretKey": MY_KEY}
    response = client.post("/api/etc/secret_key_validation", json=request_body)
    pretty_response = json.dumps(response.json(), indent=4)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['message'] == "OpenAI API key is valid."
    assert response_data['valid'] == True

    logger.warning(pretty_response)

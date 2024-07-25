from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_gpt_response(prompt: str, max_tokens: int = 100) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an NPC in a murder mystery game. Provide concise and relevant responses to help the player gather clues and solve the mystery."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

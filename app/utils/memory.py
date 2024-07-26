from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

memory = ConversationBufferMemory()

def get_conversation_chain():
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o-mini")
    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )
    return conversation

def add_conversation(user_input: str, bot_response: str):
    memory.save_context({"user": user_input}, {"bot": bot_response})

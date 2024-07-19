from fastapi import APIRouter, HTTPException
from typing import Optional, List

from app.LLMs.langchain import generator
from app.lib.validation_check import check_openai_api_key
from .schema import user_router_schema
from . import user_crud


router = APIRouter(
    prefix="/api/user",
)


def validate_request_data(secret_key: str, receiver_name: Optional[str] = None, npc_names: Optional[List[str]] = None):
    api_key = check_openai_api_key(secret_key)
    if not api_key:
        raise HTTPException(status_code=404, detail="Invalid OpenAI API key.")

    if receiver_name and not user_crud.get_character_info(receiver_name):
        raise HTTPException(status_code=404, detail="Receiver not found in the character list.")
    
    if npc_names and not user_crud.validate_npc_names(npc_names):
        raise HTTPException(status_code=404, detail="Invalid npcName in the list.")
    
    return api_key


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
             response_model=user_router_schema.ConversationUserOutput, 
             tags=["user"])
async def conversation_with_user(conversation_user_schema: user_router_schema.ConversationUserInput):
    api_key = validate_request_data(conversation_user_schema.secretKey, 
                                    receiver_name = conversation_user_schema.receiver.name)
    
    input_data_json, input_data_pydantic = user_crud.conversation_with_user_input(conversation_user_schema)
    answer, tokens, execution_time = generator.generate_conversation_with_user(api_key, input_data_pydantic)

    final_response = {
        "answer": answer.dict(), 
        "tokens": tokens
    }
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             response_model=user_router_schema.ConversationNPCOutput, 
             tags=["user"])
async def conversation_between_npc(conversation_npc_schema: user_router_schema.ConversationNPCInput):
    print(conversation_npc_schema.model_dump_json(indent=2))
    # chatDay, previousStory 이용 안함

    api_key = validate_request_data(conversation_npc_schema.secretKey, 
                                    npc_names = [conversation_npc_schema.npcName1.name, conversation_npc_schema.npcName2.name])
    
    input_data_json, input_data_pydantic = user_crud.conversation_between_npc_input(conversation_npc_schema)
    
    answer, tokens, execution_time = generator.generate_conversation_between_npc(api_key, input_data_pydantic)

    final_response = {
        "answer": answer.dict(), 
        "tokens": tokens
    }
    return final_response


@router.post("/conversation_between_npcs_each", 
             description="npc와 npc간의 대화를 하나씩 생성해 주는 API입니다.", 
             response_model=user_router_schema.ConversationNPCEachOutput, 
             tags=["user"])
async def conversation_between_npcs_each(conversation_npcs_each_schema: user_router_schema.ConversationNPCEachInput):
    # chatDay, previousStory 이용 안함

    api_key = validate_request_data(conversation_npcs_each_schema.secretKey, 
                                    npc_names = [conversation_npcs_each_schema.npcName1.name, conversation_npcs_each_schema.npcName2.name])
    
    input_data_json, input_data_pydantic = user_crud.conversation_between_npc_each_input(conversation_npcs_each_schema)
    
    answer, tokens, execution_time = generator.generate_conversation_between_npcs_each(api_key, input_data_pydantic, conversation_npcs_each_schema.state)

    final_response = {
        "answer": answer.dict(), 
        "tokens": tokens
    }
    return final_response
from fastapi import APIRouter, HTTPException
from typing import Optional, List 

from domain.scenario import scenario_crud
from domain.scenario.schema import scenario_router_schema
from LLMs.langchain import generator
from lib.validation_check import check_openai_api_key

router = APIRouter(
    prefix="/api/scenario",
)


def validate_request_data(secret_key: str, murderer_name: Optional[str] = None, living_characters: Optional[List[str]] = None):
    api_key = check_openai_api_key(secret_key)
    if not api_key:
        raise HTTPException(status_code=404, detail="Invalid OpenAI API key.")

    if murderer_name and not scenario_crud.get_character_info(murderer_name):
        raise HTTPException(status_code=404, detail="Murderer not found in the character list.")
    
    if living_characters and not scenario_crud.validate_living_characters(living_characters):
        raise HTTPException(status_code=404, detail="Invalid livingCharacters in the list.")
    
    return api_key
    
             
@router.post("/generate_intro", 
             description="게임의 intro를 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateIntroOutput, 
             tags=["scenario"])
async def generate_intro(generator_intro_schema: scenario_router_schema.GenerateIntroInput):
    api_key = validate_request_data(generator_intro_schema.secretKey)

    prompt = f"\n"
    
    answer, tokens, execution_time = generator.generate_intro(api_key, prompt)

    final_response = {
        "answer": answer.dict(), 
        "tokens": tokens
    }
    # print(json.dumps(final_response, indent=2, ensure_ascii=False))
    return final_response


@router.post("/generate_victim", 
             description="밤마다 진행되는 피해자 선택과 흰트를 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateVictimOutput, 
             tags=["scenario"])
async def generate_victim(generate_victim_schema: scenario_router_schema.GenerateVictimInput):
    # previousStory 이용 안함

    api_key = validate_request_data(generate_victim_schema.secretKey, 
                                    murderer_name = generate_victim_schema.murderer, 
                                    living_characters = generate_victim_schema.livingCharacters)

    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)

    answer, tokens, execution_time = generator.generate_victim(api_key, input_data_pydantic)

    result = scenario_crud.generate_victim_output(answer, input_data_pydantic, generate_victim_schema)
    final_response = {
        "answer": result, 
        "tokens": tokens
    }
    # print(json.dumps(final_response, indent=2, ensure_ascii=False))
    return final_response


@router.post("/generate_victim_backup_plan", 
             description="밤마다 진행되는 피해자 선택과 흰트를 2개 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateVictimBackupPlanOutput, 
             tags=["scenario"])
async def generate_victim_backup_plan(generate_victim_schema: scenario_router_schema.GenerateVictimInput):
    # previousStory 이용 안함

    api_key = validate_request_data(generate_victim_schema.secretKey, 
                                    murderer_name = generate_victim_schema.murderer, 
                                    living_characters = generate_victim_schema.livingCharacters)

    # plan A
    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)

    answer_a, tokens_a, execution_time_a = generator.generate_victim(api_key, input_data_pydantic)

    result_a = scenario_crud.generate_victim_output(answer_a, input_data_pydantic, generate_victim_schema)

    # plan B
    generate_victim_schema.livingCharacters = [character for character in generate_victim_schema.livingCharacters if character.name != input_data_pydantic.information.victim]

    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)

    answer_b, tokens_b, execution_time_b = generator.generate_victim(api_key, input_data_pydantic)

    result_b = scenario_crud.generate_victim_output(answer_b, input_data_pydantic, generate_victim_schema)

    # result
    tokens = {key: tokens_a.get(key, 0) + tokens_b.get(key, 0) for key in set(tokens_a) | set(tokens_b)}

    final_response = {
        "answer": {
            "planA": result_a,
            "planB": result_b
        }, 
        "tokens": tokens
    }
    # print(json.dumps(final_response, indent=2, ensure_ascii=False))
    return final_response


@router.post("/generate_final_words", 
             description="범인의 마지막 한마디를 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateFinalWordsOutput, 
             tags=["scenario"])
async def generate_final_words(generator_final_words_schema: scenario_router_schema.GenerateFinalWordsInput):
    # previousStory 이용 안함

    api_key = validate_request_data(generator_final_words_schema.secretKey, 
                                    murderer_name = generator_final_words_schema.murderer)
    
    if not scenario_crud.get_character_info(generator_final_words_schema.murderer):
        raise HTTPException(status_code=404, detail="Murderer not found in the character list.")
    
    input_data_json, input_data_pydantic = scenario_crud.generate_final_words_input(generator_final_words_schema)

    answer, tokens, execution_time = generator.generate_final_words(api_key, input_data_pydantic)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    return final_response
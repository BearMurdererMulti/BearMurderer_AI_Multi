from . import chains
from .execute_conversation import execute_conversation
from .prompt import prompts_schema
from .prompt import prompts_scenario, prompts_user
from ...lib.validation_check import response_format


# scenario
def generate_intro(key: str, inputs: str):
    intro_chain = chains.define_llm_chain(key, prompts_scenario.intro_prompt)
    return execute_conversation(intro_chain, response_format, prompts_schema.IntroSchema, inputs)

def generate_victim(key: str, inputs: str):
    victim_chain = chains.define_llm_chain(key, prompts_scenario.generate_victim_prompt)
    return execute_conversation(victim_chain, response_format, prompts_schema.GenerateVictimSchema, inputs)

def generate_final_words(key: str, inputs: str):
    final_words_chain = chains.define_llm_chain(key, prompts_scenario.final_words_prompt)
    return execute_conversation(final_words_chain, response_format, prompts_schema.FinalWordsSchema, inputs)

# user
def generate_conversation_with_user(key: str, inputs: str):
    conversation_with_user_chain = chains.define_llm_chain(key, prompts_user.conversation_with_user_prompt)
    return execute_conversation(conversation_with_user_chain, response_format, prompts_schema.ConversationWithUserSchema, inputs)

def generate_conversation_between_npc(key: str, inputs: str):
    conversation_between_npc_chain = chains.define_llm_chain(key, prompts_user.conversation_between_npc_prompt)
    return execute_conversation(conversation_between_npc_chain, response_format, prompts_schema.ConversationBetweenNPCSchema, inputs)

def generate_conversation_between_npcs_each(key: str, inputs: str, state: str = "ongoing"):
    if state == "ongoing":
        conversation_between_npcs_each_chain = chains.define_llm_chain(key, prompts_user.conversation_between_npc_each_prompt)
        return execute_conversation(conversation_between_npcs_each_chain, response_format, prompts_schema.ConversationBetweenNPCEachSchema, inputs)
    elif state == "finish":
        conversation_between_npcs_each_last_chain = chains.define_llm_chain(key, prompts_user.conversation_between_npc_each_last_prompt)
        return execute_conversation(conversation_between_npcs_each_last_chain, response_format, prompts_schema.ConversationBetweenNPCEachSchema, inputs)
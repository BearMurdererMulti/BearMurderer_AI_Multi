from LLMs.langchain.prompt.prompts_data import prompt_template
from LLMs.langchain.prompt import prompts_schema


conversation_with_user_chain_prefix = """
1. information을 참고하여 character를 연기하여 user의 chatContent에 대답해야 함
2. 답변의 길이는 2~3 문장 안으로 제한함
3. PreviousChatContents가 주어진다면 해당 대화에 맞는 답변을 생성해야 함
4. 지난 밤에 무엇을 했는지 물어본다면 alibi 항목을 참고
5. 답변을 만들 때 personalityDescription, featureDescription을 참고해야 함
"""

conversation_with_user_chain_prefix_2 = """
information 기반 character로 user 질문 대응. 2~3문장 내. PreviousChatContents 고려, alibi 참조. personalityDescription, featureDescription 반영
"""

conversation_between_npc_chain_prefix = """
1. 등장인물 설정을 참고하여 character1과 character2 사이의 대화를 생성하야 함
2. 플래이어와의 대화가 아니라 npc들 사이의 대화를 만들어야 함
3. 시놉시스와 시나리오를 참고하여야함
3. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음
4. 대화는 3~4번 정도 주고 받아야 함
"""

conversation_between_npc_each_chain_prefix = """
1. 등장인물 설정을 참고하여 character1과 character2 사이의 대화 내용 1개를 만들어야 함
2. character1 이 말하거나 character2 가 말하거나 둘 중 하나만 나와야 함
3. 시놉시스와 시나리오를 참고하여야함
4. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음
5. PreviousChatContents가 주어진다면 마지막 대화에 대해 다른 사람이 대화가 이어지도록 답변을 해야 함
"""

conversation_between_npc_each_last_chain_prefix = """
1. 등장인물 설정을 참고하여 character1과 character2 사이의 대화 내용 1개를 만들어야 함
2. character1 이 말하거나 character2 가 말하거나 둘 중 하나만 나와야 함
3. 시놉시스와 시나리오를 참고하여야함
5. PreviousChatContents의 내용을 참고하여 해당 대화를 마무리 짓는 마지막 말을 만들어야 함
"""

conversation_with_user_prompt = prompt_template(prompts_schema.ConversationWithUserSchema, conversation_with_user_chain_prefix)

conversation_between_npc_prompt = prompt_template(prompts_schema.ConversationBetweenNPCSchema, conversation_between_npc_chain_prefix)

conversation_between_npc_each_prompt = prompt_template(prompts_schema.ConversationBetweenNPCEachSchema, conversation_between_npc_each_chain_prefix)

conversation_between_npc_each_last_prompt = prompt_template(prompts_schema.ConversationBetweenNPCEachSchema, conversation_between_npc_each_last_chain_prefix)

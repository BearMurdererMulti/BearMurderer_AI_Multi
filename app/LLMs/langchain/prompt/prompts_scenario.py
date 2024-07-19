from LLMs.langchain.prompt.prompts_data import prompt_template
from LLMs.langchain.prompt import prompts_schema


intro_chain_prefix = """
1. 시놉시스를 이용해서 마을의 촌장의 입장으로 탐정에게 보내는 편지를 만들어야 함.
2. content의 길이는 7문장은 넘지 말아야 함.
"""
intro_chain_prefix_2 = """
탐정에게 보내는 촌장의 편지: 마을에서 발생한 미스터리 해결 요청. 시놉시스 기반, 5문장 내외.
"""

generate_victim_prefix = """
1. 주어진 information을 보고 eyewitnessInformation, dailySummary를 생성해야 함
2. dailySummary에는 누가 어디서 살해되었는 지 간단히 설명으로 지정해야 함. 'day 0 - '과 같은 식으로 시작해야 함
3. 지정된 목격자가 플레이어의 추리에 도움이 될 수 있도록 목격정보를 지정해야 함
4. previousStory를 참고하여 이후의 스토리를 만들어야하며 previousStory의 내용은 들어가면 안됨
5. alibi에는 victim과 murderer를 제외한 모든 livingCharacters의 알리바이를 만들어야 함. witness의 알리바이 또한 포함 되어야 함
6. 모든 답변은 단답식으로 작성되어야 함
"""

generate_victim_prefix_2 = """
information 기반으로 eyewitnessInformation, dailySummary 생성. Summary: 'day 0 -'로 시작, 살해 사건 간략 설명. 목격자 정보로 추리 도움. previousStory 연계 스토리, 내용 제외. livingCharacters 알리바이, victim/murderer 제외, witness 포함. 단답식 답변.
"""

final_words_chain_prefix = """
1. information을 참고하여 살인자의 마지막 한마디를 생성해야 함.
2. 마지막 한마디의 내용은 gameResult에 따라 달려져야 함. 'victory'라면 살인자의 패배이고 'defeat'면 살인자가 모든 마을 주민을 죽이고 승리한 상황임.
3. 답변의 길이는 4문장은 넘지 말아야 함.
"""

final_words_chain_prefix_2 = """
gameResult 기반 살인자 마지막 한마디 생성. 'victory': 살인자의 패배, 'defeat': 살인자의 승리. 4문장 이내.
"""

intro_prompt = prompt_template(prompts_schema.IntroSchema, intro_chain_prefix)
                              
generate_victim_prompt = prompt_template(prompts_schema.GenerateVictimSchema, generate_victim_prefix)

final_words_prompt = prompt_template(prompts_schema.FinalWordsSchema, final_words_chain_prefix)
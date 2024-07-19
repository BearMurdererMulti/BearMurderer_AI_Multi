from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.prompt import PromptTemplate

synopsis = """
주요 캐릭터:

1. 탐정 (플레이어): 유명한 탐정으로, 특이한 사건을 해결하는 데 능숙함.
2. 촌장: 마을의 촌장으로, 마을을 이끌고 있는 지혜로운 촌장.
3. 마을 주민들: 각기 다른 특성과 배경을 가진 주민들.

스토리 개요:

- 시작: 탐정인 플레이어는 마을의 촌장으로부터 마을에서 발생한 충격적인 살인 사건에 대한 의뢰를 받음. 평화로웠던 마을에서 처음으로 발생한 이 사건은 모두를 불안하게 만듬.
- 게임 진행: 탐정은 낮 동안 마을을 돌아다니며 주민들과 대화를 통해 힌트나 거짓말 을 판별하여 범인을 추리해야함.
- 밤 시간: 밤이 되면 범인은 또 다른 주민을 살해함. 이로 인해 다음 날의 조사는 더 어려워지며, 새로운 증거와 정보가 등장.
- 결말: 탐정은 모든 대화를 통해 범인을 추리해야 함. 범인을 정확히 지목하면 게임에서 승리, 실패 시 게임 오버.
"""

synopsis2 = """
주요 캐릭터: 유능한 탐정(플레이어), 지혜로운 촌장, 다양한 주민들. 
스토리: 플레이어는 살인 사건 해결 의뢰를 받고, 마을을 조사해 범인 추적. 낮에는 힌트 수집, 밤에는 새 살인 발생. 결말은 범인 정확히 지목 시 승리.
"""

conversation_chain_suffix = """
{format_instructions}
{input}
"""

def prompt_template(schema, chain_prefix):
    parser = PydanticOutputParser(pydantic_object=schema)
    template = synopsis + chain_prefix + conversation_chain_suffix
    prompt = PromptTemplate(template=template, 
                            input_variables=["input"], 
                            partial_variables={"format_instructions": parser.get_format_instructions()})
    return prompt
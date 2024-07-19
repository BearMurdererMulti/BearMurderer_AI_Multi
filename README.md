# 🧸 Gummy murderer (AI part)

#### 🎥 시연 영상 보러가기([Click]())
#### 📙 발표자료 보러가기([Click]())

<br/>


# :family: 팀원 소개 및 역할

**개발기간: 2023.12.15 ~ ing**

| AI | AI | server | server | Unity | Unity |
|:--:|:--:|:------:|:------:|:------:|:------------:|
| [정민교](https://github.com/MinkyoJeong1) | [김찬영](https://github.com/cykim1228) | [김나영](https://github.com/kny3037) | [박태근](https://github.com/taegeun-park) | [변지환](https://github.com/jimandy00) | [강주연](https://github.com/juyeon0514) |

### AI 세부 역할 분담

<table>
    <tbody>
        <tr>
            <td><b>정민교</b></td>
            <td>Fastapi를 이용한 모델 서빙 및 CI/CD 구축</td>
        </tr>
        <tr>
            <td><b>김찬영</b></td>
            <td>LLM 모델 성능 비교, 프롬프트 엔지니어링</td>
        </tr>
    </tbody>
</table>

<br/>

# 🤝 융합 구조도

<br/>

# 💡 프로젝트 소개

**두근두근 놀러와요 마피아의 숲! 구미머더러! 지금 플레이하세요(찡긋)**

<br/>

# 📜 주요 내용


## 1. LLM 모델 비교 분석
### GPT-4 VS Mistral 비교 분석
이 파트에서는 2가지 AI 모델. GPT-4 (gpt-4-1106-preview) 와 Mistral(PiVoT-10.7B-Mistral-v0.2-RP) 을 비교 분석합니다. 이 비교는 텍스트 기반 인공지능 추리 게임 설정에서의 대화 생성 품질에 초점을 맞추고 있습니다.

### 1) GPT-4 (gpt-4-1106-preview) 모델

- **Request :** 
	```JSON
	{
	  "content": "안녕? 어젯밤 일어난 사건에 대해 아는거 있어?",
	  "npc_name": "애쉬"
	}
	```

- **Response :** 
	```JSON
	{
	  "answer": "안녕, 탐정님! 어젯밤 사건이라니, 참으로 끔찍한 일이죠. 잠이 모자라서 온 마을이 수군거리고 있어요. 제가 알기로는, 레오가 늦은 밤까지 연주하고 있었다고 해요. 아마 그 시간에 뭔가 이상한 소리나 움직임을 목격했을 수도 있을 것 같아요. 물론 저는 장난치러 다니느라 그다지 많은 걸 보진 못했지만요. 하하, 장난은 장난일 뿐, 사건에 대해선 진지하게 생각하고 있답니다. 어쨌든, 주변에는 다양한 소문이 돌고 있으니, 조금 더 살펴보시는 게 좋을 거예요."
	}
	```

#### 분석
- __문맥 :__ 문맥 상 응답이 자연스러움.
- __문법 :__ 문법적으로 잘 구성되어 있음.
- __프롬 :__ NPC "애쉬" 의 성격과 사건에 대한 게임의 흐름을 잘 반영하고 있음.

### 2) Mistral (PiVoT-10.7B-Mistral-v0.2-RP) 모델

- **Request :** 
	```JSON
	{
	  "content": "안녕? 어젯밤 일어난 사건에 대해 아는거 있어?",
	  "npc_name": "애쉬"
	}
	```

- **Response :** 
	```JSON
	{
	  "answer": "애쉬 says: 밤 10시 30분 정도 밖에서 밖에서 소리가 들렸고 밖에서 밖에서 소리가 들렸고 밖에서 소리가 들렸고 밖에서 소리가 들렸고 밖에서 소리가 들렸고 "
	}
	```

#### 분석
- __문맥 :__ 응답이 반복적이고 불완전함.
- __문법 :__ 문법적으로 끝맺음되지도 않고 말이 안됨.
- __프롬 :__ 프롬프트에 따른 적절한 대화를 생성하지 못함.


### 3) 결론
- __GPT-4 :__ 상황에 적절하고 자연스러운 대화를 생성하는데 뛰어난 성능을 보임. 플레이어의 몰입감을 높이고 게임 진행에 필요한 정보를 제공하는데 유용함.
- __Mistral :__ 현재 모델 자체의 문제인지 데이터양의 문제인지 확인은 못했으나 반복적이고 불완전한 응답을 보이므로 실 적용 어려움. 설정이나 추가적인 최적화가 필요함.

<br/>

## 2. Prompt Engineering

### 1) Input data format

gpt에 데이터를 넣을 때 어떤 형식으로 넣어야 잘 알아 듣고 토큰을 아낄 수 있는지 테스트 해보았다.

- #### String
	```
	string = """
	information:
	    user: 형구
	    character:
	        name: 레오
	        personalityDescription: 용기 있게 행동함
	        featureDescription: 노래를 부르듯이 대답함
	        alibi: 지난 밤 마을 잔치에 참여함
	    chatContent: 내 이름이 뭔지 알아?
	    previousStory:
	    previousChatContents:
	        type: user
	        name: 형구
	        content: 넌 누구야?
	
	        type: character
	        name: 레오
	        content: 안녕하신가, 나는 레오라고 하네. 용기 있게 행동하는 것을 좋아하고, 대답할 땐 마치 노래를 부르듯이 말하네.
	"""
	```

	```
	> 'promptTokens': 210
	```

- #### Json pretty
	```
	{
	  "information": {
	    "user": "형구",
	    "character": {
	      "name": "레오",
	      "personalityDescription": "용기 있게 행동함",
	      "featureDescription": "노래를 부르듯이 대답함",
	      "alibi": "지난 밤 마을 잔치에 참여함"
	    },
	    "chatContent": "내 이름이 뭔지 알아?",
	    "previousStory": "",
	    "previousChatContents": [
	      {
	        "type": "user",
	        "name": "형구",
	        "content": "넌 누구야?"
	      },
	      {
	        "type": "character",
	        "name": "레오",
	        "content": "안녕하신가, 나는 레오라고 하네. 용기 있게 행동하는 것을 좋아하고, 대답할 땐 마치 노래를 부르듯이 말하네."
	      }
	    ]
	  }
	}
	```

	```
	> 'promptTokens': 254
	```

- #### Json
	```
	{'information': {'user': '형구', 'character': {'name': '레오', 'personalityDescription': '용기 있게 행동함', 'featureDescription': '노래를 부르듯이 대답함', 'alibi': '지난 밤  마을 잔치에 참여함'}, 'chatContent': '내 이름이 뭔지 알아?', 'previousStory': '', 'previousChatContents': [{'type': 'user', 'name': '형구', 'content': '넌 누구야?'}, {'type': 'character', 'name': '레오', 'content': '안녕하신가, 나는 레오라고 하네. 용기 있게 행동하는 것을 좋아하고, 대답할 땐 마치 노래를 부르듯이 말하네.'}]}}
	```

	```
	> 'promptTokens': 224
	```

- #### Pydantic
	```
	information=ConversationWithUserGeneration(user='형구', character=CharacterInfo(name='레오', personalityDescription='용기 있게 행동함', featureDescription='노래를 부르듯이 대답함', alibi='지난 밤 마을 잔치에 참여함'), chatContent='내 이름이 뭔지 알아?', previousStory='', previousChatContents=[PreviousChatContents(type='user', name='형구', content='넌 누구야?'), PreviousChatContents(type='character', name='레오', content='안녕하신가, 나 는 레오라고 하네. 용기 있게 행동하는 것을 좋아하고, 대답할 땐 마치 노래를 부르듯이 말하 네.')])
	```

	```
	> 'promptTokens': 205
	```

- #### Result
	string, json pretty, json, pydantic의 형태로 gpt에 데이터를 넣을 때 pydantic이 가장 토큰의 수가 적었고 그 다음은 string이었다. 다만 string으로 데이터를 넣을 때 데이터의 형태에 따라 내용의 명확한 구분이 어려워 gpt가 이해를 잘 못하는 경우가 생겼다. 따라서 pydantic 형태로 데이터를 입력하기로 결정하였다.
	
	|       | string | json pretty | json | pydantic |
	| :---: | :----: | :---------: | :--: | :------: |
	| token |  210   |     254     | 224  |   205    |
	|  이해도  |   하    |      상      |  상   |    상     |

### 2) Output format schema

LLM 모델의 답변으로 특정 형태가 필요한 경우가 있다. 아래의 방법을 활용하면 답변의 형식을 보장받을 수 있고 여러 개의 답변을 한번에 출력하는 경우에도 유용하게 사용하였다.

- #### prompt에 정의
	```
	답변의 형식은 greeting, content, closing 이 포함되는 dictionary 형태로 반환해야 함.
	```
	
	**Response**
	```
	{
		"greeting": "존경하는 탐정님께,",
		"content": "우리 마을에 벌어진 끔찍한 살인 사건으로 모두가 두려움에 떨고 있습니다. 평화로웠던 이곳에 갑작스럽게 드리운 그림자를 걷어내고 진실을 밝혀주시길 간곡히 부탁드립니다. 낮 시간 동안 마을 사람들과 대화하여 범인의 흔적을 찾아주시기 바랍니다. 우리 마을의 평화를 되찾는 것은 이제 당신의 손에 달려 있습니다.", 
		"closing": "건강을 빌며, 마을 촌장 올림." 
	}
	```
	
	위의 형식을 prompt에 추가 하더라도 답변은 원하는 형태로 나온다. 다만 내용의 형식이 바뀌는 경우를 종종 발견할 수 있었다. 예를 들면 
	```
	{ "closing": { "message": "건강을 빌며", "sender": "마을 촌장 올림" } }
	```
	이와 같이 closing의 내용이 string이기를 기대했지만 dictionary로 나오는 등의 경우가 있었다.

- #### langchain_core.pydantic_v1
	위의 문제를 해결하고자 langchain의 pydantic기능을 사용하였다.

	```python
	from langchain_core.pydantic_v1 import BaseModel
	from langchain.prompts.prompt import PromptTemplate
	from langchain.output_parsers import PydanticOutputParser
	
	class IntroSchema(BaseModel):
	    greeting: str
	    content: str
	    closing: str
	
	intro_parser = PydanticOutputParser(pydantic_object=IntroSchema)
	intro_prompt = PromptTemplate(template=intro_template,
	                              input_variables=["input"],
	                              partial_variables={"format_instructions": intro_parser.get_format_instructions()})
	```
	
	schema를 지정하여 PromptTemplate에 추가한다면 langchain에서 프롬프트에 다음과 같은 내용을 추가해 준다.
	```
	The output should be formatted as a JSON instance that conforms to the JSON schema below.
	
	As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
	the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.
	
	Here is the output schema:
	\```
	{"properties": {"greeting": {"title": "Greeting", "type": "string"}, "content": {"title": "Content", "type": "string"}, "closing": {"title": "Closing", "type": "string"}}, "required": ["greeting", "content", "closing"]}
	\```
	```
	
	물론 프롬프트에 답변 형식을 지정하는 방법이므로 promptTokens이 200 ~ 300 정도 추가로 필요하다. 복잡한 형식의 답변이 필요하지 않을 경우, 단답형 답변만 생성할 경우 위와 같은 방식은 비 효율적일 수 있다.

<br/>

### 3) Token saving

# 🛠 기술 스택

### - 언어
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">

### - 주요 라이브러리
 <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white"> <img src="https://img.shields.io/badge/langchain-EC1C24?style=for-the-badge&logo=langchain&logoColor=white">

### - 개발 툴
<img src="https://img.shields.io/badge/VS code-2F80ED?style=for-the-badge&logo=VS code&logoColor=white">

### - 협업 툴
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"> <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white">

# 🔍 참고자료

<br/>


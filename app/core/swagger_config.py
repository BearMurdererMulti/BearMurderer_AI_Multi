import textwrap

class SwaggerConfig:
    def __init__(self):
        self.title = "AI Mafia"
        self.version = "0.1.0"
        self.description = textwrap.dedent("""\
            #### 두근두근 놀러와요 마피아의 숲! 베어머더러! 지금 플레이하세요(찡긋)

            기능 목록:

            * **Say Hello** (_completely implemented_).
            * **scenario** (_not implemented_).
            * **user** (_not implemented_).
        """)
        self.license_info = {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
        self.tags_metadata = [
            {
                "name": "SCENARIO",
                "description": "게임 진행을 위한 시나리오 등을 생성합니다."
            },
            {
                "name": "USER",
                "description": "사용자와 상호작용 할 수 있도록 답변을 생성합니다."
            },
            {
                "name": "NEW_GAME",
                "description": "새로운 게임 시작 시 사용되는 API입니다."
            },
            {
                "name": "IN_GAME",
                "description": "게임 중 사용되는 API입니다."
            },
        ]

    def get_config(self):
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "license_info": self.license_info,
            "tags_metadata": self.tags_metadata,
        }

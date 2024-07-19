from http import HTTPStatus

def message_format(message: str, kwargs):
    if "INFO" in message:
        message = message.replace("INFO", "[0;36mINFO[0m")

    if "status_code" in kwargs.keys() and "Response" in message:
        status_code = kwargs["status_code"]

        try:
            status_text = HTTPStatus(status_code).phrase
        except ValueError:
            status_text = "Unknown Status"
        
        # 성공 응답
        if 200 <= status_code < 300:
            message += f"  [0;32m{status_code} {status_text}[0m"
        # 클라이언트 오류 응답
        elif 400 <= status_code < 500:
            message += f"  [0;31m{status_code} {status_text}[0m"
        # 서버 오류 응답
        elif 500 <= status_code:
            message += f"  [0;35m{status_code} {status_text}[0m"
        # 리다이렉션 응답
        elif 300 <= status_code < 400:
            message += f"  [0;33m{status_code} {status_text}[0m"
        # 정보 응답
        elif 100 <= status_code < 200:
            message += f"  [0;34m{status_code} {status_text}[0m"
        else:
            message += f"  {status_code} {status_text}"

    return message
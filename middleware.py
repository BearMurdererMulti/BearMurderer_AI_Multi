from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from datetime import datetime
import json
import time
import logging

from discord_bot.discord_bot import send_message

url_list = ["/api/scenario/generate_intro",
            "/api/scenario/generate_victim",
            "/api/scenario/generate_victim_backup_plan",
            "/api/scenario/generate_final_words",
            "/api/user/conversation_with_user",
            "/api/user/conversation_between_npcs",
            "/api/user/conversation_between_npcs_each",
            "/api/etc/secret_key_validation"]


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in url_list:
            # Before processing the request
            await self.handle_request(request)

            # Measure request processing time
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log request completion
            logging.info(f"Request: {request.method} {request.url.path} - Completed in {process_time:.2f}s")

            # After processing the request
            response = await self.handle_response(request, response, process_time)
            
            return response
        else:
            return await call_next(request)

    async def handle_request(self, request: Request):
        # Log client IP and request details
        client_ip = request.client.host if request.client else "Unknown"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_log = f"INFO:    Request  {client_ip} - \"{request.method} {request.url.path}\"  {current_time}"
        
        # Log POST request body if applicable
        if request.method == "POST":
            body = await request.body()
            request._body = body
            try:
                body_json = json.loads(body.decode('utf-8'))
                request_body = f"\nRequest body: {json.dumps(body_json, indent=2, ensure_ascii=False)}"
            except json.JSONDecodeError:
                request_body = "\nRequest body is not valid JSON"
        
            # Send message to Discord
            await send_message(["#"*40, request_log, request_body])
        else:
            await send_message(["#"*40, request_log])

    async def handle_response(self, request: Request, response: Response, process_time: float):
        # Log client IP and response details
        client_ip = request.client.host if request.client else "Unknown"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_log = f"INFO:    Response {client_ip} - {current_time} - Processed in {process_time:.2f}s"

        if hasattr(response, 'body_iterator'):
            body_bytes = b''
            async for chunk in response.body_iterator:
                body_bytes += chunk

            try:
                body_text = json.dumps(eval(body_bytes.decode('utf-8')), indent=2, ensure_ascii=False)
            except:
                body_text = body_bytes.decode('utf-8')

            new_response = Response(content=body_bytes, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)

            await send_message([response_log, body_text], status_code=response.status_code)
            return new_response
        else:
            await send_message([response_log], status_code=response.status_code)
            return response
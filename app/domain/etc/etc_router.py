from fastapi import APIRouter, HTTPException

from . import etc_schema
from app.lib.validation_check import check_openai_api_key

router = APIRouter(
    prefix="/api/etc",
)
    
             
@router.post("/secret_key_validation", 
             description="openAI secret key를 확인하는 API입니다.", 
             tags=["etc"])
async def secret_key_validation(secret_key_schema: etc_schema.SecretKeyValidation):
    api_key = check_openai_api_key(secret_key_schema.secretKey)

    if not api_key:
        raise HTTPException(status_code=404, detail="Invalid OpenAI API key.")
    
    return {
        "message": "OpenAI API key is valid.", 
        "valid": True, 
        }

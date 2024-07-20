from pydantic import BaseModel


class SecretKeyValidation(BaseModel):
    secretKey: str
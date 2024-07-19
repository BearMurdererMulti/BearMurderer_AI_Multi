from typing import List, Optional
from pydantic import BaseModel


class SecretKeyValidation(BaseModel):
    secretKey: str
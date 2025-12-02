from pydantic import BaseModel, EmailStr
from typing import List, Optional



class Deal(BaseModel):
    id: int
    title: str
    status: Optional[str] = None
    asset_class: Optional[str] = None
    currency: Optional[str] = None
    minimum_ticket: Optional[int] = None

class LoginRequest(BaseModel):
    username: EmailStr
    password: str
    website: str

class LoginResult(BaseModel):
    token: str
    deals: List[Deal]

class LoginResponse(BaseModel):
    website: str
    token: str
    deals: List[Deal]
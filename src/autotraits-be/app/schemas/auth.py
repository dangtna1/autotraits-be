from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    breeder_name: Optional[str] = None  # allow breeder creation at signup
    role: Optional[str] = "user"


class UserInDB(UserBase):
    id: int
    role: str
    breeder_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    breeder_id: int
    role: str

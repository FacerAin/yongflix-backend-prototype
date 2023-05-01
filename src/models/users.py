from beanie import Document
from pydantic import BaseModel, EmailStr


class User(Document):
    name: str
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "name": "test_name",
                "email": "test@test.com",
                "password": "testpassword",
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@test.com",
                "password": "testpassword",
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

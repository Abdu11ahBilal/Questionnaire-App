from pydantic import BaseModel, EmailStr, Field, field_validator

class SignupSchema(BaseModel):

    email: EmailStr 
    username: str = Field(..., min_length=3, max_length=25)
    password: str = Field(..., min_length=8)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class LoginSchema(BaseModel):
    email: EmailStr
    password: str 
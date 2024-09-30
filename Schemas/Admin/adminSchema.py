from datetime import datetime, date
from typing import Optional
from wsgiref.validate import validator
from nanoid import generate
from pydantic import BaseModel, EmailStr, Json, constr, conint, field_validator, Field

# Create a Admin
class CreateAdmin(BaseModel):
    admin_name: str
    password: str
    email: EmailStr

# Admin Login
class LoginAdmin(BaseModel):
    admin_name: str
    password: str


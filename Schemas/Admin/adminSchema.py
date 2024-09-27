from pydantic import BaseModel, EmailStr

# Create a Admin
class CreateAdmin(BaseModel):
    admin_name: str
    password: str
    email: EmailStr

# Admin Login
class LoginAdmin(BaseModel):
    admin_name: str
    password: str
from pydantic import BaseModel , constr, Json, EmailStr, field_validator, Field
from typing import Optional
from datetime import time
from nanoid import generate


class BranchSchema(BaseModel):
    branch_id: Optional[str] = Field(default_factory=lambda : generate(size=8))
    branch_name: constr(max_length=20, to_lower=True)
    address: Json
    email: EmailStr
    location: constr(max_length=10, to_lower=True)
    mobile: int
    open_time: time
    close_time: time
    description: Optional[str] = None
    branch_manager_id : str

    @classmethod
    @field_validator('email')
    def email_length(cls,value):
        if len(value) > 40:
            raise ValueError("email too long. max length is 40 chars")
        return value

class BranchRequestSchema(BaseModel):
    branch: list[BranchSchema]
    branch_halls: Optional[list] = None
    branch_images_urls: Optional[list] = None

    @classmethod
    @field_validator("branch")
    def branch_length(cls,value):
        if len(value) > 1:
            raise ValueError("create one branch in per request, can not create multiple branches")

class DeleteBranchSchema(BaseModel):
    branch_id : list

class UpdateActiveField(BaseModel):
    branch_id: str
    active: bool

class BranchUpdateSchema(BaseModel):
    branch_id: str
    branch_name: constr(max_length=20, to_lower=True)
    address: Json
    email: EmailStr
    location: constr(max_length=10, to_lower=True)
    mobile: int
    open_time: time
    close_time: time
    description: Optional[str] = None
    branch_manager_id : str



class BranchUpdateRequestSchema(BaseModel):
    branch: list[BranchUpdateSchema]
    branch_halls: Optional[list] = None
    branch_images_urls: Optional[list] = None




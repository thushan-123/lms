from pydantic import BaseModel, EmailStr, constr, field_validator, Field, Json
from typing import Optional
from nanoid import generate
from Function.function import password_hash

class OfficerSchema(BaseModel):
    officer_id: str = Field(default_factory= lambda : generate(size=15))
    officer_firstname: constr(to_lower=True, max_length=15)
    officer_lastname: constr(to_lower=True, max_length=15)
    password: str = Field(default_factory= lambda : generate(size=7))
    officer_address:  Optional[Json] = None
    province: Optional[constr(to_lower=True, max_length=10)] = None
    district: Optional[constr(to_lower=True,max_length=10)] = None
    home_town: Optional[constr(to_lower=True,max_length=10)] = None
    officer_email: EmailStr
    officer_gender: Optional[bool] = None
    officer_mobile: int
    branch_id: constr(max_length=36)
    officer_NIC: Optional[constr(max_length=15)] = None
    officer_school: Optional[str] = None
    education_level_id: constr(max_length=36)

    @classmethod
    @field_validator('officer_email')
    def email_length(cls,value):
        if len(value) >40:
            raise ValueError("email length less than 40 chars")
        return value


class CreateOfficerSchema(BaseModel):
    officer_data: list[OfficerSchema]
    urls: list

class OfficerDetailsSchema(BaseModel):
    officer_id: str
    officer_firstname: str
    officer_lastname: str
    officer_address: Json
    province: str
    district: str
    home_town: str
    officer_email: EmailStr
    officer_gender: bool
    officer_mobile: int
    branch_id: str
    officer_NIC: str
    officer_school: str
    education_level_id: str

class OfficerDetailsResponseSchema(BaseModel):
    officer_data: list[OfficerDetailsSchema]
    urls: list

class OfficerUpdateSchema(BaseModel):
    officer_id: str
    officer_firstname: constr(to_lower=True, max_length=15)
    officer_lastname: constr(to_lower=True, max_length=15)
    officer_address: Optional[Json] = None
    province: Optional[constr(to_lower=True, max_length=10)] = None
    district: Optional[constr(to_lower=True, max_length=10)] = None
    home_town: Optional[constr(to_lower=True, max_length=10)] = None
    officer_email: EmailStr
    officer_gender: Optional[bool] = None
    officer_mobile: int
    branch_id: constr(max_length=36)
    officer_NIC: Optional[constr(max_length=15)] = None
    officer_school: Optional[str] = None
    education_level_id: constr(max_length=36)

    @classmethod
    @field_validator('officer_email')
    def email_length(cls, value):
        if len(value) > 40:
            raise ValueError("email length less than 40 chars")
        return value

class OfficerUpdateReqSchema(BaseModel):
    officer_data: list[OfficerUpdateSchema]
    urls: list

class OfficerStatusSchema(BaseModel):
    officer_id: str
    current_status: bool


class OfficerDeleteSchema(BaseModel):
    officer_id: list

class OfficerSearchSchema(BaseModel):
    branch_id: Optional[str] = None
    officer_id: Optional[str] = None
    officer_name: Optional[str] = None



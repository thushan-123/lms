from pydantic import BaseModel, EmailStr, constr, field_validator, Field, Json
from typing import Optional
from datetime import datetime
import uuid

class TeacherCreateSchema(BaseModel):
    teacher_id:str = uuid.uuid4()
    teacher_firstname: constr(max_length=15)
    teacher_lastname: constr(max_length=15)
    teacher_email: EmailStr
    teacher_mobile: int
    subject: constr(max_length=15)
    branch_id: constr(max_length=8)
    education_level_id: constr(max_length=36)

class TeacherSchema(BaseModel):
    teacher_id: str
    teacher_firstname: constr(max_length=15)
    teacher_lastname: constr(max_length=15)
    teacher_email: EmailStr
    teacher_mobile: int
    subject: constr(max_length=15)
    branch_id: constr(max_length=8)
    education_level_id: constr(max_length=36)
    teacher_address: Json
    province: constr(max_length=10)
    district: constr(max_length=10)
    home_town: constr(max_length=10)
    teacher_gender: bool
    teacher_NIC: constr(max_length=15)
    teacher_school: constr(max_length=50)
    teacher_description: str

class TeacherUpdateSchema(BaseModel):
    teacher_data: list[TeacherSchema]
    urls: list

class TeacherStatusSchema(BaseModel):
    teacher_id: str
    teacher_current_status: bool


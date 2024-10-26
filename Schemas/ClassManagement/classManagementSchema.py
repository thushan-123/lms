from pydantic import BaseModel, EmailStr, field_validator, constr, Field, Json
from typing import Optional

class ClassTypesSchema(BaseModel):
    class_type_id: int
    class_fee: float

class CreateClassSchema(BaseModel):
    class_name: constr(to_lower=True, max_length=25)
    branch_id: list
    teacher_id: constr(max_length=36)
    class_type_id: int
    class_fees: list[ClassTypesSchema]
    education_level_id: constr(max_length=36)
    about: str
    urls: list

class ClassDataResponseSchema(BaseModel):
    class_id: str
    class_name: str
    branch_id: list
    teacher_id: str
    class_type_id: int
    class_fees: list[ClassTypesSchema]
    education_level_id: str
    about: str
    urls: list

class UpdateClassSchema(BaseModel):
    class_id: constr(max_length=36)
    class_name: constr(to_lower=True, max_length=25)
    branch_id: list
    teacher_id: constr(max_length=36)
    class_type_id: int
    class_fees: list[ClassTypesSchema]
    education_level_id: constr(max_length=36)
    about: str
    urls: list

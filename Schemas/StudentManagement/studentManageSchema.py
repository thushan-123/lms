from datetime import datetime, date
from typing import Optional
from nanoid import generate
from pydantic import BaseModel, EmailStr, Json, constr, conint, field_validator, Field, validator

class Student(BaseModel):
    student_id: str = Field(default_factory= lambda : generate(size=15)) # auto gen student id
    firstname: constr(max_length=15, to_lower=True)
    lastname: constr(max_length=15, to_lower=True)
    email: EmailStr
    address: Json
    gender: bool
    admission_free_is_paid: bool
    mother_tung: Optional[constr(max_length=10, to_lower=True)] = None
    NIC: Optional[str] = None
    school: Optional[constr(max_length=50)] = None
    mobile: int
    education_level_name: constr(max_length=15, to_lower=True)
    branch_id: constr(max_length=8, to_lower=True)


class StudentParents(BaseModel):
    father_name: Optional[constr(max_length=25, to_lower=True)] = None
    father_mobile: Optional[int] = None
    father_email: Optional[EmailStr] = None
    father_occupation: Optional[constr(max_length=15, to_lower=True)] = None
    father_address: Optional[Json] = None
    mother_name: Optional[constr(max_length=25, to_lower=True)] = None
    mother_mobile: Optional[int] = None
    mother_email: Optional[EmailStr] = None
    mother_occupation: Optional[constr(max_length=15, to_lower=True)] = None
    mother_address: Optional[Json] = None
    info_send: Optional[bool] = None

class ProfileImageStudent(BaseModel):
    profile_image_url: Optional[str] = None

class CertificateImagesStudent(BaseModel):
    certificate_image_url: Optional[str] = None

class StudentSiblings(BaseModel):
    name: constr(max_length=40)
    DOB: Optional[date] = None
    gender: bool
    mobile: Optional[int] = None

class AddStudent(BaseModel):
    student: list[Student]
    profile_image_url: Optional[list] = None
    certificate_image_url: Optional[list] = None
    student_parents: list[StudentParents]
    siblings: list[StudentSiblings]

    @classmethod
    @field_validator('student')
    def student_list_length(cls, value):  # Improved naming convention
        if not (len(value) == 1):
            raise ValueError("Student list must contain exactly one student.")
        return value

    @classmethod
    @field_validator('student_parents')
    def student_parents_list_length(cls, value):
        if not (len(value) == 1):
            raise ValueError("Student parents list must contain exactly one set of parents.")
        return value

    @classmethod
    @field_validator('profile_image_url')
    def url_list_length(cls, value):
        if value and len(value) > 1:  # Handle optional value and length check
            raise ValueError("Profile image URL can be empty or contain only one URL.")
        return value

class DeactivateStudent(BaseModel):
    student_id: list

class DeleteStudent(BaseModel):
    student_id: list

from pydantic import BaseModel, constr, EmailStr, field_validator

class CreateManagerSchema(BaseModel):
    manager_name: constr(max_length=30)
    manager_email: EmailStr

    @classmethod
    @field_validator("manager_email")
    def email_length(cls,value):
        if len(value) > 40:
            raise ValueError("email max length is 40 chars")
        return value


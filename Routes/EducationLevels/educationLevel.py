import json

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from Loggers.log import app_log,err_log
from Authorization.auth import decode_token_access_role, oauth2_scheme
from pydantic import BaseModel, constr
from Function.function import db_dependency
from .educationalLevelFunction import add_education_level, retrieve_education_level
import uuid

router = APIRouter()

class AddEducationLevel(BaseModel):
    education_level_name: constr(max_length=15)


@router.post("/addEducationLevel")
async def create_education_level(request: AddEducationLevel, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic','student','teacher'])
        if payload:
            education_level_id = str(uuid.uuid4())
            result = await add_education_level(db,education_level_id,request.education_level_name)
            if result:
                response: dict = {"education_level_id": education_level_id,"education_level_name":request.education_level_name}
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": True, "data": response, "detail": "created successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "process error"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"educationLevel - addEducationLevel | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.get("/educationLevel")
async def retrieve_edu_levels(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin', 'manager', 'academic', 'student', 'teacher'])
        if payload:
            result = await retrieve_education_level(db)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "data retrieve error"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"educationLevel - addEducationLevel | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from Authorization.auth import create_access_token
from Databases.models import Teacher
from Loggers.log import err_log
from Function.function import db_dependency
from .teacherFunction import teacher_signin
from pydantic import BaseModel
import json

class TeacherSignInSchema(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/signIn")
async def student_sign_in(request:TeacherSignInSchema, db: db_dependency):
    try:
        payload = await teacher_signin(db,request.username,request.password)
        if payload:
            token = await create_access_token(payload,role="student")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "token":token, "data": payload})
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"status": False, "detail": "invalid user or password"})
    except Exception as e:
        err_log.error(f"teacher SignIn endpoint error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})
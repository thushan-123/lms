from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Function.function import db_dependency
from Loggers.log import err_log, app_log
from Authorization.auth import create_access_token, decode_verify_token
from Schemas.Admin.adminSchema import CreateAdmin, LoginAdmin
from .adminFunction import insert_new_admin_data


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router.post("/createAdmin")
async def create_admin(request: CreateAdmin, db: db_dependency):
    try:
        response = await insert_new_admin_data(db, request.admin_name, request.password, request.email)
        if response:
            app_log.info("admin - insert admin data successfully")
            return JSONResponse(status_code=201, content={"status": True, "detail": "create admin successfully"})
        else:
            app_log.warning("admin - fail to insert admin data")
            return JSONResponse(status_code=400, content={"status": False, "detail": "fail to create admin"})
    except Exception as e:
        err_log.error(f"admin - server error: {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})


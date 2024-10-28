from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Function.function import db_dependency
from Loggers.log import err_log, app_log
from Authorization.auth import create_access_token, oauth2_scheme
from Schemas.Admin.adminSchema import CreateAdmin, LoginAdmin
from .adminFunction import insert_new_admin_data, get_admin_data, admin_verify


router = APIRouter()


@router.post("/createAdmin")
async def create_admin(request: CreateAdmin, db: db_dependency, token: str = Depends(oauth2_scheme)):
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

@router.post("/adminLogin")
async def admin_login(request: LoginAdmin, db: db_dependency):
    try:
        is_verify = await admin_verify(db, request.admin_name, request.password)
        if is_verify:
            payload = await get_admin_data(db, request.admin_name)
            if not (payload is None):
                payload['role'] = 'admin'
                token = await create_access_token(payload, role='admin')
                app_log.info(f"adminLogin - return the access token {request.admin_name}")
                return JSONResponse(status_code=200, content={"status": True, "token": token})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "process-error"})
        else:
            return JSONResponse(status_code=403, content={"status": False, "detail": "invalid username or password"})
    except Exception as e:
        err_log.error(f"adminLogin - server error: {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})






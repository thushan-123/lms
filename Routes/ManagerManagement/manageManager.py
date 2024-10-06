from fastapi import APIRouter , Depends, status
from fastapi.responses import JSONResponse
from Function.function import db_dependency
from Authorization.auth import oauth2_scheme, decode_token_access_role
from Loggers.log import app_log, err_log
from Schemas.ManagerManagement.managerManageSchema import CreateManagerSchema
from .manageManagerFunction import create_manager, retrieve_managers_details

router = APIRouter()

@router.post("/createManager")
async def creating_manager(request: CreateManagerSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin'])
        if payload:
            result = await create_manager(db, request.manager_name, request.manager_email)
            if result:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": True, "detail": "create successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "creation fail or data duplication"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageManager - creating_manager | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.get("/allManagers")
async def retrieve_managers(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload:
            result = await retrieve_managers_details(db)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageManager - retrieve_managers | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})
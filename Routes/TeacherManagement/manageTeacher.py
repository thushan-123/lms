from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Authorization.auth import decode_token_access_role, oauth2_scheme
from Function.function import db_dependency
from Loggers.log import err_log
from Schemas.TeacherManagement.TeacherManagementSchema import TeacherCreateSchema, TeacherUpdateSchema, TeacherStatusSchema
from .manageTeacherFunction import create_teacher, update_teacher, teacher_credentials, change_teacher_status

router = APIRouter()

@router.post("/createTeacher")
async def create_new_teacher(request: TeacherCreateSchema, db: db_dependency,token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','academic','manager'])
        if payload:
            result = await create_teacher(db, dict(request))
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "teacher is created successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "failed to insert branch data. Possible duplicate entry"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageTeacher - createTeacher | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.put("/updateTeacher")
async def update_teacher_details(request: TeacherUpdateSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','academic','manager','teacher'])
        if payload:
            result = await update_teacher(db,str(request.teacher_data[0].teacher_id),dict(request.teacher_data[0]),request.urls)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "update successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": False, "detail": "update fail or teacher not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageTeacher - updateTeacher | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status":False, "detail": "internal server error"})

@router.get("/getTeacherDetails/{teacher_id}")
async def request_teacher_details(teacher_id: str, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','academic','manager','teacher'])
        if payload:
            result = await teacher_credentials(db,teacher_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": jsonable_encoder(result)})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "fail to retrieve teacher credentials or not found"})

        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageTeacher - getTeacherDetails | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.put("/changeTeacherStatus")
async def change_to_teacher_status(request: TeacherStatusSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','academic','manager'])
        if payload:
            result = await change_teacher_status(db,request.teacher_id,request.teacher_current_status)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "successfully change teacher status"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "teacher not found or another issue"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageTeacher - changeTeacherStatus | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})
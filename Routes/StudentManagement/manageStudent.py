from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Function.function import db_dependency
from Loggers.log import app_log,err_log
from Schemas.StudentManagement.studentManageSchema import AddStudent, DeactivateStudent, DeleteStudent
from Authorization.auth import decode_token_without_role, decode_token_access_role
from .manageStudentFunction import get_educational_level, get_education_level_id, insert_student_all_data, \
    insert_education_level, deactivate_students_field, delete_students_cascade

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/educationLevels")
async def get_education_levels(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token,['admin','manager','academic'])
        if payload is not None:
            data_set = await get_educational_level(db)
            if data_set is not None:
                app_log.info("manageStudent - get_education_level | send payload to user")
                return JSONResponse(status_code=200, content={"status": True, "data": list(data_set)})
            else:
                return JSONResponse(status_code=200, content={"status": False, "detail": "no levels in database"})
        else:
            return JSONResponse(status_code=400, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - get_education_levels | server error: {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})


@router.post("/addStudent")
async def adding_student(request: AddStudent, db: db_dependency, token:str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token, ['admin','manager','academic'])
        if payload is not None:
            # insert a student in student table
            # insert a parents in student_parents table
            # insert a siblings in student_siblings table
            # insert a profile image url
            # insert a certificate images urls
            student_id: str = request.student[0].student_id
            edu_level_name: str = request.student[0].education_level_name
            student_data_dict: dict = dict(request.student[0])
            student_data_dict.pop('education_level_name')
            educational_level: bool = await insert_education_level(db, edu_level_name)

            if educational_level is not None:
                student_data_dict['education_level_id'] = await get_education_level_id(db, edu_level_name)
            result = await insert_student_all_data(db,student_id,student_data_dict,dict(request.student_parents[0]),
                                                   request.siblings,request.profile_image_url[0],request.certificate_image_url)
            if result:
                return JSONResponse(status_code=201, content={"status": True, "detail": "data insert successfully"})
            else:
                return JSONResponse(status_code=401, content={"status": False, "detail": "data insert fail"})
        else:
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - addStudent | server error: {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})
'''
@router.get("/getStudentDetails/{student_id}")
async def get_student_details(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
'''

@router.put("/deactivateStudents")
async def deactivate_student(request: DeactivateStudent, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token,['admin','manager','academic'])
        if payload is not None:
            result = await deactivate_students_field(db,request.student_id)
            if result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "successfully deactivated"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "deactivation fail"})
        else:
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - deactivateStudents | error {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})

@router.delete("/deleteStudents")
async def delete_student(request: DeleteStudent, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token, ['admin','manager','academic'])
        if payload is not None:
            result = await delete_students_cascade(db,request.student_id)
            if result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "successfully deleted"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "deletion fail"})
        else:
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - deactivateStudents | error {e}")
        return JSONResponse(status_code=500, content={"status": False, "detail": "internal server error"})








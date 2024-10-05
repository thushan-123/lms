from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Function.function import db_dependency
from Loggers.log import app_log,err_log
from Schemas.StudentManagement.studentManageSchema import AddStudent, DeactivateStudent, DeleteStudent, SearchStudentSchema
from Authorization.auth import decode_token_access_role, oauth2_scheme
from .manageStudentFunction import get_educational_level, get_education_level_id, insert_student_all_data, \
    insert_education_level, deactivate_students_field, delete_students_cascade, get_student_data, admin_get_students_details, \
    search_students

router = APIRouter()


@router.get("/educationLevels")
async def get_education_levels(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic','teacher'])
        if payload is not None:
            data_set = await get_educational_level(db)
            if data_set is not None:
                app_log.info("manageStudent - get_education_level | send payload to user")
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": list(data_set)})
            else:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": False, "detail": "no levels in database"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - get_education_levels | server error: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.post("/addStudent")
async def adding_student(request: AddStudent, db: db_dependency, token:str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials, ['admin','manager','academic'])
        if payload is not None:
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
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": True, "detail": "data insert successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"status": False, "detail": "data insert fail| data is duplicated"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - addStudent | server error: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.get("/getStudentDetails/{student_id}", response_model=AddStudent)
async def get_student_details(student_id: str, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic','teacher','student'])
        if payload is not None:
            result = await get_student_data(db, student_id)
            if result is not None:
                app_log.info(f"managementStudent - getStudentDetailsStudent | send data student_id {str(student_id)}")
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": jsonable_encoder(result)})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "student not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - getStudentDetails | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.put("/deactivateStudents")
async def deactivate_student(request: DeactivateStudent, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload is not None:
            result = await deactivate_students_field(db,request.student_id)
            if result:
                app_log.info(f"managementStudent - deactivateStudent | student_id {str(request.student_id)}")
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "successfully deactivated"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "deactivation fail or student not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - deactivateStudents | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.delete("/deleteStudents")
async def delete_student(request: DeleteStudent, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials, ['admin','manager'])
        if payload is not None:
            result = await delete_students_cascade(db,request.student_id)
            if result:
                app_log.info(f"managementStudent - deleteStudent | student_id {str(request.student_id)}")
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "successfully deleted"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "deletion fail or student not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - deleteStudents | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.get("/getStudents")
async def get_students(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials, ['admin','manager'])
        if payload is not None:
            if payload['role'] == 'admin':
                result = await admin_get_students_details(db)
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            elif payload['role'] in ['manager','academic','teacher']:
                return JSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED, content={"not implemented"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "deletion fail or student not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - getStudents | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})


@router.post("/searchStudents")
async def searching_student(request:SearchStudentSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload is not None:
            if payload['role'] == 'admin':
                result = await search_students(db,'admin',branch_name=request.branch_name,student_id=request.student_id,
                                               student_name=request.student_name)
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            else:
                return JSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED, content={"not implemented"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageStudent - searching_student | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False , "detail": "internal server error"})










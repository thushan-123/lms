from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Authorization.auth import decode_token_access_role, oauth2_scheme
from Loggers.log import app_log,err_log
from Function.function import db_dependency,get_gen_password,generate_unique_username, password_hash
from Schemas.OfficerManagement.officerManagementSchema import CreateOfficerSchema, OfficerUpdateReqSchema, OfficerStatusSchema,OfficerDeleteSchema,OfficerSearchSchema
from Mail import mail
from Mail.html import html_content_username_password
from .manageOfficerFunction import add_officer,retrieve_officer_details,update_officer,update_officer_status,cascade_delete_officers, retrieve_officers,search_officers


router = APIRouter()

@router.post("/createOfficer")
async def create_new_officer(request:CreateOfficerSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload:
            officer_username: str = generate_unique_username(request.officer_data[0].officer_firstname)
            password: str = request.officer_data[0].password
            officer_data_copy = request.officer_data[0].model_copy(update={"officer_username": officer_username})
            result = await add_officer(db,request.officer_data[0].officer_id,dict(officer_data_copy),request.urls)
            if result:
                html_content = html_content_username_password(officer_username,password)
                mail_ = mail.Mail(request.officer_data[0].officer_email,"Username and Password",html_content)
                mail_.send()
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status": True, "detail": "username password send email"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "failed to insert officer data. Possible duplicate entry"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - createOfficer | error {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.get("/getOfficerDetail/{officer_id}")
async def get_officer_info(officer_id: str, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload:
            result = await retrieve_officer_details(db,officer_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": jsonable_encoder(result)})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "officer not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - getOfficerDetail | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.put("/updateOfficer")
async def update_officer_data(request:OfficerUpdateReqSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload:
            result = await update_officer(db,request.officer_data[0].officer_id,dict(request.officer_data[0]),request.urls)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "update successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "fail to update officer data"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - update_officer_data | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.put("/changeOfficerStatus")
async def active_deactivate_officer(request:OfficerStatusSchema,db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload:
            result = await update_officer_status(db,request.officer_id,request.current_status)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "change status successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": False, "detail": "officer not found or another reason"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - active_deactivate_officer | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.delete("/deleteOfficers")
async def delete_officers(request:OfficerDeleteSchema,db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager'])
        if payload:
            result = await cascade_delete_officers(db,request.officer_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "detail": "delete successfully"})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "not found or another reason"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - delete_officers | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.get("/getOfficersDetails")
async def get_officers( db: db_dependency, token: str = Depends(oauth2_scheme),branch_id: str = None):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload:
            result = await retrieve_officers(db,branch_id)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - getOfficerDetails | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})

@router.post("/searchOfficers")
async def search_officers_(request: OfficerSearchSchema, db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token_access_role(token.credentials,['admin','manager','academic'])
        if payload:
            result = await search_officers(db,request.branch_id,request.officer_id,request.officer_name)
            if result:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": True, "data": result})
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": False, "detail": "not found"})
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"manageOfficer - search_officers_ | error - {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": False, "detail": "internal server error"})
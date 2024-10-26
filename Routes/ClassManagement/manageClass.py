from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Loggers.log import app_log, err_log
from Authorization.auth import decode_token_access_role, oauth2_scheme
from Function.function import db_dependency
from Schemas.ClassManagement.classManagementSchema import CreateClassSchema

router = APIRouter()
from fastapi import APIRouter , Depends, status
from Function.function import db_dependency
from Authorization.auth import oauth2_scheme, decode_token_access_role
import Loggers.log
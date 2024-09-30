import os
import jwt
from dotenv import load_dotenv
from typing import Literal
from fastapi import HTTPException
from jose import JWTError

from Loggers.log import err_log

load_dotenv()

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")
MANAGER_SECRET_KEY = os.getenv("MANAGER_SECRET_KEY")
ACADEMIC_SECRET_KEY = os.getenv("ACADEMIC_SECRET_KEY")
TEACHER_SECRET_KEY = os.getenv("TEACHER_SECRET_KEY")
STUDENT_SECRET_KEY = os.getenv("STUDENT_SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

def generate_access_token(key: str, data_set: dict) -> str:
    try:
        encode = data_set.copy()
        token = jwt.encode(encode, key, ALGORITHM)
        return token
    except Exception as e:
        err_log.error(f"generate_access_token auth {e}")


_ROLE = Literal['admin', 'manager', 'academic', 'teacher', 'student']

async def create_access_token(data: dict, role: _ROLE) -> str:
    try:
        if role == 'admin':
            return generate_access_token(ADMIN_SECRET_KEY, data)
        elif role == 'manager':
            return generate_access_token(MANAGER_SECRET_KEY, data)
        elif role == 'academic':
            return generate_access_token(ACADEMIC_SECRET_KEY, data)
        elif role == 'teacher':
            return generate_access_token(TEACHER_SECRET_KEY, data)
        else:
            return generate_access_token(STUDENT_SECRET_KEY, data)
    except Exception as e:
        err_log.error(f"create_access_token auth {e}")

def decode_token(key: str, token: str) -> str:
    try:
        payload = jwt.decode(token, key, ALGORITHM)
        return payload
    except Exception as e:
        err_log.error(f"decode_token auth {e}")

async def decode_verify_token_with_role(token: str, role: _ROLE):
    try:
        if role == 'admin':
            return decode_token(ADMIN_SECRET_KEY, token)
        elif role == 'manager':
            return decode_token(MANAGER_SECRET_KEY, token)
        elif role == 'academic':
            return decode_token(ACADEMIC_SECRET_KEY, token)
        elif role == 'teacher':
            return decode_token(TEACHER_SECRET_KEY, token)
        else:
            return decode_token(STUDENT_SECRET_KEY, token)
    except JWTError as e:
        err_log.error(f"JWT decode error {e}")

async def decode_token_without_role(token: str):
    try:
        # Attempt to decode the token using all possible secret keys
        for secret_key in [ADMIN_SECRET_KEY, MANAGER_SECRET_KEY, ACADEMIC_SECRET_KEY, TEACHER_SECRET_KEY, STUDENT_SECRET_KEY]:
            try:
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                return payload
            except jwt.InvalidTokenError:
                continue  # Try the next secret key

        # If none of the secret keys worked, the token is invalid
        return None

    except jwt.ExpiredSignatureError:
        err_log.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        err_log.error("Invalid token")
        return None

async def decode_token_access_role(token: str, access_list: list):
    payload = await decode_token_without_role(token)
    if payload is not None:
        if payload['role'] in access_list:
            return payload
        else:
            return None
    else:
        return None




import os
import jwt
from dotenv import load_dotenv
from typing import Literal

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

async def decode_verify_token(token: str, role: _ROLE):
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



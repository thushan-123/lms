from sqlalchemy.orm import Session
from Function.function import  password_hash, verify_password
from Loggers.log import err_log, app_log
from Databases.models import Teacher


async def teacher_signin(db: Session, username: str, password:str):
    try:
        data = db.query(Teacher).filter(Teacher.teacher_username==username,Teacher.teacher_active==True).first()
        if data:
            if verify_password(data.teacher_password, password_hash(password)):
                payload = {
                    "teacher_id" : data.teacher_id,
                    "firstname" : data.teacher_firstname,
                    "lastname" : data.teacher_lastname,
                    "role": "teacher",
                    "email": data.teacher_email,
                    "branch_id" : data.branch_id
                }
                app_log.info(f"return the payload {str(payload)}")
                return payload
            else:
                return None
        else:
            return None
    except Exception as e:
        err_log.error(f"teacher signin error : {e}")
        return None
from sqlalchemy.orm import Session
from Function.function import  password_hash, verify_password
from Loggers.log import err_log, app_log
from Databases.models import Student


async def student_signin(db: Session, username: str, password:str):
    try:
        data = db.query(Student).filter(Student.username==username,Student.active==True).first()
        if data:
            if verify_password(data.password, password_hash(password)):
                payload = {
                    "student_id" : data.student_id,
                    "firstname" : data.firstname,
                    "lastname" : data.lastname,
                    "role": "student",
                    "email": data.email,
                    "branch_id" : data.branch_id
                }
                app_log.info(f"return the payload {str(payload)}")
                return payload
            else:
                return None
        else:
            return None
    except Exception as e:
        err_log.error(f"student signin error : {e}")
        return None
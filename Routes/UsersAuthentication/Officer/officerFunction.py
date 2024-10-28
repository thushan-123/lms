from sqlalchemy.orm import Session
from Function.function import  password_hash, verify_password
from Loggers.log import err_log, app_log
from Databases.models import Officer


async def officer_signin(db: Session, username: str, password:str):
    try:
        data = db.query(Officer).filter(Officer.officer_username==username,Officer.officer_active==True).first()
        if data:
            if verify_password(data.password, password_hash(password)):
                payload = {
                    "officer_id" : data.officer_id,
                    "firstname" : data.officer_firstname,
                    "lastname" : data.officer_lastname,
                    "role": "officer",
                    "email": data.officer_email,
                    "branch_id" : data.branch_id
                }
                app_log.info(f"return the payload {str(payload)}")
                return payload
            else:
                return None
        else:
            return None
    except Exception as e:
        err_log.error(f"officer signin error : {e}")
        return None
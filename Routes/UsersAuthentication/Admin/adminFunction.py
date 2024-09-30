from Databases.models import Admin
from sqlalchemy.orm import Session
from Function.function import password_hash, verify_password
from Loggers.log import app_log, err_log
from sqlalchemy import update
from pydantic import EmailStr

async def insert_new_admin_data(db: Session, admin_name: str, password: str, email: EmailStr) -> bool:
    try:
        hash_password = password_hash(password)
        query = Admin(admin_name=admin_name, password=hash_password, email=email)
        db.add(query)
        db.commit()
        db.refresh(query)
        app_log.info("adminFunction - insert a new admin data")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"adminFunction - admin data insert fail {e}")
        return False


# get the Admin data in database
async def get_admin_data(db:Session, admin_name: str):
    try:
        data = db.query(Admin).filter(Admin.admin_name==admin_name).first() # admin_name is unique
        if not (data is None):
            payload = {"admin_id": data.admin_id, "admin_name": data.admin_name, "role":"admin", "email": data.email}
            app_log.info("adminFunction get_admin_data | return the payload")
            return payload
        else:
            return None
    except Exception as e:
        err_log.error(f"adminFunction get_admin_data | {e}")
        return None


async def admin_verify(db: Session, admin_name: str, password: str) -> bool:
    try:
        data = db.query(Admin).filter(Admin.admin_name==admin_name).first()
        if not (data is None):
            is_verify = verify_password(data.password, password_hash(password))
            app_log.info("adminFunction admin_verify_get_data | verify the password")
            if is_verify:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        err_log.error(f"adminFunction admin_verify_get_data | {e}")
        return False



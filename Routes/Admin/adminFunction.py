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
        err_log.error(f"adminFunction - admin data insert fail {e}")
        return False



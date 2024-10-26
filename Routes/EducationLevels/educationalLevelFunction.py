from sqlalchemy.orm import Session
from Loggers.log import err_log, app_log
from Databases.models import EducationLevel

async def add_education_level(db: Session, education_level_id, education_level_name: str) -> bool:
    try:
        db.add(EducationLevel(education_level_id=education_level_id,education_level_name=education_level_name))
        db.commit()
        app_log.info(f"add a new education level {education_level_id} {education_level_name}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"educationLevelFunction - add_education_level | error - {e}")
        return False

async def retrieve_education_level(db: Session):
    try:
        data_list = db.query(EducationLevel).all()
        payload = []

        for data in data_list:
            payload.append({
                "education_level_id": data.education_level_id,
                "education_level_name": data.education_level_name
            })
        app_log.info(f"retrieve the education level : {str(payload)}")
        return payload
    except Exception as e:
        db.rollback()
        err_log.error(f"educationLevelFunction - retrieve_education_level | error - {e}")
        return None

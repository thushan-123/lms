from dns.resolver import query

from Databases.models import Student, StudentParents, StudentSiblings, EducationLevel, ProfileImagesStudent, CertificateImagesStudent
from sqlalchemy.orm import Session
from Function.function import password_hash, verify_password
from sqlalchemy import update, delete
from pydantic import EmailStr
# db.add(StudentParents(student_id=student_id ,**parents))
from Loggers.log import app_log, err_log

async def insert_student_all_data(db:Session, student_id: str
                                  ,student:dict, parents: dict,
                                  siblings:list, prof_image_url: str, certificate_urls: list):
    try:
        db.add(Student(**student))
        db.flush()
        StudentParents(student_id=student_id, **parents)
        db.add_all([StudentSiblings(student_id=student_id, **data.dict()) for data in siblings])
        db.add(ProfileImagesStudent(student_id=student_id, profile_image_url=prof_image_url))
        db.add_all(CertificateImagesStudent(student_id=student_id, certificate_image_url=url) for url in certificate_urls)
        db.commit()
        app_log.info("manageStudentFunction - insert_student_all_data | data insert successfully")
        return True
    except Exception as e:
        err_log.error(f"manageStudentFunction - insert_student_all_data | error {e}")
        return False

async def insert_education_level(db: Session, level_name: str) -> bool:
    try:
        # check education_level_name in the table | level_name is exits not insert data
        check = db.query(EducationLevel).filter(EducationLevel.education_level_name == level_name).first()
        if check is None:
            query = EducationLevel(education_level_name=level_name)
            db.add(query)
            db.commit()
            db.refresh(query)
            app_log.info("manageStudentFunction - insert_education_level | data insert successfully")
            return True
        else:
            return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageStudentFunction - insert_educational_level | data insert fail {e}")
        return False

async def get_education_level_id(db:Session, level_name:str):
    try:
        data = db.query(EducationLevel).filter(EducationLevel.education_level_name == level_name).first()
        return data.education_level_id
    except Exception as e:
        err_log.error(f"educational_level_get_error manageStuFunc {e}")
        return None

async def get_educational_level(db: Session):
    try:
        data_set = db.query(EducationLevel).all()
        app_log.info("manageStudentFunction - insert_get_educational_level | data retrieve successfully")
        if data_set is not None:
            payload = set()
            for data in data_set:
                payload.add(data.education_level_name)
            return payload
        else:
            return None
    except Exception as e:
        db.rollback()
        err_log.error(f"manageStudentFunction - insert_get_educational_level | data retrieve fail {e}")
        return None

async def deactivate_students_field(db: Session, student_id: list) -> bool:
    try:
        update_query = update(Student).where(Student.student_id.in_(student_id)).values(active=False)
        db.execute(update_query)
        db.flush()
        db.commit()
        app_log.info("manageStudentFunction - deactivate_students_field | successfully update active field")
        return True
    except Exception as e:
        err_log.error(f"manageStudentFunction - deactivate_students_field | error {e}")
        return False

async def delete_students_cascade(db: Session, student_id: list) -> bool:
    try:
        delete_query = delete(Student).where(Student.student_id.in_(student_id))
        db.execute(delete_query)
        db.flush()
        db.commit()
        app_log.info("manageStudentFunction - delete_students_cascade | successfully deleted")
        return True
    except Exception as e:
        err_log.error(f"manageStudentFunction - delete_student_cascade | error {e}")
        return False

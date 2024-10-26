import json
from sqlalchemy.orm import Session, joinedload, selectinload
from Loggers.log import err_log, app_log
from Databases.models import Teacher, TeacherCertificateImages
from sqlalchemy import delete, update
from Schemas.TeacherManagement.TeacherManagementSchema import TeacherSchema,TeacherUpdateSchema
from Function.function import password_hash

async def create_teacher(db: Session, teacher_credential: dict) -> bool:
    try:
        teacher_credential["teacher_password"] = password_hash(teacher_credential["teacher_password"])
        db.add(Teacher(**teacher_credential))
        db.commit()
        app_log.info(f"manageTeacherFunction - create_new_teacher | teacher credentials {str(teacher_credential)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageTeacherFunction - create_new_teacher | error {e}")
        return False

async def update_teacher(db: Session, teacher_id: str, teacher_credential: dict, urls: list) -> bool:
    try:
        # Check if teacher exists before proceeding
        teacher_exists = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if not teacher_exists:
            app_log.error(f"Teacher with id {teacher_id} not found.")
            return False

        update_query = update(Teacher).where(Teacher.teacher_id == teacher_id).values(**teacher_credential)
        db.execute(update_query)

        # Delete existing certificate images associated with this teacher
        db.query(TeacherCertificateImages).filter(TeacherCertificateImages.teacher_id == teacher_id).delete()

        for url in urls:
            db.add(TeacherCertificateImages(teacher_id=teacher_id, image_url=url))

        db.commit()
        app_log.info(f"manageTeacherFunction - updateTeacher | teacher credentials {str(teacher_credential)} urls {str(urls)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageTeacherFunction - update_teacher | error {e}")
        return False

async def teacher_credentials(db: Session, teacher_id: str):
    try:
        data = db.query(Teacher).join(Teacher.teacher_certificate_images).filter(Teacher.teacher_id==teacher_id).first()

        if not data:
            return False

        teacher_data = TeacherSchema(
            teacher_id = data.teacher_id,
            teacher_firstname= data.teacher_firstname,
            teacher_lastname= data.teacher_lastname,
            teacher_email= data.teacher_email,
            teacher_mobile= data.teacher_mobile,
            subject= data.subject,
            branch_id= data.branch_id,
            education_level_id= data.education_level_id,
            teacher_address= json.dumps(data.teacher_address),
            province= data.province,
            district= data.district,
            home_town= data.home_town,
            teacher_gender= data.teacher_gender,
            teacher_NIC= data.teacher_NIC,
            teacher_school= data.teacher_school,
            teacher_description= data.teacher_description
        )
        urls = [url.image_url for url in data.teacher_certificate_images]

        teacher_response_model = TeacherUpdateSchema(
            teacher_data= [teacher_data],
            urls= urls
        )
        app_log.info(f"manageTeacherFunction - teacher_credentials | retrieve teacher credentials {str(teacher_id)}")
        return teacher_response_model
    except Exception as e:
        err_log.error(f"manageTeacherFunction - teacher_credentials | error {e}")
        return False

async def change_teacher_status(db: Session, teacher_id: str, current_status: bool) -> bool:
    try:
        update_query = update(Teacher).where(Teacher.teacher_id==teacher_id).values(teacher_active=not current_status)
        db.execute(update_query)
        db.commit()
        app_log.info(f"manageTeacherFunction - change_teacher_status | change to status {teacher_id} ")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageTeacherFunction - change_teacher_status | error {e}")
        return False




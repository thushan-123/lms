from Databases.models import Student, StudentParents, StudentSiblings, EducationLevel, ProfileImagesStudent, CertificateImagesStudent, Branch
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import update, delete, and_
from pydantic import EmailStr
from Loggers.log import app_log, err_log
from Schemas.StudentManagement.studentManageSchema import AddStudent, StudentParentsSchema, StudentSchema, StudentSiblingsSchema \
    , ProfileImageStudentSchema, CertificateImagesStudentSchema
import json

async def insert_student_all_data(db:Session, student_id: str
                                  ,student:dict, parents: dict,
                                  siblings:list, prof_image_url: str, certificate_urls: list):
    try:
        db.add(Student(**student))
        db.flush()
        db.add(StudentParents(student_id=student_id, **parents))
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

async def get_student_data(db: Session, student_id: str):
    try:
        data = db.query(Student).options(
            joinedload(Student.student_parents),
            joinedload(Student.student_siblings),
            joinedload(Student.student_profile_image),
            joinedload(Student.student_certificate_images)
        ).filter(Student.student_id == student_id).first()

        education_level = db.query(EducationLevel).filter(EducationLevel.education_level_id == data.education_level_id).first()

        app_log.info("manageStudentFunction - get_student_data | successfully retrieve student data")

        if not data:
            return None

        student = StudentSchema(
            student_id = data.student_id,
            firstname = data.firstname,
            lastname = data.lastname,
            email = data.email,
            address = json.dumps(data.address),
            gender = data.gender,
            admission_free_is_paid = data.admission_free_is_paid,
            mother_tung = data.mother_tung,
            NIC = data.NIC,
            school = data.school,
            mobile = data.mobile,
            education_level_name = education_level.education_level_name,
            branch_id = data.branch_id
        )
        parents = StudentParentsSchema(
            father_name = data.student_parents[0].father_name,
            father_mobile = data.student_parents[0].father_mobile,
            father_email = data.student_parents[0].father_email,
            father_occupation = data.student_parents[0].father_occupation,
            father_address = json.dumps(data.student_parents[0].father_address),
            mother_name = data.student_parents[0].mother_name,
            mother_mobile = data.student_parents[0].mother_mobile,
            mother_email = data.student_parents[0].mother_email,
            mother_occupation = data.student_parents[0].mother_occupation,
            mother_address = json.dumps(data.student_parents[0].mother_address),
            info_send = data.student_parents[0].info_send
        )
        siblings = [StudentSiblingsSchema(
            name = siblingData.name,
            DOB = siblingData.DOB,
            gender = siblingData.gender,
            mobile = siblingData.mobile
        ) for siblingData in data.student_siblings]

        #profile_image_url = [ProfileImageStudentSchema(profile_image_url = url.profile_image_url) for url in data.student_profile_image]
        #certificate_image_url = [CertificateImagesStudentSchema(certificate_image_url = url.certificate_image_url) for url in data.student_certificate_images]
        profile_image_url = []
        for url in data.student_profile_image:
            profile_image_url.append(url.profile_image_url)

        certificate_image_url = []
        for url in data.student_certificate_images:
            certificate_image_url.append(url.certificate_image_url)

        return AddStudent(
            student = [student],
            profile_image_url = profile_image_url,
            certificate_image_url = certificate_image_url,
            student_parents = [parents],
            siblings = siblings
        )


    except Exception as e:
        err_log.error(f"manageStudentFunction - get_student_data | error {e}")
        return None

async def admin_get_students_details(db: Session) -> list:
    try:
        data_list = db.query(Student).options(joinedload(Student.branch)).all()

        if not data_list:
            return ["not found"]

        data_list_dict = [{
            "student_id": data.student_id,
            "firstname": data.firstname,
            "lastname": data.lastname,
            "branch_name" : data.branch.branch_name,
            "active": data.active
        } for data in data_list]
        return data_list_dict
    except Exception as e:
        err_log.error(f"manageStudentFunction - admin_get_students_details | error {e}")
        return ["error"]

async def search_students(db: Session, role:str, user_id: str = None,branch_name: str = None, student_id: str = None, student_name: str = None):
    try:
        firstname: str =""
        lastname: str =""
        if student_name is not None:
            firstname = student_name.split(" ")[0]
            if len(student_name.split(" "))> 1:
                lastname = student_name.split(" ")[1]

        data_list = db.query(Student).join(Student.branch).options(joinedload(Student.branch))
        filters: list = []
        if role != 'admin':
            return "not implemented"
            #data_list.filter() # not implemented
        else:
            if branch_name:
                filters.append(Branch.branch_name == branch_name)

        if student_id:
            filters.append(Student.student_id == student_id)
        if student_name:
            filters.append(Student.firstname == firstname)
            if lastname:
                filters.append(Student.lastname == lastname)

        data_list = data_list.filter(and_(*filters))

        data_list_dict = [{
            "student_id": data.student_id,
            "firstname": data.firstname,
            "lastname": data.lastname,
            "branch_name": data.branch.branch_name,
            "active": data.active
        } for data in data_list]
        return data_list_dict
    except Exception as e:
        err_log.error(f"manageStudentFunction - search_students | error {e}")
        return "error"

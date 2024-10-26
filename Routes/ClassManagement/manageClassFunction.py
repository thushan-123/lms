import json
from sqlalchemy import update , and_
from sqlalchemy.orm import Session, joinedload
from Databases.models import Classes, ClassImages, ClassFees, ClassType, ClassBranch
from Loggers.log import app_log, err_log
from Schemas.ClassManagement.classManagementSchema import ClassDataResponseSchema

async def retrieve_class_types(db:Session):
    try:
        data_list = db.query(ClassType).all()

        if not data_list:
            return None

        payload : list = []
        for data in data_list:
            payload.append({
                "class_type_id": data.class_type_id,
                "class_type": data.class_type
            })
        return payload
    except Exception as e:
        db.rollback()
        err_log.error(f"manageClassFunction - retrieve_class_types | error - {e}")
        return None

async def create_new_class(db: Session,class_id: str,class_data: dict) -> bool:
    try:
        db.add(Classes(class_id=class_id,
                       class_name=class_data["class_name"],
                       teacher_id=class_data["teacher_id"],
                       class_type_id=class_data["class_type_id"],
                       education_level_id=class_data["education_level_id"],
                       about=class_data["about"]))

        class_fees_list: list = class_data["class_fees"]

        for data in class_fees_list:
            db.add(ClassFees(class_id=class_id,class_type_id=data["class_type_id"],class_fee=data["class_fee"]))

        for url in class_data["urls"]:
            db.add(ClassImages(class_id=class_id,url=url))

        for branch_id in class_data["branch_id"]:
            db.add(ClassBranch(class_id=class_id,branch_id=branch_id))

        db.commit()
        app_log.info(f"create a new class class_id: {class_id} - class data: {str(class_data)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageClassFunction - create_new_class | error - {e}")
        return False

async def retrieve_class_data(db: Session,class_id: str,branch_id=None):
    try:
        filters = [Classes.class_id == class_id]

        if branch_id:
            filters.append(ClassBranch.branch_id==branch_id)

        data_ = db.query(Classes).options(
            joinedload(Classes.class_fees),
            joinedload(Classes.class_images),
            joinedload(Classes.class_branch)
        ).filter(and_(filters)).first()

        branch_id = [data.branch_id for data in data_.class_branch]
        class_fees = [{
            "class_type_id": data.class_type_id,
            "class_fee": data.class_fee
        } for data in data_.class_fees]

        urls =[data.url for data in data_.class_images]

        payload = ClassDataResponseSchema(
            class_id = data_.class_id,
            class_name = data_.class_name,
            branch_id = branch_id,
            teacher_id = data_.teacher_id,
            class_type_id = data_.class_type_id,
            class_fees = class_fees,
            education_level_id = data_.education_level_id,
            about = data_.about,
            urls = urls
        )
        app_log.info(f"retrieve the class data using class_id : {class_id}")
        return payload
    except Exception as e:
        db.rollback()
        err_log.error(f"manageClassFunction - retrieve_class_data | error - {e}")
        return None

async def change_class_status(db: Session, class_id: str, current_status: bool) -> bool:
    try:
        query = update(Classes).where(Classes.class_id==class_id).values(class_active= not current_status)
        db.execute(query)
        db.commit()
        app_log.info(f"change the class status class_id: {class_id} - current_status {str(current_status)} to change {str(not current_status)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageClassFunction - change_class_status | error - {e}")
        return False

async def cascade_delete_class(db:Session, class_id: str) -> bool:
    try:
        db.query(Classes).filter(Classes.class_id==class_id).delete()
        db.commit()
        app_log.info(f"delete class  class_id: {class_id}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageClassFunction - cascade_delete_class | error - {e}")
        return False

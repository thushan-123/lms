import json
from sqlalchemy.orm import Session, joinedload, selectinload
from Loggers.log import err_log, app_log
from Databases.models import Branch, BranchHalls, BranchImages
from sqlalchemy import delete, update
from Schemas.BranchManagement.branchManagementSchema import BranchUpdateSchema, BranchUpdateRequestSchema

async def create_branch(db: Session, branch_id: str, branch: dict, branch_halls: list, branch_images: list) -> bool:
    try:
        db.add(Branch(**branch))
        db.flush()

        for hall_name in branch_halls:
            db.add(BranchHalls(branch_id=branch_id, hall_name=hall_name))

        for image_url in branch_images:
            db.add(BranchImages(branch_id=branch_id, image_url=image_url))

        db.commit()
        db.flush()
        app_log.info(
            f"manageBranchFunction - create_branch | create successfully {str(branch), str(branch_halls), str(branch_images)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageBranchFunction - create_branch | error {e}")
        return False

async def delete_branch_cascade(db: Session, branch_id: list) -> bool:
    try:
        delete_to = db.query(Branch).options(selectinload(Branch.branch_halls), selectinload(Branch.branch_images)).filter(Branch.branch_id.in_(branch_id)).all()
        if not delete_to:
            return False
        for branch in delete_to:
            db.delete(branch)
        db.commit()
        db.flush()
        app_log.info(f"manageBranchFunction - delete_branch_cascade | delete branches {str(branch_id)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageBranchFunction - delete_branch_cascade | error {e}")
        return False

async def update_branch_active_field(db: Session, branch_id: str, status: bool):
    try:
        update_query = update(Branch).where(Branch.branch_id == branch_id).values(active= not status)
        db.execute(update_query)
        db.commit()
        app_log.info(f"managementBranchFunction - update_branch_active_field | update active field {branch_id}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageBranchFunction - update_branch_active_field | error {e}")
        return False

async def update_branch(db: Session,branch_id: str, branch: dict, branch_halls: list, branch_images: list) -> bool:
    try:
        update_branch_query = update(Branch).where(Branch.branch_id==branch_id).values(**branch)
        db.execute(update_branch_query)

        db.query(BranchHalls).filter(BranchHalls.branch_id == branch_id).delete()
        for hall_name in branch_halls:
            db.add(BranchHalls(branch_id=branch_id, hall_name=hall_name))

        db.query(BranchImages).filter(BranchImages.branch_id == branch_id).delete()
        for image_url in branch_images:
            db.add(BranchImages(branch_id=branch_id, image_url=image_url))

        db.flush()
        db.commit()
        app_log.info(f"manageBranchFunction - update_branch | branch updates {str(branch), str(branch_halls), str(branch_images)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageBranchFunction - update_branch | error {e}")
        return False

async def retrieve_branch(db: Session, branch_id: str):
    try:
        data = (db.query(Branch).options(joinedload(Branch.branch_halls),
                                        joinedload(Branch.branch_images)).
                                        filter(Branch.branch_id==branch_id)).first()
        if not data:
            return None
        branch_data = BranchUpdateSchema(
            branch_id=data.branch_id,
            branch_name=data.branch_name,
            address=json.dumps(data.address),
            email=data.email,
            location=data.location,
            mobile=data.mobile,
            open_time=data.open_time,
            close_time=data.close_time,
            description=data.description,
            branch_manager_id=data.branch_manager_id
        )

        branch_halls = [hall.hall_name for hall in data.branch_halls]

        branch_images = [image.image_url for image in data.branch_images]

        return BranchUpdateRequestSchema(
            branch = [branch_data],
            branch_halls = branch_halls,
            branch_images_urls = branch_images
        )
    except Exception as e:
        err_log.error(f"manageStudentFunction - get_branch_data | error {e} branch_id: {str(branch_id)}")
        return None

async def retrieve_branches(db: Session):
    try:
        data_object_list = db.query(Branch).options(joinedload(Branch.branch_manager)).all()

        if not data_object_list:
            return "not found or no branches"

        data_list = [{
            "branch_id": data.branch_id,
            "branch_name": data.branch_name,
            "manager_id": data.branch_manager.manager_id,
            "branch_manager": data.branch_manager.manager_name,
            "mobile": data.mobile,
            "email": data.email,
            "open_time": data.open_time
        } for data in data_object_list]
        app_log.info(f"manageBranchFunction - retrieve_branches | return data {str(data_list)}")
        return data_list
    except Exception as e:
        err_log.error(f"manageBranchFunction - retrieve_branches | error {e}")
        return None


from sqlalchemy.orm import Session, joinedload, selectinload
from Loggers.log import err_log, app_log
from Databases.models import BranchManager
from sqlalchemy import delete, update

async def create_manager(db: Session, manager_name: str, manager_email: str) -> bool:
    try:
        db.add(BranchManager(manager_name=manager_name,manager_email=manager_email))
        db.commit()
        db.flush()
        app_log.info(f"manageManagerFunction - create_manager | create manager {manager_name,manager_email}")
        return True
    except Exception as e:
        err_log.error(f"manageManagerFunction - create_manager | error {e}")
        return False

async def retrieve_managers_details(db: Session):
    try:
        data_set= db.query(BranchManager)
        data_list = []
        for data in data_set:
            data_list.append({"manager_id": data.manager_id, "manager_name": data.manager_name})
        app_log.info(f"manageManagerFunction - retrieve_managers_details | retrieve data {str(data_list)}")
        return data_list
    except Exception as e:
        err_log.error(f"manageManagerFunction - retrieve_manager_details | error {e}")


import json
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import update, and_
from Databases.models import Officer, OfficerCertificateImages
from Loggers.log import err_log, app_log
from Function.function import password_hash
from Schemas.OfficerManagement.officerManagementSchema import OfficerDetailsSchema,OfficerDetailsResponseSchema

async def add_officer(db: Session,officer_id: str, officer_data: dict, urls: list) -> bool:
    try:
        officer_data['password'] = password_hash(officer_data['password'])
        db.add(Officer(**officer_data))

        for url in urls:
            db.add(OfficerCertificateImages(officer_id=officer_id, image_url=url))
        db.commit()
        app_log.info(f"manageOfficerFunction - add_officer | insert successfully  officer-data :{str(officer_data)} images: {str(urls)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - add_officer | error {e}")
        return False

async def retrieve_officer_details(db: Session, officer_id:str):
    try:
        data = db.query(Officer).join(OfficerCertificateImages).filter(Officer.officer_id==officer_id).first()

        if not data:
            return None

        officer_info = [OfficerDetailsSchema(
            officer_id = data.officer_id,
            officer_firstname = data.officer_firstname,
            officer_lastname = data.officer_lastname,
            officer_address = json.dumps(data.officer_address),
            province = data.province,
            district = data.district,
            home_town = data.home_town,
            officer_email = data.officer_email,
            officer_gender = data.officer_gender,
            officer_mobile = data.officer_mobile,
            branch_id = data.branch_id,
            officer_NIC = data.officer_NIC,
            officer_school = data.officer_school,
            education_level_id = data.education_level_id
        )]

        print(officer_info)
        urls = [url.image_url for url in data.officer_certificate_images]


        officer_response_model = OfficerDetailsResponseSchema(
            officer_data = officer_info,
            urls = urls
        )
        app_log.info(f"retrieve data officer details using officer_id: {str(officer_id)}")

        return officer_response_model
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - retrieve_officer_details | error - {e}")
        return None

async def cascade_delete_officers(db: Session,officer_id: list) -> bool:
    try:
        officers = db.query(Officer).filter(Officer.officer_id.in_(officer_id)).all()

        if not officers:
            return False

        for officer in officers:
            db.delete(officer)

        db.commit()
        app_log.info(f"delete officers - officer_id : {str(officer_id)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - cascade_delete_officers : error - {e}")
        return False

async def retrieve_officers(db: Session, branch_id: str=None):
    try:
        if not branch_id:
            data_list = db.query(Officer).all()
        else:
            data_list = db.query(Officer).filter(Officer.branch_id==branch_id).all()

        print(data_list)

        if not data_list:
            return False

        payload : list = [{
            "officer_id": data.officer_id,
            "officer_firstname": data.officer_firstname,
            "officer_lastname": data.officer_lastname,
            "officer_email": data.officer_email,
            "officer_mobile": data.officer_mobile,
            "officer_status": data.officer_active
        } for data in data_list]
        app_log.info(f"retrieve the officers information : branch_id {branch_id}")
        return payload

    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - retrieve_officers | error - {e}")
        return False

async def update_officer_status(db: Session, officer_id:str, current_status: bool) -> bool:
    try:
        query = update(Officer).where(Officer.officer_id==officer_id).values(officer_active= not current_status)
        db.execute(query)
        db.commit()
        app_log.info(f"change the officer status officer_id: {officer_id} - current_status {str(current_status)} to change {str(not current_status)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - update_officer_status | error - {e}")
        return False

async def search_officers(db:Session, branch_id: str, officer_id: str = None ,officer_name: str= None):
    try:
        firstname: str = ""
        lastname : str = ""
        filters: list = []
        if not officer_name:
            firstname = officer_name.split(" ")[0]
            if len(officer_name.split(" ")) >1:
                lastname = officer_name.split(" ")[1]

        if branch_id:
            filters.append(Officer.branch_id==branch_id)

        if officer_id:
            filters.append(Officer.officer_id==officer_id)

        if firstname:
            filters.append(Officer.officer_firstname==firstname)

        if lastname:
            filters.append(Officer.officer_lastname==lastname)

        data_list = db.query(Officer).filter(and_(*filters)).all()

        payload: list =[{
            "officer_id": data.officer_id,
            "officer_firstname": data.officer_firstname,
            "officer_lastname": data.officer_lastname,
            "officer_email": data.officer_email,
            "officer_mobile": data.officer_mobile,
            "officer_status": data.officer_active
        } for data in data_list]

        app_log.info(f"officer search data retrieve successfully")
        return payload
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - search_officers | error - {e}")
        return None

async def update_officer(db: Session,officer_id: str, officer_data: dict, urls) -> bool:
    try:
        query = update(Officer).where(Officer.officer_id==officer_id).values(**officer_data)
        db.execute(query)

        db.query(OfficerCertificateImages).filter(OfficerCertificateImages.officer_id==officer_id).delete()

        for url in urls:
            db.add(OfficerCertificateImages(officer_id=officer_id,image_url=url))

        db.commit()
        app_log.info(f"officer detail update successfully data : {str(officer_data)}")
        return True
    except Exception as e:
        db.rollback()
        err_log.error(f"manageOfficerFunction - search_officers | error - {e}")
        return False




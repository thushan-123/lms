from Databases.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, JSON, DateTime, Time, Text
import uuid
from Function.function import get_sl_DateTime
from nanoid import generate

class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    admin_name = Column(String(20), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(40), unique=True, nullable=False, index=True)

class ProfileImagesStudent(Base):
    __tablename__ = "profile_images"

    profile_image_id = Column(Integer, nullable=False, index=True, primary_key=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    profile_image_url = Column(Text, nullable=False)

class CertificateImagesStudent(Base):
    __tablename__ = "certificate_images_student"

    certificate_image_id = Column(Integer, nullable=False, index=True, primary_key=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    certificate_image_url = Column(Text, nullable=False)


class EducationLevel(Base):
    __tablename__ = "education_level"

    education_level_id = Column(String(36), nullable=False, index=True, primary_key=True, default=lambda : uuid.uuid4())
    education_level_name = Column(String(15), nullable=False, index=True)

class BranchManager(Base):
    __tablename__ = "branch_manager"

    manager_id = Column(String(10), nullable=False, index=True, primary_key=True, default= lambda : generate(size=10))


class Branch(Base):
    __tablename__ = "branch"

    branch_id = Column(String(8), nullable=False, index=True, primary_key=True, default= lambda : generate(size=8))
    branch_name = Column(String(20), nullable=False, unique=True, index=True)
    address = Column(JSON, nullable=False)
    location = Column(String(10), nullable=False)
    mobile = Column(Integer, nullable=False, index=True)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    hall = Column(JSON)
    active = Column(Boolean, nullable=False, default=True)
    branch_manager_id = Column(String(10)) # , ForeignKey("branch_manager.manager_id")
    created = Column(DateTime, nullable=False, default= lambda : get_sl_DateTime())


class Student(Base):
    __tablename__ = "student"

    student_id = Column(String(15), primary_key=True, nullable=False, unique=True, index=True)
    firstname = Column(String(15), nullable=False)
    lastname = Column(String(15), nullable=False)
    email = Column(String(40), nullable=False, unique=True, index=True)
    address = Column(JSON, nullable=False)
    gender = Column(Boolean, nullable=False) # male -> true | female -> false
    admission_free_is_paid = Column(Boolean, nullable=False)
    mother_tung = Column(String(10))
    NIC = Column(String(14))
    school = Column(String(50))
    mobile = Column(Integer, unique=True, index=True)
    education_level_id = Column(String(36), ForeignKey("education_level.education_level_id"), index=True)
    branch_id = Column(String(8)) # , ForeignKey("branch.branch_id")
    created = Column(DateTime, nullable=False, index=True, default= lambda : get_sl_DateTime())
    active = Column(Boolean, nullable=False, default=True)

class StudentParents(Base):
    __tablename__ = "student_parents"

    row_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    father_name = Column(String(25))
    father_mobile = Column(Integer, unique=True)
    father_email = Column(String(40), unique=True)
    father_occupation = Column(String(15))
    father_address = Column(JSON)
    mother_name = Column(String(25))
    mother_mobile = Column(Integer, unique=True)
    mother_email = Column(String(40), unique=True)
    mother_occupation = Column(String(15))
    mother_address = Column(JSON)
    info_send = Column(Boolean) # father -> true | mother -> false


class StudentSiblings(Base):
    __tablename__ = "student_siblings"

    row_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    name = Column(String(40), nullable=False)
    DOB = Column(Date)
    gender = Column(Boolean, nullable=False)  # male -> true | female -> false
    mobile = Column(Integer)






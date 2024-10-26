from operator import index

from Databases.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, JSON, DateTime, Time, Text, Float, PrimaryKeyConstraint
import uuid
from Function.function import get_sl_DateTime
from nanoid import generate
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    admin_name = Column(String(20), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(40), unique=True, nullable=False, index=True)


class EducationLevel(Base):
    __tablename__ = "education_level"

    education_level_id = Column(String(36), nullable=False, index=True, primary_key=True, default=lambda : uuid.uuid4())
    education_level_name = Column(String(15), nullable=False, index=True)

class BranchManager(Base):
    __tablename__ = "branch_manager"

    manager_id = Column(String(10), nullable=False, index=True, primary_key=True, default= lambda : generate(size=10))
    manager_name = Column(String(30), index=True, nullable=False, unique=True)
    manager_email = Column(String(40), nullable=False, index=True, unique=True)

    # relationship -> branch
    branch = relationship("Branch", back_populates="branch_manager", cascade="all, delete-orphan", lazy="joined")


class Branch(Base):
    __tablename__ = "branch"

    branch_id = Column(String(8), nullable=False, index=True, primary_key=True)
    branch_name = Column(String(20), nullable=False, unique=True, index=True)
    address = Column(JSON, nullable=False)
    email = Column(String(40), nullable=False, unique=True, index=True)
    location = Column(String(10), nullable=False)
    mobile = Column(Integer, nullable=False, index=True)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    description = Column(Text)
    active = Column(Boolean, nullable=False, default=True)
    branch_manager_id = Column(String(10), ForeignKey("branch_manager.manager_id"))
    created = Column(DateTime, nullable=False, default= lambda : get_sl_DateTime())


    # relationship -> Student
    student = relationship("Student", back_populates="branch", cascade="all, delete-orphan", lazy="joined")
    # relationship -> BranchHalls
    branch_halls = relationship("BranchHalls", back_populates="branch", cascade="all, delete-orphan", lazy="joined")
    # relationship -> BranchImages
    branch_images = relationship("BranchImages", back_populates="branch", cascade="all, delete-orphan", lazy="joined")
    # relationship ->branch_manager
    branch_manager = relationship("BranchManager", lazy="joined")
    # relationship -> Teacher
    teacher = relationship("Teacher", back_populates="branch", cascade="all, delete-orphan", lazy="joined")
    #relationship -> Officer
    officer = relationship("Officer", back_populates="branch", cascade="all, delete-orphan", lazy="joined")
    #relationship -> ClassBranch
    class_branch = relationship("ClassBranch", back_populates="branch", cascade="all, delete-orphan", lazy="joined")

class BranchHalls(Base):
    __tablename__ = "branch_halls"

    row_id = Column(Integer, autoincrement=True, primary_key=True)
    hall_name = Column(String(10), nullable=False, index=True)
    branch_id = Column(String(8), ForeignKey('branch.branch_id'), index=True)

    # relationship -> Branch
    branch = relationship("Branch", back_populates="branch_halls", lazy="joined")

class BranchImages(Base):
    __tablename__ = "branch_images"

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(Text, nullable=False)
    branch_id = Column(String(8), ForeignKey("branch.branch_id"), index=True)

    # relationship -> Branch
    branch = relationship("Branch", back_populates="branch_images", lazy="joined")

class Student(Base):
    __tablename__ = 'student'

    student_id = Column(String(15), primary_key=True, index=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(80),nullable=False)
    firstname = Column(String(15), nullable=False)
    lastname = Column(String(15), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    address = Column(JSON, nullable=False)
    gender = Column(Boolean, nullable=False)
    admission_free_is_paid = Column(Boolean, nullable=False)
    mother_tung = Column(String(10))
    NIC = Column(String(14))
    school = Column(String(50))
    mobile = Column(Integer,unique=True)
    education_level_id = Column(String(36), ForeignKey('education_level.education_level_id'),index=True)
    branch_id = Column(String(8), ForeignKey('branch.branch_id'),index=True)
    created = Column(DateTime, nullable=False, index=True, default= lambda : get_sl_DateTime())
    active = Column(Boolean, nullable=False, default=True)
    # relationship -> Branch
    branch = relationship("Branch", lazy="joined")

    # relationship -> StudentParents, StudentSiblings, ProfileImagesStudent, CertificateImageStudent
    student_parents = relationship("StudentParents", back_populates="student", cascade="all, delete-orphan", lazy='joined')
    student_siblings = relationship("StudentSiblings", back_populates="student", cascade="all, delete-orphan", lazy="joined")
    student_profile_image = relationship("ProfileImagesStudent", back_populates="student", cascade="all, delete-orphan", lazy="joined")
    student_certificate_images = relationship("CertificateImagesStudent", back_populates="student", cascade="all, delete-orphan", lazy="joined")



    # delete-orphan delete child records if they are removed from parents

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

    # relationships
    student = relationship("Student", back_populates="student_parents")


class StudentSiblings(Base):
    __tablename__ = "student_siblings"

    row_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    name = Column(String(40), nullable=False)
    DOB = Column(Date)
    gender = Column(Boolean, nullable=False)  # male -> true | female -> false
    mobile = Column(Integer)

    # relationships
    student = relationship("Student", back_populates="student_siblings")

class ProfileImagesStudent(Base):
    __tablename__ = "profile_images"

    profile_image_id = Column(Integer, nullable=False, index=True, primary_key=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    profile_image_url = Column(Text, nullable=False)

    # relationships
    student = relationship("Student", back_populates="student_profile_image")


class CertificateImagesStudent(Base):
    __tablename__ = "certificate_images_student"

    certificate_image_id = Column(Integer, nullable=False, index=True, primary_key=True, autoincrement=True)
    student_id = Column(String(15), ForeignKey("student.student_id", ondelete="CASCADE"), index=True)
    certificate_image_url = Column(Text, nullable=False)

    # relationships
    student = relationship("Student", back_populates="student_certificate_images")


class Teacher(Base):
    __tablename__ = "teacher"

    teacher_id = Column(String(36), primary_key=True, index=True)
    teacher_username = Column(String(20),nullable=False,unique=True,index=True)
    teacher_password = Column(String(80),nullable=False)
    teacher_firstname = Column(String(15), index=True, nullable=False)
    teacher_lastname = Column(String(15), index=True, nullable=False)
    teacher_email = Column(String(40), index=True, nullable=False)
    teacher_mobile = Column(Integer, nullable=False, index=True)
    subject = Column(String(15), nullable=False, index=True)
    branch_id = Column(String(8), ForeignKey("branch.branch_id"))
    education_level_id = Column(String(36), ForeignKey("education_level.education_level_id"), index=True)
    password = Column(String(100))
    teacher_address = Column(JSON)
    province = Column(String(10))
    district = Column(String(10))
    home_town = Column(String(10))
    teacher_gender = Column(Boolean)
    teacher_NIC = Column(String(15))
    teacher_school = Column(String(50))
    teacher_description = Column(Text)
    teacher_active = Column(Boolean, default=True)
    created = Column(DateTime, default= lambda : get_sl_DateTime())

    # relationship -> TeacherCertificateImages
    teacher_certificate_images = relationship("TeacherCertificateImages", back_populates="teacher", cascade="all, delete-orphan", lazy="joined")
    # relationship -> Branch
    branch = relationship("Branch", back_populates="teacher")
    # relationship -> classes
    classes = relationship("Classes", back_populates="teacher", cascade="all, delete-orphan", lazy="joined")

class TeacherCertificateImages(Base):
    __tablename__ = "teacher_certificate_images"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(String(36), ForeignKey("teacher.teacher_id"),index=True, nullable=False)
    image_url = Column(Text, nullable=False)

    # relationship -> Teacher
    teacher = relationship("Teacher", back_populates="teacher_certificate_images", lazy="joined")

class Officer(Base):
    __tablename__ = "officer"

    officer_id = Column(String(15), primary_key=True, index=True)
    officer_username = Column(String(20), index=True, nullable=False, unique=True)
    officer_firstname = Column(String(15), index=True, nullable=False)
    officer_lastname = Column(String(15), index=True, nullable=False)
    password = Column(String(100))
    officer_address = Column(JSON)
    province = Column(String(10))
    district = Column(String(10))
    home_town = Column(String(10))
    officer_email = Column(String(40),index=True, nullable=False, unique=True)
    officer_gender = Column(Boolean)
    officer_mobile = Column(Integer, nullable=False, unique=True)
    branch_id = Column(String(8), ForeignKey("branch.branch_id"))
    officer_NIC = Column(String(15))
    officer_school = Column(Text)
    education_level_id = Column(String(36), ForeignKey("education_level.education_level_id"), index=True)
    officer_active = Column(Boolean, default=True)
    created = Column(DateTime, default=lambda: get_sl_DateTime())

    # relationship -> OfficerCertificateImages
    officer_certificate_images = relationship("OfficerCertificateImages", back_populates="officer", cascade="all, delete-orphan", lazy="joined")
    # relationship -> Branch
    branch = relationship("Branch", back_populates="officer", lazy="joined")

class OfficerCertificateImages(Base):
    __tablename__ = "officer_certificate_images"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    officer_id = Column(String(15), ForeignKey("officer.officer_id"), nullable=False, index=True)
    image_url = Column(Text, nullable=False)

    # relationship -> Officer
    officer = relationship("Officer", back_populates="officer_certificate_images", lazy="joined")

class ClassType(Base):
    __tablename__ = "class_type"
    class_type_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    class_type = Column(String(15), unique=True, nullable=False)

    # relationship -> Classes
    classes = relationship("Classes", back_populates="class_type", cascade="all, delete-orphan", lazy="joined")
    # relationship -> ClassFees
    class_fees = relationship("ClassFees", back_populates="class_type", cascade="all, delete-orphan", lazy="joined")

class Classes(Base):
    __tablename__ = "classes"

    class_id = Column(String(36), primary_key=True, index=True)
    class_name = Column(String(25), nullable=False, unique=True, index=True)
    teacher_id = Column(String(36), ForeignKey("teacher.teacher_id"))
    education_level_id = Column(String(36), ForeignKey("education_level.education_level_id"), index=True)
    class_type_id = Column(Integer, ForeignKey("class_type.class_type_id"), index=True)
    about = Column(Text)
    class_active = Column(Boolean, default=True)
    created = Column(DateTime, default=lambda: get_sl_DateTime())

    # relationship -> ClassFees
    class_fees = relationship("ClassFees", back_populates="classes", cascade="all, delete-orphan", lazy="joined")
    # relationship -> ClassType
    class_type = relationship("ClassType", back_populates="classes", lazy="joined")
    # relationship -> ClassImages
    class_images = relationship("ClassImages", back_populates="classes", cascade="all, delete-orphan", lazy="joined")
    # relationship -> ClassBranch
    class_branch = relationship("ClassBranch",back_populates="classes", cascade="all, delete-orphan", lazy="joined")
    # relationship -> Teacher
    teacher = relationship("Teacher", back_populates="classes", lazy="joined")

class ClassFees(Base):
    __tablename__ = "class_fees"

    class_id = Column(String(36), ForeignKey("classes.class_id"))
    class_type_id = Column(Integer, ForeignKey("class_type.class_type_id"))
    class_fee = Column(Float,nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("class_id", "class_type_id"),
    )

    # relationship -> classes
    classes = relationship("Classes", back_populates="class_fees", lazy="joined")
    # relationship -> class_type
    class_type = relationship("ClassType", back_populates="class_fees", lazy="joined")

class ClassImages(Base):
    __tablename__ = "class_images"

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(String(36), ForeignKey("classes.class_id"), index=True)
    url = Column(Text, nullable=False)

    # relationship -> classes
    classes = relationship("Classes", back_populates="class_images", lazy="joined")

class ClassBranch(Base):
    __tablename__ = "class_branch"

    class_id = Column(String(36), ForeignKey("classes.class_id"))
    branch_id = Column(String(8), ForeignKey("branch.branch_id"))

    # add composite primary key -> class_id, branch_id
    __table_args__ = (
        PrimaryKeyConstraint("class_id", "branch_id"),
    )

    # relationship -> Classes
    classes = relationship("Classes", back_populates="class_branch", lazy="joined")
    branch = relationship("Branch" , back_populates="class_branch", lazy="joined")



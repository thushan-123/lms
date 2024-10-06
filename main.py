from fastapi import FastAPI
from Databases.database import engine
from Databases import models
from starlette.middleware.cors import CORSMiddleware
from Routes.UsersAuthentication.Admin import admin
from Loggers.log import err_log, app_log
from Routes.StudentManagement import manageStudent
from Routes.BranchManagement import manageBranch
from Routes.ManagerManagement import manageManager


app = FastAPI()

# Create the database tables
try:
    models.Base.metadata.create_all(bind=engine)
    app_log.info("Database tables create successfully")
except Exception as e:
    err_log.error(f"Database tables create fail {e}")


origins = ["http://localhost", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router, prefix="/api/v1/auth/admin")
app.include_router(manageStudent.router, prefix="/api/v1/manageStudent")
app.include_router(manageBranch.router, prefix="/api/v1/manageBranch")
app.include_router(manageManager.router, prefix="/api/v1/manageManager")
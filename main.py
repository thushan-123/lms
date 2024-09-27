from fastapi import FastAPI
from Databases.database import engine
from Databases import models
from starlette.middleware.cors import CORSMiddleware
from Routes.Admin import admin


app = FastAPI()

# Create the database tables
try:
    models.Base.metadata.create_all(bind=engine)
except:
    pass

origins = ["http://localhost", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router, prefix="/api/v1/admin")
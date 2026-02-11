from fastapi import FastAPI
from .routers import users, auth, profile, jobs, applications
from .db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware


# Import models so tables are registered
from .models.user import User
from .models.profile import Profile
from .models.job import JobListing
from .models.application import CandidateApplication
from .models.interview import Interview

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(jobs.router)
app.include_router(applications.router)

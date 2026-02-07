from fastapi import FastAPI
from .routers import users, auth, profile
from .db.database import engine, Base

# Import models so tables are registered
from .models.user import User
from .models.profile import Profile
from .models.job import JobListing
from .models.application import CandidateApplication
from .models.interview import Interview

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)

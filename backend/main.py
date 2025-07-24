from fastapi import FastAPI
from app.api import endpoints
from app.database import init_db

app = FastAPI()
init_db()

# Include routes
app.include_router(endpoints.router)

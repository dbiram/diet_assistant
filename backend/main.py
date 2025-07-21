from fastapi import FastAPI
from app.api import endpoints

app = FastAPI()

# Include routes
app.include_router(endpoints.router)

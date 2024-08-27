# pylint: disable=missing-module-docstring
from fastapi import FastAPI
from routers import auth, user, company

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(company.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"

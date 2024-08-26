# pylint: disable=missing-module-docstring
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return "API service is up and running"

from fastapi import FastAPI
from routers.emails_router import emails_router


app = FastAPI()

app.include_router(emails_router, prefix="/api/email")

@app.get("/")
async def index():
    return "app running!"

from fastapi import FastAPI
from routers.files_router import files_router


app = FastAPI()

app.include_router(files_router, prefix="/api/files")

@app.get("/")
async def index():
    return "app running!"
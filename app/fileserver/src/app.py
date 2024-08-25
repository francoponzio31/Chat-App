from fastapi import FastAPI
from routers.files_router import files_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(files_router, prefix="/api/files")

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.get("/")
async def index():
    return "app running!"
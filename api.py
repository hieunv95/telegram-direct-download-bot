from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from io import BytesIO
import os

app = FastAPI()

# Temporary in-memory storage
file_store = {}

@app.post("/upload/{filename}")
async def upload_file(filename: str, file: UploadFile = File(...)):
    file_content = await file.read()
    file_store[filename] = file_content  # Store file content in-memory
    return {"message": "File uploaded successfully."}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_content = file_store.get(filename)
    if file_content:
        return FileResponse(BytesIO(file_content), filename=filename)
    return {"error": "File not found"}

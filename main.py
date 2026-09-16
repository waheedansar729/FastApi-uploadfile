from fastapi import FastAPI,File, UploadFile, Depends, HTTPException, status
import os
from fastapi.staticfiles import StaticFiles
import shutil




app = FastAPI()


UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
# step 1: Mount the uploads directory to serve static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# step 2: Create an endpoint to handle file uploads
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {
            "message": "File uploaded successfully",
            "filename": filename,
            "file_url": f"http://127.0.0.1:8000/uploads/{filename}"
        }

@app.get("/files")
def get_files(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return {
        "filename": filename,
        "file_url": f"http://127.0.0.1:8000/uploads/{filename}"
    }

@app.get("/")
def home():
    return {"message": "Welcome to the File Upload API"}
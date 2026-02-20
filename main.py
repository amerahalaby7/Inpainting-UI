import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Dict , List
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fake DB
# {id: {"filename": "...", "colored": False}}
db: Dict[int, dict] = {}

# ---------------- UPLOAD IMAGE ----------------
@app.post("/upload/{image_id}")
def upload_image(image_id: int, file: UploadFile = File(...)):
    if image_id in db:
        raise HTTPException(status_code=400, detail="Image ID already exists")

    file_path = os.path.join(UPLOAD_FOLDER, f'{image_id}.{file.filename.split(".")[-1]}')
    print(f"Saving uploaded file to: {file_path}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db[image_id] = {
        "filename": f'{image_id}.{file.filename.split(".")[-1]}',
        "colored": False
    }
    # print(f"Uploaded {file} as ID {image_id}")
    return {"message": "Image uploaded successfully"}
# @app.post("/updated/{image_id}")
# def update_image(image_id: int,file: UploadFile = File(...), coordinates: List = None):
#     if image_id not in db:
#         raise HTTPException(status_code=404, detail="Not found")

#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     db[image_id]["filename"] = file.filename

#     return {"message": "Image updated"}

# ---------------- GET ALL IMAGES ----------------
@app.get("/images")
def get_images():
    print(f"Current DB state: {db}")
    return db


# ---------------- GET SINGLE IMAGE FILE ----------------
@app.get("/image/{image_id}")
def get_image(image_id: int):
    if image_id not in db:
        raise HTTPException(status_code=404, detail="Not found")

    file_path = os.path.join(UPLOAD_FOLDER, db[image_id]["filename"])
    # print(FileResponse(file_path))
    return FileResponse(file_path)


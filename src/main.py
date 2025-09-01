from fastapi import FastAPI, UploadFile, File, Form
from src.faces import register_face, recognize_faces, list_faces
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Facial Recognition Service is running."}

@app.post("/register")
async def register(name: str = Form(...), file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    result = register_face(name, temp_path)
    os.remove(temp_path)
    return result

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    names = recognize_faces(temp_path)
    os.remove(temp_path)
    return {"recognized": names}

@app.get("/faces")
def faces():
    return {"faces": list_faces()}

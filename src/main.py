from fastapi import FastAPI, UploadFile, File, Form
from faces import register_face, recognize_faces, list_faces
import os

app = FastAPI(
    title="Sightline - Facial Recognition API",
    description="A powerful facial recognition service using DeepFace and OpenCV. Register faces and recognize them in images.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    return {
        "message": "Sightline Facial Recognition Service is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /register - Register a new face",
            "recognize": "POST /recognize - Recognize faces in an image", 
            "faces": "GET /faces - List all registered faces",
            "health": "GET /healthz - Health check"
        }
    }

@app.get("/healthz")
def health_check():
    return {"status": "healthy", "service": "sightline-facial-recognition", "version": "1.0.0"}

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
    result = recognize_faces(temp_path)
    os.remove(temp_path)
    return result

@app.get("/faces")
def faces():
    return list_faces()

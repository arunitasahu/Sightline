import os
import gc
import logging
from fastapi import FastAPI, UploadFile, File, Form
from .faces import register_face, recognize_faces, list_faces

# Configure logging for memory tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import memory monitoring
try:
    import psutil
    MEMORY_MONITORING = True
    
    def get_memory_usage():
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return round(process.memory_info().rss / 1024 / 1024, 2)
        
    def log_memory_usage(endpoint: str):
        """Log memory usage for debugging"""
        memory_mb = get_memory_usage()
        logger.info(f"Memory usage after {endpoint}: {memory_mb} MB")
        return memory_mb
        
except ImportError:
    MEMORY_MONITORING = False
    logger.warning("psutil not available - memory monitoring disabled")
    
    def get_memory_usage():
        return 0
        
    def log_memory_usage(endpoint: str):
        return 0

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
    memory_mb = get_memory_usage()
    return {
        "status": "healthy", 
        "service": "sightline-facial-recognition", 
        "version": "1.0.0",
        "memory_usage_mb": memory_mb,
        "memory_monitoring": MEMORY_MONITORING
    }

@app.post("/register")
async def register(name: str = Form(...), file: UploadFile = File(...)):
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        result = register_face(name, temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Force garbage collection to free memory
        gc.collect()
        log_memory_usage("register")
        
        return result
    except Exception as e:
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        logger.error(f"Registration error: {str(e)}")
        raise e

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        result = recognize_faces(temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Force garbage collection to free memory
        gc.collect()
        log_memory_usage("recognize")
        
        return result
    except Exception as e:
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        logger.error(f"Recognition error: {str(e)}")
        raise e

@app.get("/memory")
def memory_status():
    """Get detailed memory information for debugging"""
    if not MEMORY_MONITORING:
        return {"error": "Memory monitoring not available"}
    
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "memory_usage_mb": round(memory_info.rss / 1024 / 1024, 2),
            "virtual_memory_mb": round(memory_info.vms / 1024 / 1024, 2),
            "memory_percent": round(process.memory_percent(), 2),
            "available_memory_mb": round(psutil.virtual_memory().available / 1024 / 1024, 2),
            "total_memory_mb": round(psutil.virtual_memory().total / 1024 / 1024, 2)
        }
    except Exception as e:
        return {"error": f"Failed to get memory info: {str(e)}"}

@app.get("/faces")
def faces():
    try:
        result = list_faces()
        log_memory_usage("faces")
        return result
    except Exception as e:
        logger.error(f"List faces error: {str(e)}")
        return {"total_faces": 0, "registered_faces": [], "error": str(e)}

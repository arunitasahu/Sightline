import os
import tempfile

# Lazy imports to reduce memory usage
_cv2 = None
_np = None
_DeepFace = None

def get_cv2():
    global _cv2
    if _cv2 is None:
        import cv2
        _cv2 = cv2
    return _cv2

def get_np():
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np

def get_deepface():
    global _DeepFace
    if _DeepFace is None:
        # Configure TensorFlow for low memory usage
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF logging
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN optimizations
        
        try:
            import tensorflow as tf
            # Configure TensorFlow for memory efficiency
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                try:
                    for gpu in gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                except RuntimeError as e:
                    print(f"GPU configuration error: {e}")
            
            # Limit TensorFlow to use less memory
            tf.config.threading.set_inter_op_parallelism_threads(1)
            tf.config.threading.set_intra_op_parallelism_threads(1)
        except Exception as e:
            print(f"TensorFlow configuration warning: {e}")
        
        from deepface import DeepFace
        _DeepFace = DeepFace
    return _DeepFace

from db import init_db, add_face, get_all_faces, get_all_face_data

# Initialize the database
init_db()

# Register a new face
def register_face(name: str, image_path: str):
    cv2 = get_cv2()
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError('Image not found or unreadable')
    
    # Convert image to bytes for storage
    _, buffer = cv2.imencode('.jpg', img)
    image_data = buffer.tobytes()
    
    # Store in database
    add_face(name, image_data, 'jpg')
    
    return {"name": name, "status": "registered", "message": f"Face for {name} registered successfully"}

# Recognize faces in an image
def recognize_faces(image_path: str):
    try:
        cv2 = get_cv2()
        np = get_np()
        DeepFace = get_deepface()
        
        # Read the input image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError('Image not found or unreadable')
        
        results = []
        
        # Get registered faces with error handling
        try:
            registered_faces = get_all_face_data()
        except Exception as e:
            print(f"Error accessing database: {str(e)}")
            return {"message": "Database error", "matches": []}
        
        if not registered_faces:
            return {"message": "No faces registered yet", "matches": []}
        
        temp_files = []  # Track temp files for cleanup
        
        try:
            for name, face_data, face_format in registered_faces:
                temp_stored_path = None
                try:
                    # Convert stored image data back to image
                    nparr = np.frombuffer(face_data, np.uint8)
                    stored_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if stored_img is None:
                        print(f"Failed to decode image for {name}")
                        continue
                    
                    # Create temporary file for DeepFace verification
                    temp_stored = tempfile.NamedTemporaryFile(suffix=f'.{face_format}', delete=False)
                    temp_stored_path = temp_stored.name
                    temp_stored.close()
                    temp_files.append(temp_stored_path)
                    
                    # Write image to temp file
                    if not cv2.imwrite(temp_stored_path, stored_img):
                        print(f"Failed to write temp file for {name}")
                        continue
                    
                    # Verify faces with timeout protection
                    verification = DeepFace.verify(
                        img1_path=temp_stored_path, 
                        img2_path=image_path, 
                        enforce_detection=False,
                        model_name='Facenet',  # Use lighter model
                        detector_backend='opencv'  # Use OpenCV detector for efficiency
                    )
                    
                    if verification.get('verified', False):
                        distance = verification.get('distance', 1.0)
                        confidence = max(0, round(1 - distance, 3)) if distance < 1 else 0.1
                        results.append({
                            "name": name,
                            "confidence": confidence
                        })
                        
                except Exception as e:
                    print(f"Error processing face {name}: {str(e)}")
                    continue
        
        finally:
            # Clean up all temporary files
            for temp_path in temp_files:
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except Exception as e:
                    print(f"Error cleaning up temp file {temp_path}: {str(e)}")
        
        if results:
            # Sort by confidence (highest first)
            results.sort(key=lambda x: x['confidence'], reverse=True)
            return {"message": f"Found {len(results)} matching face(s)", "matches": results}
        else:
            return {"message": "No matching faces found", "matches": []}
            
    except Exception as e:
        print(f"Critical error in recognize_faces: {str(e)}")
        return {"message": "Recognition failed", "matches": [], "error": str(e)}

# List all registered faces
def list_faces():
    faces = get_all_faces()
    return {
        "total_faces": len(faces),
        "registered_faces": faces
    }

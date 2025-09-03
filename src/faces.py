import os
import cv2
import numpy as np
import tempfile
from deepface import DeepFace
from db import init_db, add_face, get_all_faces, get_all_face_data

# Initialize the database
init_db()

# Register a new face
def register_face(name: str, image_path: str):
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
                        enforce_detection=False
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

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
    # Read the input image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError('Image not found or unreadable')
    
    results = []
    registered_faces = get_all_face_data()
    
    if not registered_faces:
        return {"message": "No faces registered yet", "matches": []}
    
    for name, face_data, face_format in registered_faces:
        try:
            # Convert stored image data back to image
            nparr = np.frombuffer(face_data, np.uint8)
            stored_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Create temporary files for DeepFace verification
            with tempfile.NamedTemporaryFile(suffix=f'.{face_format}', delete=False) as temp_stored:
                cv2.imwrite(temp_stored.name, stored_img)
                temp_stored_path = temp_stored.name
            
            try:
                # Verify faces
                verification = DeepFace.verify(
                    img1_path=temp_stored_path, 
                    img2_path=image_path, 
                    enforce_detection=False
                )
                
                if verification['verified']:
                    confidence = verification.get('distance', 0)
                    results.append({
                        "name": name,
                        "confidence": round(1 - confidence, 3) if confidence < 1 else 0.5
                    })
            finally:
                # Clean up temporary file
                if os.path.exists(temp_stored_path):
                    os.unlink(temp_stored_path)
                    
        except Exception as e:
            print(f"Error processing face {name}: {str(e)}")
            continue
    
    if results:
        # Sort by confidence (highest first)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return {"message": f"Found {len(results)} matching face(s)", "matches": results}
    else:
        return {"message": "No matching faces found", "matches": []}

# List all registered faces
def list_faces():
    faces = get_all_faces()
    return {
        "total_faces": len(faces),
        "registered_faces": faces
    }

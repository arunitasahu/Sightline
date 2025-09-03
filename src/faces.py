import os
import tempfile
import pickle
import base64

# Lazy imports to reduce memory usage
_cv2 = None
_np = None
_face_recognition = None

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

def get_face_recognition():
    global _face_recognition
    if _face_recognition is None:
        import face_recognition
        _face_recognition = face_recognition
    return _face_recognition

from db import init_db, add_face, get_all_faces, get_all_face_data

# Initialize the database
init_db()

# Register a new face
def register_face(name: str, image_path: str):
    try:
        face_recognition = get_face_recognition()
        
        # Load image and find face encodings
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            raise ValueError('No face found in the image')
        
        if len(face_encodings) > 1:
            raise ValueError('Multiple faces found in image. Please use an image with only one face.')
        
        # Get the first (and only) face encoding
        face_encoding = face_encodings[0]
        
        # Serialize the face encoding for storage
        encoding_data = pickle.dumps(face_encoding)
        
        # Store in database
        add_face(name, encoding_data, 'encoding')
        
        return {"name": name, "status": "registered", "message": f"Face for {name} registered successfully"}
    
    except Exception as e:
        return {"name": name, "status": "error", "message": f"Registration failed: {str(e)}"}

# Recognize faces in an image
def recognize_faces(image_path: str):
    try:
        face_recognition = get_face_recognition()
        np = get_np()
        
        # Load the input image and find face encodings
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            return {"message": "No faces found in the image", "matches": []}
        
        # Get registered faces with error handling
        try:
            registered_faces = get_all_face_data()
        except Exception as e:
            print(f"Error accessing database: {str(e)}")
            return {"message": "Database error", "matches": []}
        
        if not registered_faces:
            return {"message": "No faces registered yet", "matches": []}
        
        results = []
        
        # For each face found in the input image
        for face_encoding in face_encodings:
            best_match_name = None
            best_distance = float('inf')
            
            # Compare with all registered faces
            for name, encoding_data, format_type in registered_faces:
                if format_type != 'encoding':
                    continue  # Skip non-encoding data
                
                try:
                    # Deserialize the stored face encoding
                    stored_encoding = pickle.loads(encoding_data)
                    
                    # Calculate face distance (lower is better)
                    distances = face_recognition.face_distance([stored_encoding], face_encoding)
                    distance = distances[0]
                    
                    # If this is the best match so far and below threshold
                    if distance < best_distance and distance < 0.6:  # 0.6 is a good threshold
                        best_distance = distance
                        best_match_name = name
                
                except Exception as e:
                    print(f"Error processing stored face {name}: {str(e)}")
                    continue
            
            # If we found a good match
            if best_match_name:
                confidence = max(0, round(1 - best_distance, 3))
                results.append({
                    "name": best_match_name,
                    "confidence": confidence
                })
        
        if results:
            # Sort by confidence (highest first) and remove duplicates
            unique_results = {}
            for result in results:
                name = result["name"]
                if name not in unique_results or result["confidence"] > unique_results[name]["confidence"]:
                    unique_results[name] = result
            
            final_results = list(unique_results.values())
            final_results.sort(key=lambda x: x['confidence'], reverse=True)
            return {"message": f"Found {len(final_results)} matching face(s)", "matches": final_results}
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

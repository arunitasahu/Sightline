import os
import cv2
import numpy as np
from PIL import Image
import base64
import hashlib
from .db import init_db, add_face, get_all_faces, get_all_face_data

# Initialize the database
init_db()

def extract_face_features(image_path):
    """Extract simple face features using OpenCV Haar cascades"""
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError('Image not found or unreadable')
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            raise ValueError('No face found in the image')
        
        if len(faces) > 1:
            raise ValueError('Multiple faces found. Please use an image with only one face.')
        
        # Get the first (and only) face
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize face to standard size for comparison
        face_resized = cv2.resize(face_roi, (100, 100))
        
        # Calculate histogram as simple feature
        hist = cv2.calcHist([face_resized], [0], None, [256], [0, 256])
        
        # Normalize histogram
        hist = cv2.normalize(hist, hist).flatten()
        
        return {
            'face_region': face_resized,
            'histogram': hist,
            'face_box': (x, y, w, h)
        }
        
    except Exception as e:
        raise ValueError(f"Face extraction failed: {str(e)}")

def compare_faces(features1, features2):
    """Compare two face feature sets and return similarity score"""
    try:
        # Compare histograms using correlation
        hist_corr = cv2.compareHist(features1['histogram'], features2['histogram'], cv2.HISTCMP_CORREL)
        
        # Compare face regions using template matching
        face1 = features1['face_region']
        face2 = features2['face_region']
        
        # Ensure same size
        if face1.shape != face2.shape:
            face2 = cv2.resize(face2, (face1.shape[1], face1.shape[0]))
        
        # Calculate structural similarity
        diff = cv2.absdiff(face1, face2)
        structural_sim = 1.0 - (np.mean(diff) / 255.0)
        
        # Combine scores
        similarity = (hist_corr * 0.6) + (structural_sim * 0.4)
        return max(0, min(1, similarity))
        
    except Exception as e:
        print(f"Face comparison error: {str(e)}")
        return 0.0

# Register a new face
def register_face(name: str, image_path: str):
    try:
        # Extract face features
        features = extract_face_features(image_path)
        
        # Serialize features for storage
        face_data = {
            'face_region': features['face_region'].tolist(),
            'histogram': features['histogram'].tolist(),
            'face_box': features['face_box']
        }
        
        # Convert to bytes for database storage
        import json
        feature_bytes = json.dumps(face_data).encode('utf-8')
        
        # Store in database
        add_face(name, feature_bytes, 'features')
        
        return {"name": name, "status": "registered", "message": f"Face for {name} registered successfully"}
    
    except Exception as e:
        return {"name": name, "status": "error", "message": f"Registration failed: {str(e)}"}

# Recognize faces in an image
def recognize_faces(image_path: str):
    try:
        # Extract features from input image
        input_features = extract_face_features(image_path)
        
        # Get registered faces
        try:
            registered_faces = get_all_face_data()
        except Exception as e:
            print(f"Error accessing database: {str(e)}")
            return {"message": "Database error", "matches": []}
        
        if not registered_faces:
            return {"message": "No faces registered yet", "matches": []}
        
        results = []
        
        # Compare with all registered faces
        for name, feature_data, format_type in registered_faces:
            if format_type != 'features':
                continue  # Skip non-feature data
            
            try:
                # Deserialize stored features
                import json
                stored_data = json.loads(feature_data.decode('utf-8'))
                
                # Reconstruct features
                stored_features = {
                    'face_region': np.array(stored_data['face_region'], dtype=np.uint8),
                    'histogram': np.array(stored_data['histogram'], dtype=np.float32),
                    'face_box': stored_data['face_box']
                }
                
                # Compare faces
                similarity = compare_faces(input_features, stored_features)
                
                # If similarity is above threshold
                if similarity > 0.6:  # Threshold for match
                    confidence = round(similarity, 3)
                    results.append({
                        "name": name,
                        "confidence": confidence
                    })
                
            except Exception as e:
                print(f"Error processing stored face {name}: {str(e)}")
                continue
        
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

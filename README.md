# Sightline - Facial Recognition Service

A powerful, cloud-deployed FastAPI microservice for facial recognition using DeepFace and OpenCV. **Now live and ready to use!**

🌐 **[Try the Live API](https://sightline-4s51.onrender.com/docs)** | 🔗 **[GitHub Repository](https://github.com/arunitasahu/Sightline)**

---

## 🌟 Features
- 🚀 **Live and deployed** at [sightline-4s51.onrender.com](https://sightline-4s51.onrender.com/docs)
- 📝 Register new faces with images and names
- 🔍 Recognize faces in uploaded images  
- 📋 List all registered faces
- 💾 Persistent storage with SQLite
- 🧠 DeepFace-powered recognition (supports multiple models)
- 📚 Interactive API docs (Swagger UI)
- 🐳 Dockerized for easy local development
- ☁️ Free cloud hosting on Render

---

## 🛠️ Tech Stack
- Python 3.11
- FastAPI
- DeepFace
- OpenCV
- TensorFlow 2.13.0
- SQLite
- Docker
- Deployed on Render

---

## 📦 Project Structure
```
facial-service/
├── src/
│   ├── main.py              # FastAPI app and endpoints
│   ├── faces.py             # Core facial recognition logic
│   ├── db.py                # SQLite database integration
├── data/                    # Stores face images and database
├── app.py                   # Render deployment entry point
├── requirements.txt         # Python dependencies
├── Dockerfile.local         # Local container build instructions
├── docker-compose.local.yml # Local development with Docker
└── README.md                # Project documentation
```

---

## 🚀 Quick Start (Local Development)

### 1. Clone the repository
```sh
git clone https://github.com/arunitasahu/Sightline.git
cd Sightline
```

### 2. Build and run with Docker Compose
```sh
docker compose -f docker-compose.local.yml up --build
```

### 3. Access the API
- Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

### 4. API Endpoints
- 📝 `POST /register` — Register a new face (upload image + name)
- 🔍 `POST /recognize` — Recognize faces in an uploaded image
- 📋 `GET /faces` — List all registered faces
- ❤️ `GET /healthz` — Health check endpoint

---

## 🌐 **Live Demo - Try It Now!**

### **� Interactive API**: [https://sightline-4s51.onrender.com/docs](https://sightline-4s51.onrender.com/docs)

**Quick Start Guide:**
1. 📝 **Register a Face**: Upload an image with a name using `POST /register`
2. 🔍 **Recognize Faces**: Upload an image to identify faces using `POST /recognize` 
3. 📋 **List All Faces**: View registered faces using `GET /faces`
4. ❤️ **Health Check**: `GET /healthz` to verify service status

> **Note**: First request after inactivity may take 50+ seconds (free tier limitation)

---

## 💡 API Endpoints

### 📝 Register a Face
- **Endpoint**: `POST /register`
- **Usage**: Go to [/docs](https://sightline-4s51.onrender.com/docs), upload an image and enter a name

### 🔍 Recognize a Face
- **Endpoint**: `POST /recognize` 
- **Usage**: Upload an image to identify registered faces

### 📋 List Faces
- **Endpoint**: `GET /faces`
- **Usage**: View all registered face names

### ❤️ Health Check
- **Endpoint**: `GET /healthz`
- **Usage**: Verify service is running

---

---

## 🌍 Cloud Deployment (Done! ✅)

### ✅ **Already Deployed on Render**
**Live API**: [https://sightline-4s51.onrender.com/docs](https://sightline-4s51.onrender.com/docs)

---

---

## 🎯 **Live Service Links**

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **API Documentation** | [sightline-4s51.onrender.com/docs](https://sightline-4s51.onrender.com/docs) | Interactive Swagger UI |
| ❤️ **Health Check** | [sightline-4s51.onrender.com/healthz](https://sightline-4s51.onrender.com/healthz) | Service status |
| 📊 **Root Endpoint** | [sightline-4s51.onrender.com](https://sightline-4s51.onrender.com) | Basic info |
| 📋 **List Faces** | [sightline-4s51.onrender.com/faces](https://sightline-4s51.onrender.com/faces) | View registered faces |
| 📁 **GitHub Repository** | [github.com/arunitasahu/Sightline](https://github.com/arunitasahu/Sightline) | Source code |

---

## ⚡ **Performance & Limitations**

### **✅ What Works Great:**
- Face registration and recognition
- Multiple face detection models (VGGFace, FaceNet, etc.)
- SQLite persistent storage
- Real-time API responses (when active)
- Interactive documentation

---

## 🐳 Local Docker Development

To use Docker locally:
```bash
# Rename files back to use Docker locally
mv Dockerfile.local Dockerfile
mv docker-compose.local.yml docker-compose.yml
docker compose up --build
```

---

## 🧑‍💻 Contributing
Pull requests and suggestions are welcome!

---

## 📄 License
MIT

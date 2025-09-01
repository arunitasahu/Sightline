# Facial Recognition Service

A powerful, containerized FastAPI microservice for facial recognition using DeepFace and OpenCV. Easily deployable and ready for cloud or local use.

---

## 🌟 Features
- Register new faces with images and names
- Recognize faces in uploaded images
- List all registered faces
- Persistent storage with SQLite
- DeepFace-powered recognition (supports multiple models)
- Interactive API docs (Swagger UI)
- Dockerized for easy deployment

---

## 🛠️ Tech Stack
- Python 3.9
- FastAPI
- DeepFace
- OpenCV
- SQLite
- Docker

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
├── Dockerfile               # Container build instructions
├── docker-compose.local.yml # Local development with Docker
└── README.md                # Project documentation
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repository
```sh
git clone https://github.com/your-username/facial-service.git
cd facial-service
```

### 2. Build and run with Docker Compose
```sh
docker compose -f docker-compose.local.yml up --build
```

### 3. Access the API
- Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

### 4. Endpoints
- `POST /register` — Register a new face (upload image + name)
- `POST /recognize` — Recognize faces in an uploaded image
- `GET /faces` — List all registered faces

---

## 💡 Example API Usage

### Register a Face
- Go to `/docs`, use `POST /register`, upload an image and enter a name.

### Recognize a Face
- Go to `/docs`, use `POST /recognize`, upload an image to identify faces.

### List Faces
- Go to `/docs`, use `GET /faces` to see all registered names.

---

## 🌍 Free Cloud Deployment

### Deploy on Render (Recommended)
1. **Push your code to GitHub.**
2. **Sign up at [render.com](https://render.com) and create a new Web Service.**
3. **Connect your GitHub repo.**
4. **Set build/start commands:**
   - Build: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start: `gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. **Choose the free plan and deploy.**
6. **Access your API at `https://your-app.onrender.com/docs`**

---

## 📢 Try It Online
Once deployed, add your public API link here:
```
[Open Swagger UI](https://your-app.onrender.com/docs)
```

---

## 🧑‍💻 Contributing
Pull requests and suggestions are welcome!

---

## 📄 License
MIT

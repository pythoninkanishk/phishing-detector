from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from featureExtractor import PredictURL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import validators

# ------------------- 1️⃣ FASTAPI SETUP -------------------
app = FastAPI(
    title="Phishing Detection API",
    description="Detect if a URL is phishing or safe using ML model",
    version="1.0.0"
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- 2️⃣ MACHINE LEARNING MODEL -------------------
classification = PredictURL()

# ------------------- 3️⃣ SQLITE DATABASE SETUP -------------------
DATABASE_URL = "sqlite:///./phishing.db"  # Creates phishing.db in root folder

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table for storing scan history
class URLLog(Base):
    __tablename__ = "urllogs"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    result = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ------------------- 4️⃣ MAIN ENDPOINT: SCAN URL -------------------
@app.get("/api")
def scan_url(url: str = ""):
    # 🧠 Auto-clean the URL
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Auto-add https:// if missing
    if not url.endswith("/"):
        url += "/"  # Add trailing slash if missing

    # 🧪 Validate URL more gently
    if not validators.url(url):
        return {"msg": "Invalid URL. Make sure it starts with http:// or https://"}

    # 🧠 Predict using your ML model
    try:
        ans = classification.predict(url)
    except Exception as e:
        return {"msg": f"Prediction failed: {str(e)}"}

    # 💾 Save scan result in database
    try:
        db = SessionLocal()
        log = URLLog(url=url, result=ans)
        db.add(log)
        db.commit()
        db.refresh(log)
    except Exception as e:
        return {"msg": f"Database error: {str(e)}"}
    finally:
        db.close()

    return {"url": url, "result": ans}

# ------------------- 5️⃣ HISTORY ENDPOINT -------------------
@app.get("/history")
def get_history():
    db = SessionLocal()
    logs = db.query(URLLog).order_by(URLLog.timestamp.desc()).all()
    db.close()

    return [
        {
            "id": log.id,
            "url": log.url,
            "result": log.result,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for log in logs
    ]

# ------------------- 6️⃣ ROOT ENDPOINT -------------------
@app.get("/")
def home():
    return {
        "msg": "Welcome to the Phishing Detection API 🚀",
        "endpoints": {
            "Scan URL": "/api?url=https://example.com",
            "History": "/history",
            "Docs": "/docs",
        },
    }

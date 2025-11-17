from fastapi import FastAPI
from phishing_detector.phishing import router as phishing_router
from EDA.eda_router import router as eda_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 🧩 Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend domain here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 📦 Include routers
app.include_router(phishing_router)


# ✅ Make sure the EDA static directory matches what's used in eda_router.py
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_ROOT, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


app.include_router(eda_router)

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}
from fastapi import FastAPI
from phishing_detector.phishing import router as phishing_router
from EDA.eda_router import router as eda_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(phishing_router)
app.include_router(eda_router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}

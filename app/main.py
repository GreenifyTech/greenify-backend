from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import admin, ai_doctor, auth, bouquet, cart, categories, diagnosis, orders, products, profile, analytics, notifications
import app.models # Ensure models are loaded

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

@app.on_event("startup")
def startup_event():
    # Create tables on startup if they don't exist
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Greenify API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(bouquet.router)
app.include_router(ai_doctor.router)
app.include_router(profile.router)
app.include_router(diagnosis.router)
app.include_router(admin.router)
app.include_router(analytics.router)
app.include_router(notifications.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

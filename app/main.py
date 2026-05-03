import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import admin, ai_doctor, auth, bouquet, cart, categories, diagnosis, orders, products, profile, analytics, notifications, users
import app.models 


try:
    print("Base metadata tables:", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
except Exception as e:
    print("❌ Error creating tables:", e)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    # Disable CSRF protection
    csrf_protection=False,
    redirect_slashes=False,
)

# CORS configuration
allow_origins=[
    "https://greenify-frontend-five.vercel.app",
    "https://greenify-frontend.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Greenify API is running"}

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
app.include_router(users.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

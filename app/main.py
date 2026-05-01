import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import admin, ai_doctor, auth, bouquet, cart, categories, diagnosis, orders, products, profile, analytics, notifications
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
)

# CORS configuration
_extra_origins = os.getenv("CORS_ORIGINS", "")
_extra_list = [o.strip() for o in _extra_origins.split(",") if o.strip()]

origins: list[str] = list(
    dict.fromkeys(
        [
            settings.frontend_url,
            "https://greenify-frontend-five.vercel.app",
            "https://greenify-app.vercel.app",
            "http://localhost:5173",
            "http://localhost:3000",
        ]
        + _extra_list
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

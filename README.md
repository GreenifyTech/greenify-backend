# 🌱 Greenify Backend

A production-ready backend powering the **Greenify platform** — a smart ecosystem for plant care, customization, and e-commerce.

Built with **FastAPI** and designed with clean architecture principles, this backend delivers secure authentication, scalable APIs, and real-time business insights through an advanced admin dashboard.

---

## ✨ Key Features

🔐 **Authentication & Security**
- JWT-based authentication system
- Role-based access control (Admin / User)
- Secure credential validation

🛍 **Product Management**
- Full CRUD operations
- Structured product catalog
- Ready for media integration (images via cloud storage)

📦 **Order System**
- Create and manage orders
- User-specific order history
- Order status tracking (pending, shipped, delivered, etc.)

📊 **Admin Dashboard**
- Total orders & revenue tracking
- Order status analytics
- Top-selling products insights
- Recent orders monitoring

⚙️ **Clean Architecture**
- Separation of concerns (routers, services, models)
- Scalable and maintainable structure

---

## 🛠 Tech Stack

| Layer            | Technology |
|------------------|-----------|
| Backend Framework | FastAPI |
| Database         | MySQL |
| ORM              | SQLAlchemy |
| Authentication   | JWT |
| Validation       | Pydantic |
| Server           | Uvicorn |

---

## 📂 Project Structure

```bash
greenify-backend/
│
├── app/
│   ├── core/        # Config, security, dependencies
│   ├── models/      # Database models
│   ├── schemas/     # Pydantic schemas
│   ├── routers/     # API routes
│   ├── services/    # Business logic
│   └── main.py      # App entry point
│
├── create_tables.py
├── requirements.txt
└── .env
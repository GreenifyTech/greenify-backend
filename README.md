# 🌱 Greenify Backend

A production-ready backend powering the **Greenify platform** — a smart ecosystem for plant care, customization, and e-commerce.

Built with **FastAPI** and designed with clean architecture principles, this backend delivers secure authentication, scalable APIs, and real-time business insights through an advanced admin dashboard.

---

## ✨ Key Features

🔐 **Authentication & Security**

* JWT-based authentication system
* Role-based access control (Admin / User)
* Secure credential validation

🛍 **Product Management**

* Full CRUD operations
* Structured product catalog
* Ready for media integration (images via cloud storage)

📦 **Order System**

* Create and manage orders
* User-specific order history
* Order status tracking (pending, shipped, delivered, etc.)

📊 **Admin Dashboard**

* Total orders & revenue tracking
* Order status analytics
* Top-selling products insights
* Recent orders monitoring

⚙️ **Clean Architecture**

* Separation of concerns (routers, services, models)
* Scalable and maintainable structure

---

## 🛠 Tech Stack

| Layer             | Technology |
| ----------------- | ---------- |
| Backend Framework | FastAPI    |
| Database          | MySQL      |
| ORM               | SQLAlchemy |
| Authentication    | JWT        |
| Validation        | Pydantic   |
| Server            | Uvicorn    |

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
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/GreenifyTech/greenify-backend.git
cd greenify-backend
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

* Windows:

```bash
.venv\Scripts\activate
```

* macOS/Linux:

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create `.env` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=greenify_db
DB_USER=root
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

FRONTEND_URL=http://localhost:5173
```

---

### 5. Initialize Database

```bash
python create_tables.py
```

---

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

---

## 📚 API Documentation

Once running:

* Swagger UI 👉 http://localhost:8000/docs
* ReDoc 👉 http://localhost:8000/redoc

Interactive testing available directly from the browser.

---

## 🔗 Core API Endpoints

### 🔐 Authentication

* `POST /api/auth/register`
* `POST /api/auth/login`
* `POST /api/auth/token`

---

### 🛍 Products

* `GET /api/products`
* `GET /api/products/{product_id}`
* `POST /api/products` *(Admin only)*

---

### 📦 Orders

* `POST /api/orders`
* `GET /api/orders/me`
* Pagination & filtering supported

---

### 📊 Admin

* `GET /api/admin/dashboard`
* `GET /api/admin/stats`

---

## 🧠 System Highlights

* Optimized database queries using SQLAlchemy
* Pagination for scalable data handling
* Clean dependency injection using FastAPI Depends
* Structured response models for consistency
* Ready for frontend integration (React)

---

## 🔮 Future Roadmap

* 🔄 Redis caching for performance optimization
* 💳 Payment gateway integration (Stripe / Paymob)
* 🧪 Unit & integration testing (pytest)
* 🐳 Docker support for deployment
* ☁️ Cloud deployment (Railway / AWS)

---

## 👨‍💻 Author

**Khalid Samy**
Backend Developer | Digital Transformation Student

📧 [khalidsmhran@gmail.com](mailto:khalidsmhran@gmail.com)
📍 Giza, Egypt

---

## ⭐ Contribution

Feel free to fork, contribute, or suggest improvements.

If you like the project, don’t forget to ⭐ the repo!

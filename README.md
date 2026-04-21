# Greenify Backend

A robust and scalable backend for the Greenify platform, providing a seamless experience for plant enthusiasts. Built with FastAPI, SQLAlchemy, and MySQL, it offers secure user authentication, product catalog management, a comprehensive order system, and an advanced administrative dashboard.

## 🌟 Features

- **Secure Authentication**: JWT-based user login and registration system.
- **Product Management**: Complete CRUD operations for the product catalog.
- **Order System**: Seamless order creation, listing, and user-specific order history tracking.
- **Admin Dashboard**: Powerful analytics including total orders, revenue tracking, and top-selling products.
- **Role-Based Access Control (RBAC)**: Distinct permissions for standard users and administrators.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Language**: Python 3.8+

## 📂 Project Structure

```text
greenify-backend/
├── app/
│   ├── core/           # Configurations, security, and dependencies
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic models for validation & serialization
│   ├── routers/        # API endpoints and route definitions
│   └── services/       # Core business logic and database interactions
├── create_tables.py    # Script to initialize database tables
├── requirements.txt    # Python dependencies
└── .env                # Environment variables configuration
```

## 🚀 Installation & Setup

Follow these steps to set up the project locally.

### 1. Clone the repository
```bash
git clone https://github.com/GreenifyTech/greenify-backend.git
cd greenify-backend
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Ensure you have MySQL installed and running. Create a database for the project (e.g., `greenify_db`).

Initialize the tables:
```bash
python create_tables.py
```

## ⚙️ Environment Variables

Create a `.env` file in the root directory. You can use the `.env.example` file (if available) as a template.

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/greenify_db

# Security
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
- `DATABASE_URL`: Connection string for your MySQL database.
- `SECRET_KEY`: A secure random string used to sign JWT tokens.

## 🏃‍♂️ Running the Project

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## 📚 API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access:

- **Swagger UI**: Visit `http://localhost:8000/docs` for an interactive interface to test the endpoints directly from your browser.
- **ReDoc**: Visit `http://localhost:8000/redoc` for an alternative, structured view of the API documentation.

## 🔗 Example Endpoints

Here are some of the key endpoints available in the API:

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate and receive a JWT

### Products
- `GET /api/products` - Retrieve a list of all products
- `GET /api/products/{id}` - Get details of a specific product

### Orders
- `POST /api/orders` - Create a new order
- `GET /api/orders/me` - Retrieve the order history for the logged-in user

## 📊 Admin Dashboard

Administrators have access to specialized endpoints that provide insights into the platform's performance. The admin dashboard routes allow authorized users to fetch:
- **Total Orders**: The overall number of orders placed.
- **Revenue**: Calculation of total sales revenue.
- **Top Products**: Analysis of the highest-selling items across the platform.

*(Ensure you are logged in with an admin account to access these endpoints.)*

## 🔮 Future Improvements

- Implementation of a caching layer (e.g., Redis) for faster read operations.
- Integration of a payment gateway (e.g., Stripe) for real-time transaction processing.
- Addition of unit and integration tests using `pytest` to ensure continued reliability.
- Dockerization of the application for easier deployment and environment consistency.

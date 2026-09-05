<div align="center">

<img src="youtab/frontend/images/logo.png" alt="Youtab Logo" width="420"/>

from Persia to tomorrow

# YOUTAB

### Engineered for Speed.

**A full-stack automotive platform built around the Youtab automotive brand.**

<br>

![Status](https://img.shields.io/badge/status-under%20active%20development-orange?style=for-the-badge)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![Database](https://img.shields.io/badge/database-MySQL-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Frontend](https://img.shields.io/badge/frontend-HTML%20%2F%20CSS%20%2F%20JavaScript-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)

</div>

---

## 🚧 Project Status

> **Youtab is currently under active development.**

This project is an evolving automotive platform and is being continuously improved.

New features, UI improvements, backend capabilities, database enhancements, and additional vehicle models are planned for future releases.

Some parts of the project currently operate as **demonstration features** rather than production-ready services.

---

## 🏎️ About Youtab

**Youtab** is a fictional automotive brand and full-stack web application designed around a modern digital car-buying experience.

The project combines a visually focused automotive frontend with a **FastAPI-powered backend**, **MySQL database**, authentication, vehicle configuration, and order management.

The goal is to create a complete digital journey:

**Explore → Configure → Register → Order**

> *We don't build cars. We build the feeling of driving one.*

---

## ✨ Features

### 🚘 Vehicle Showcase

Explore the available Youtab lineup with detailed information about each vehicle, including:

* Vehicle name
* Vehicle category
* Description
* Base price
* Warranty information
* Available exterior colors
* Color-specific vehicle images

Current models include:

| Model              | Category     |
| ------------------ | ------------ |
| **Youtab Kourosh** | Muscle Coupe |
| **Youtab Ario**    | Sport Sedan  |

---

### 🎨 Car Configuration

Users can customize their selected vehicle by choosing from available colors.

Each color is connected to its corresponding vehicle image, creating a simple visual configuration experience.

---

### 👤 User Authentication

The backend provides a complete authentication flow including:

* User registration
* User login
* Password hashing
* JWT-based authentication
* Current-user endpoint
* Duplicate phone number prevention
* Duplicate national ID prevention
* Input validation

Passwords are never stored as plain text and are hashed using **bcrypt**.

---

### 🛒 Order Management

Authenticated users can create vehicle orders by providing:

* Vehicle model
* Selected color
* Delivery address

Users can also retrieve their own previous orders.

The current implementation includes a **demo payment flow**. No real payment is processed.

---

### 🗄️ Database

The application uses **MySQL** with **SQLAlchemy ORM**.

The current database structure includes:

```text
Users
  │
  └── Orders
        │
        └── Car Models
              │
              └── Car Colors
```

Main entities:

* `User`
* `CarModel`
* `CarColor`
* `Order`

---

## 🧰 Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Custom UI components
* Responsive automotive interface
* Custom fonts and visual assets

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* MySQL
* PyMySQL

### Authentication & Security

* JWT
* `python-jose`
* Passlib
* bcrypt
* Environment variables

---

## 📁 Project Structure

```text
Youtab/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── cars.py
│   │   │   └── orders.py
│   │   │
│   │   ├── database.py
│   │   ├── deps.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── seed_data.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │   ├── logo.png
│   │   ├── ario-*.png
│   │   ├── kourosh-*.png
│   │   └── ...
│   │
│   ├── icon/
│   ├── font/
│   ├── js/
│   │   └── script.js
│   │
│   └── index.html
│
└── README.md
```

---

## 🔌 API Overview

The backend exposes RESTful API endpoints under the `/api` prefix.

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Cars

```http
GET /api/cars
GET /api/cars/{car_key}
```

### Orders

```http
POST /api/orders
GET  /api/orders/me
```

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd Youtab
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend` directory:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=youtab_db

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

> **Never commit your `.env` file to GitHub.**

A `.gitignore` file is included in the project to prevent sensitive and environment-specific files from being tracked.

---

## 🗃️ Database Setup

Make sure your MySQL server is running and create the database:

```sql
CREATE DATABASE youtab_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then configure your database credentials in `.env`.

The application automatically creates the required tables when the backend starts.

---

## 🌱 Seed Initial Vehicle Data

To populate the database with the initial Youtab vehicles:

```bash
cd backend
python -m app.seed_data
```

This currently adds:

* Youtab Kourosh
* Youtab Ario
* Available vehicle colors
* Vehicle descriptions
* Base prices
* Warranty information

---

## ▶️ Running the Application

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🔐 Security Notes

Sensitive configuration is intentionally kept outside the repository.

The following should **never** be committed:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
```

For production deployment, additional security improvements are required, including:

* Restricting CORS origins
* Using a strong production `SECRET_KEY`
* Proper production payment integration
* HTTPS
* Database migration management
* Production-grade error handling
* Rate limiting
* More robust authentication and authorization

---

## 🛣️ Roadmap

Youtab is still evolving. Planned improvements include:

* [ ] More Youtab vehicle models
* [ ] Advanced vehicle configuration
* [ ] Improved responsive design
* [ ] Better mobile experience
* [ ] Real payment gateway integration
* [ ] Order tracking
* [ ] User profile dashboard
* [ ] Admin dashboard
* [ ] Advanced search and filtering
* [ ] Vehicle comparison
* [ ] Wishlist / favorites
* [ ] Database migrations with Alembic
* [ ] Automated testing
* [ ] Production deployment
* [ ] Improved API documentation

---

## 🎯 Project Goals

The project is being developed with several goals in mind:

**01 — Build a complete full-stack application**

Connect a modern frontend to a structured backend and relational database.

**02 — Create a realistic automotive experience**

Make vehicle exploration and configuration feel closer to a real digital automotive platform.

**03 — Practice production-oriented architecture**

Apply concepts such as:

* REST APIs
* ORM
* Authentication
* Database relationships
* Environment configuration
* Frontend/backend integration

**04 — Evolve Youtab into a complete automotive ecosystem**

The long-term vision is to transform the current prototype into a more comprehensive digital automotive platform.

---

## 🤝 Contributing

Youtab is currently a personal project under active development.

As the project evolves, contribution guidelines and development standards may be introduced.

For now, suggestions, ideas, and constructive feedback are welcome.

---

## 📜 License

This project is currently intended for educational and development purposes.

A formal open-source license may be added in a future release.

---

<div align="center">

### YOUTAB

**From Persia to Tomorrow.**

*Engineered for Speed.*

<br>

🚗 ⚡ 🏁

</div>

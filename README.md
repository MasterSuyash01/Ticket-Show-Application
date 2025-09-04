# 🎟️ Ticket Show Application

A Flask-based web application for managing venues, shows, ticket bookings, user accounts, and ratings.  
This project implements a complete workflow for both **users** (book tickets, register/login, rate shows) and **admins** (manage venues, shows, bookings, and view summaries).

---

## ✨ Features

### 👤 User
- Register and login with secure password hashing (Flask-Login + Werkzeug).
- Browse available venues and shows.
- Book tickets with unique booking numbers.
- View **My Bookings**.
- Rate venues and shows.
- Search for movies and venues.
- Personalized user dashboard.

### 🔑 Admin
- Admin login page (default: `admin` / `password`).
- Manage venues: **add, edit, delete**.
- Manage shows: **add, edit, delete**.
- Dashboard with search support for venues and shows.
- View ticket sales and ratings summary with **Matplotlib charts**.

### 📊 Analytics
- Ticket sales summary (bar chart).
- Show ratings summary (average ratings visualization).

---

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login  
- **Database:** SQLite (`booking.db`)  
- **Frontend:** HTML + Jinja2 templates  
- **Data Visualization:** Matplotlib  
- **Authentication:** Flask-Login, Werkzeug (password hashing)  

---


# Django CarDealer – Used Car Marketplace

## Project Overview

**Django CarDealer** is a web-based application designed to simplify and modernize the process of buying and selling used cars online.  
The platform provides a **user-friendly and efficient interface** for both buyers and sellers, ensuring a transparent and secure experience.

### 🎯 Objectives
- Allow users to easily **create accounts** and manage their car listings.  
- Provide buyers with **advanced search tools** to find cars matching their preferences.  
- Enable sellers to **publish, update, and delete** their ads with ease.  
- Ensure **authenticity and trust** by verifying car listings and user legitimacy.

---

## 🧩 Key Features

### 👤 User Management
- Secure registration and authentication system.  
- Password recovery functionality.  

### 🚗 Seller Features
- Intuitive interface to publish car ads with detailed vehicle descriptions and images.  
- Manage listings (create, update, delete).  
- View history of all published ads.  

### 🔍 Buyer Features
- Smart search bar for quick car discovery by keywords.  
- Advanced filters for narrowing results by price, brand, year, etc.  
- Detailed car view with full information and pictures.  

By combining an **intuitive interface**, **robust functionality**, and **security-first design**, Django CarDealer aims to become a trusted reference in online used car trading.

---

## ⚙️ Architecture & Technologies

| Layer              | Technology / Tool                     |
|--------------------|---------------------------------------|
| Framework          | Django (Python)                       |
| Database           | MySQL / MariaDB (or SQLite)           |
| Frontend           | HTML, CSS, JavaScript (Django templates) |
| Virtual Environment | Python venv                           |
| Image Handling     | Pillow                                |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+  
- pip  
- MySQL / MariaDB (or use SQLite for simplicity)  
- phpMyAdmin (for managing the database easily)

---

### Steps

```bash
# 1️⃣ Create and activate virtual environment
virtualenv venv
venv\Scripts\activate
```
# 2️⃣ Import the database
# Open phpMyAdmin, create a new database, import the SQL file ( in /database/ folder)
# Verify database settings in settings.py (name, user, password, host)

# 3️⃣ Install dependencies
pip install mysqlclient
python -m pip install Pillow

# 4️⃣ Verify Django version compatibility
# Check which Django version the project uses (series 3, 4, or 5)
# If installed Django is incompatible:
pip uninstall django
pip install "django==4.1.13"

# 5️⃣ Apply migrations
python manage.py migrate

# 6️⃣ Run the development server
python manage.py runserver


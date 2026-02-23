# Sittr 🐾  
Find Trusted Caretakers for Your Pets

Sittr is a Django-based web platform that connects pet owners with trusted local caretakers.  
Users can search, compare ratings, read reviews, and send hire requests in minutes.

---

## 🚀 Features

- 🔎 Search caretakers by:
  - City
  - Pet type
  - Service
  - Max price

- ⭐ Review system
  - Average rating calculation
  - Review count
  - Top-rated featured caretakers on homepage

- 📩 Hire request functionality

- 🛠 Admin panel (Unfold Admin UI)

- 🎨 Modern UI
  - Django + Tailwind CLI
  - Bootstrap 5
  - Responsive layout
  - Hero section with dynamic image blending

---

## 🏗 Tech Stack

- Python 3.13
- Django 6.0.2
- PostgreSQL
- Tailwind CSS (via django-tailwind-cli)
- Bootstrap 5
- Bootstrap Icons

---
# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/borislavbog931/Sittr.git
cd Sittr
```

---

## 2️⃣ Create & Activate Virtual Environment

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create `.env` File

Create a file named `.env` in the project root and add:

```
SECRET_KEY=your-secret-key

DB_NAME=sittr_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=5432
```

The project loads environment variables using:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 5️⃣ Setup PostgreSQL Database

Create database:

```sql
CREATE DATABASE sittr_db;
```

---

## 6️⃣ Apply Migrations

```bash
python manage.py migrate
```

---

## 7️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

---

## 8️⃣ Build Tailwind CSS

```bash
python manage.py tailwind build
```

---

## 9️⃣ Run Development Server

```bash
python manage.py runserver
```

Open in browser:

http://127.0.0.1:8000/

---
## 📂 Project Structure

```
Sittr/
│
├── common/        # Home, About, 404
├── caretakers/    # Caretaker model, filtering, detail
├── services/      # Services and Pet Types
├── reviews/       # Review system
├── requests/      # Hire request functionality
│
├── static/
│   ├── css/
│   └── images/
│
├── templates/
└── media/
```

---

## 📊 Core Logic Overview

### Homepage

Displays top 3 caretakers ordered by:

- Highest average rating  
- Highest review count  
- Active status only  

### Filtering System

Supports:

- City  
- Service  
- Pet type  
- Maximum price  

Uses `.distinct()` to prevent duplicate query results.

---

## 🧪 Future Improvements

- Authentication system  
- Caretaker dashboard  
- Messaging system  
- Booking calendar  
- Docker deployment  
- Production WSGI/ASGI configuration  

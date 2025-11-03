# 🚀 Quick Start Guide

## Starting the Application

### 1. Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Start Django Server
```powershell
python manage.py runserver
```

### 3. Open in Browser
Navigate to: **http://127.0.0.1:8000**

---

## Common Commands

### **Database Management**
```powershell
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### **Development**
```powershell
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run tests
python manage.py test
```

### **Dependency Management**
```powershell
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

---

## Project Structure

```
DDS_for Student/
├── drowsiness_app/          # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   ├── drowsiness_detector.py  # Detection algorithm
│   └── templates/           # HTML templates
├── sedds_project/           # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   └── wsgi.py              # WSGI config
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

---

## URLs

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Detection**: http://127.0.0.1:8000/detect/
- **Sessions**: http://127.0.0.1:8000/sessions/

---

## Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## Tips

1. **Always activate the virtual environment** before running commands
2. **Keep the terminal open** while the server is running
3. **Check the terminal** for error messages if something goes wrong
4. **Use Ctrl + C** to stop the server gracefully

---

**Happy Coding! 🎓**
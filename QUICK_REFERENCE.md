# 🚀 Quick Reference Card - SEDDS

## 📦 Push to GitHub (First Time)

```bash
cd "c:\Users\Hp\Desktop\College Project\DDS_for Student"
git init
git add .
git commit -m "Initial commit: SEDDS project"
git remote add origin https://github.com/yourusername/Student-Eye-Drowsiness-Detection-System.git
git branch -M main
git push -u origin main
```

## 🔄 Update GitHub (After Changes)

```bash
git add .
git commit -m "Description of your changes"
git push origin main
```

## 🏃 Run the Application

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server
python manage.py runserver

# Access at: http://127.0.0.1:8000
```

## 🛠️ Common Commands

### Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Dependencies
```bash
pip install -r requirements.txt
pip freeze > requirements.txt  # Update requirements
```

### Git
```bash
git status                    # Check changes
git log                       # View history
git branch                    # List branches
git checkout -b feature-name  # Create new branch
```

## 📁 Project Structure

```
DDS_for_Student/
├── drowsiness_app/          # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Request handlers
│   ├── urls.py              # URL routing
│   └── drowsiness_detector.py  # Detection algorithm
├── sedds_project/           # Project settings
│   └── settings.py          # Configuration
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── manage.py                # Django management
├── requirements.txt         # Dependencies
├── README.md                # Documentation
└── .gitignore              # Git exclusions
```

## 🔑 Key Files

- **README.md** - Project overview
- **SETUP.md** - Installation guide
- **CONTRIBUTING.md** - How to contribute
- **LICENSE** - MIT License
- **.gitignore** - Files to exclude from Git
- **.github_instructions.md** - GitHub setup guide

## 🎯 Important URLs

- **Homepage**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin
- **Dashboard**: http://127.0.0.1:8000/dashboard
- **Monitoring**: http://127.0.0.1:8000/start-monitoring

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | `python manage.py runserver 8080` |
| Camera not working | Check browser permissions |
| Import errors | `pip install -r requirements.txt` |
| Database errors | `python manage.py migrate` |
| Static files missing | `python manage.py collectstatic` |

## 📊 Performance Settings

Located in `drowsiness_detector.py`:

```python
# Fast (lower-end systems)
FRAME_SKIP = 3
process_size = (240, 180)

# Balanced (default)
FRAME_SKIP = 2
process_size = (320, 240)

# Accurate (high-end systems)
FRAME_SKIP = 1
process_size = (640, 480)
```

## 🔐 Security Checklist

Before pushing to GitHub:
- [ ] No database files (db.sqlite3)
- [ ] No virtual environment (venv/)
- [ ] No secret keys in code
- [ ] .gitignore is configured
- [ ] No personal data

## 📞 Support

- **Email**: kmglm04718@gmail.com
- **GitHub Issues**: Create an issue on repository
- **Documentation**: Check README.md and SETUP.md

## 🎓 Author

**Kumar Manglam**  
M2346015 | BCA 2023-2026  
C.M.P. Degree College, University of Allahabad

---

**Quick Tip**: Bookmark this file for easy reference!

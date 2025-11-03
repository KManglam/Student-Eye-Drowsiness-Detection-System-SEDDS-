# 🚀 Complete Setup Guide for SEDDS

This guide will walk you through setting up the Student Eye Drowsiness Detection System on your local machine.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

## Prerequisites

### Required Software

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Webcam** (built-in or external USB)
- **Modern Web Browser** (Chrome, Firefox, or Edge)

### System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB minimum (8GB recommended)
- **CPU**: Intel i3 or equivalent (AVX support recommended for MediaPipe)
- **Storage**: 500MB free space

### Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed or version is lower than 3.8, download and install from [python.org](https://www.python.org/downloads/).

## Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/Student-Eye-Drowsiness-Detection-System.git

# Navigate to project directory
cd Student-Eye-Drowsiness-Detection-System
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Note:** This may take 5-10 minutes depending on your internet connection.

### Step 4: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, drowsiness_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

### Step 5: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: (your choice)
- Email: (your email)
- Password: (secure password)

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Configuration

### Camera Settings

The default camera index is `0`. If you have multiple cameras, you may need to change this in `drowsiness_detector.py`:

```python
# Line 318 in drowsiness_detector.py
cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc.
```

### Performance Tuning

Edit `drowsiness_detector.py` to adjust performance settings:

```python
# For better performance (lower-end systems)
self.FRAME_SKIP = 3  # Process every 3rd frame
self.process_size = (240, 180)  # Smaller processing size

# For better accuracy (higher-end systems)
self.FRAME_SKIP = 1  # Process every frame
self.process_size = (640, 480)  # Full resolution
```

### Timezone Configuration

Update timezone in `sedds_project/settings.py`:

```python
TIME_ZONE = 'Asia/Kolkata'  # Change to your timezone
```

## Running the Application

### Step 1: Activate Virtual Environment

If not already activated:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 2: Start Development Server

```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'sedds_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

or

```
http://localhost:8000
```

## Troubleshooting

### Issue 1: Python Not Found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
- Reinstall Python and check "Add Python to PATH" during installation
- Or use `python3` instead of `python` on macOS/Linux

### Issue 2: pip Install Fails

**Error:**
```
ERROR: Could not install packages due to an OSError
```

**Solution:**
```bash
# Try with --user flag
pip install --user -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
```

### Issue 3: MediaPipe Installation Error

**Error:**
```
ERROR: Failed building wheel for mediapipe
```

**Solution:**
```bash
# Install Microsoft C++ Build Tools (Windows)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or try pre-built wheel
pip install mediapipe --no-cache-dir
```

### Issue 4: Camera Not Detected

**Error:**
```
Could not open camera
```

**Solution:**
1. Check if camera is being used by another application
2. Grant camera permissions to your browser
3. Try different camera index (0, 1, 2...)
4. On Linux, add user to video group:
   ```bash
   sudo usermod -a -G video $USER
   ```

### Issue 5: Port Already in Use

**Error:**
```
Error: That port is already in use.
```

**Solution:**
```bash
# Use a different port
python manage.py runserver 8080

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Issue 6: Static Files Not Loading

**Solution:**
```bash
# Collect static files again
python manage.py collectstatic --clear --noinput

# Check STATIC_URL in settings.py
# Should be: STATIC_URL = '/static/'
```

## Next Steps

### 1. Create Your Account

- Navigate to the registration page
- Fill in your details
- Create a secure password

### 2. Start Your First Session

- Login with your credentials
- Click "Start Monitoring"
- Allow camera permissions
- Position yourself in front of the camera

### 3. Explore Features

- View your dashboard
- Check session history
- Review detailed reports
- Adjust settings as needed

### 4. Customize Settings

- Adjust EAR threshold for sensitivity
- Change detection parameters
- Configure alert sounds
- Set up your profile

## 📚 Additional Resources

- **README.md**: Project overview and features
- **CONTRIBUTING.md**: How to contribute to the project
- **DATABASE_DOCUMENTATION.md**: Database schema details
- **TECHNICAL_ARCHITECTURE.md**: System architecture

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check existing [GitHub Issues](https://github.com/yourusername/Student-Eye-Drowsiness-Detection-System/issues)
2. Create a new issue with detailed information
3. Email: kmglm04718@gmail.com

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ is installed
- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] Database migrations are complete
- [ ] Camera is connected and working
- [ ] Browser has camera permissions
- [ ] Port 8000 is available
- [ ] Static files are collected

## 🎉 Success!

If you can see the SEDDS homepage and start a monitoring session, congratulations! You've successfully set up the system.

---

**Need more help?** Open an issue on GitHub or contact us at kmglm04718@gmail.com

# SQLite Database Documentation
## Student Eye Drowsiness Detection System (SEDDS)

---

## 🗄️ Database Overview

The SEDDS project uses **SQLite** as its primary database management system, configured through Django's ORM. SQLite is a lightweight, serverless, zero-configuration, transactional SQL database engine that's perfect for development and small to medium-scale applications.

### Database Configuration
```python
# Location: sedds_project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Database File Location
Database File: c:\Users\Hp\Desktop\College Project\DDS_for Student\db.sqlite3
Time Zone: Asia/Kolkata
```

---

## 📊 Database Schema Architecture

### Database Entity Relationship Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                     DJANGO BUILT-IN TABLES                     │
├─────────────────────────────────────────────────────────────────┤
│ auth_user                                                       │
│ ├── id (PK, BigAutoField)                                       │
│ ├── username (CharField, unique)                                │
│ ├── email (EmailField)                                          │
│ ├── first_name (CharField)                                      │
│ ├── last_name (CharField)                                       │
│ ├── password (CharField, hashed)                                │
│ ├── is_staff (BooleanField)                                     │
│ ├── is_active (BooleanField)                                    │
│ ├── date_joined (DateTimeField)                                 │
│ └── last_login (DateTimeField)                                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ (1:1 Relationship)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      USER_PROFILES TABLE                       │
├─────────────────────────────────────────────────────────────────┤
│ Table Name: user_profiles                                       │
│ ├── id (PK, BigAutoField)                                       │
│ ├── user_id (FK to auth_user) - OneToOneField                   │
│ ├── enrollment_no (CharField, 20, unique, nullable)             │
│ ├── batch_year (CharField, 20, nullable)                        │
│ ├── total_sessions (IntegerField, default=0)                    │
│ ├── total_alerts (IntegerField, default=0)                      │
│ └── created_at (DateTimeField, auto_now_add=True)               │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ (1:Many Relationship)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION_LOGS TABLE                         │
├─────────────────────────────────────────────────────────────────┤
│ Table Name: session_logs                                        │
│ ├── id (PK, BigAutoField)                                       │
│ ├── user_id (FK to auth_user) - ForeignKey                      │
│ ├── session_start (DateTimeField, default=timezone.now)         │
│ ├── session_end (DateTimeField, nullable)                       │
│ ├── alert_count (IntegerField, default=0)                       │
│ ├── drowsy_timestamps (TextField, JSON array as string)         │
│ ├── session_duration (DurationField, nullable)                  │
│ │   └── Ordering: ['-session_start'] (Most recent first)       │
│ └── CASCADE DELETE: When user deleted, all sessions deleted     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Database Tables Detailed Structure

### 1. **auth_user** (Django Built-in)
**Purpose**: Core user authentication and management

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | BigAutoField | PRIMARY KEY | Unique user identifier |
| `username` | CharField(150) | UNIQUE, NOT NULL | User login name |
| `email` | EmailField | UNIQUE | User email address |
| `first_name` | CharField(150) | | User's first name |
| `last_name` | CharField(150) | | User's last name |
| `password` | CharField(128) | NOT NULL | Hashed password (PBKDF2) |
| `is_staff` | BooleanField | DEFAULT FALSE | Admin access flag |
| `is_active` | BooleanField | DEFAULT TRUE | Account status |
| `date_joined` | DateTimeField | DEFAULT now() | Registration timestamp |
| `last_login` | DateTimeField | NULLABLE | Last login timestamp |

### 2. **user_profiles** (Custom Model)
**Purpose**: Extended user information specific to SEDDS

```sql
CREATE TABLE "user_profiles" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "enrollment_no" VARCHAR(20) UNIQUE,
    "batch_year" VARCHAR(20),
    "total_sessions" INTEGER NOT NULL DEFAULT 0,
    "total_alerts" INTEGER NOT NULL DEFAULT 0,
    "created_at" DATETIME NOT NULL,
    "user_id" INTEGER NOT NULL UNIQUE REFERENCES "auth_user" ("id") 
        DEFERRABLE INITIALLY DEFERRED
);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | BigAutoField | PRIMARY KEY | Unique profile identifier |
| `user_id` | OneToOneField | FK to auth_user, CASCADE | Links to Django user |
| `enrollment_no` | CharField(20) | UNIQUE, NULLABLE | Student enrollment number |
| `batch_year` | CharField(20) | NULLABLE | Student batch/academic year |
| `total_sessions` | IntegerField | DEFAULT 0 | Cached total session count |
| `total_alerts` | IntegerField | DEFAULT 0 | Cached total alert count |
| `created_at` | DateTimeField | AUTO_NOW_ADD | Profile creation timestamp |

**Business Rules**:
- Automatically created when user registers
- Statistics updated via `update_stats()` method
- One-to-one relationship with Django User model

### 3. **session_logs** (Core Drowsiness Data)
**Purpose**: Stores all drowsiness detection session information

```sql
CREATE TABLE "session_logs" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "session_start" DATETIME NOT NULL,
    "session_end" DATETIME,
    "alert_count" INTEGER NOT NULL DEFAULT 0,
    "drowsy_timestamps" TEXT NOT NULL DEFAULT '[]',
    "session_duration" REAL,
    "user_id" INTEGER NOT NULL REFERENCES "auth_user" ("id") 
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX "session_logs_user_id_idx" ON "session_logs" ("user_id");
CREATE INDEX "session_logs_session_start_idx" ON "session_logs" ("session_start");
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | BigAutoField | PRIMARY KEY | Unique session identifier |
| `user_id` | ForeignKey | FK to auth_user, CASCADE | Session owner |
| `session_start` | DateTimeField | DEFAULT timezone.now | Session start timestamp |
| `session_end` | DateTimeField | NULLABLE | Session end timestamp |
| `alert_count` | IntegerField | DEFAULT 0 | Number of drowsiness alerts |
| `drowsy_timestamps` | TextField | DEFAULT '[]' | JSON array of alert timestamps |
| `session_duration` | DurationField | NULLABLE | Calculated session duration |

**Business Rules**:
- Ordered by most recent sessions first (`ordering = ['-session_start']`)
- Cascade delete when user is deleted
- JSON data stored in `drowsy_timestamps` field

---

## 💾 Data Storage Mechanisms

### 1. **JSON Data Storage in drowsy_timestamps**

**Implementation Pattern**:
```python
# Data Structure in drowsy_timestamps field
[
    "2024-01-15T10:30:45.123456+05:30",  # ISO format timestamp
    "2024-01-15T10:32:15.789012+05:30",
    "2024-01-15T10:35:22.456789+05:30"
]

# Storage Method
def add_drowsy_alert(self, timestamp=None):
    """Add a drowsiness alert timestamp"""
    if timestamp is None:
        timestamp = timezone.now().isoformat()
    
    try:
        timestamps = json.loads(self.drowsy_timestamps)  # Parse existing JSON
    except (json.JSONDecodeError, TypeError):
        timestamps = []  # Initialize empty if corrupt
    
    timestamps.append(timestamp)  # Add new timestamp
    self.drowsy_timestamps = json.dumps(timestamps)  # Store as JSON string
    self.alert_count += 1  # Increment counter
    self.save()  # Persist to database
```

### 2. **Duration Calculation and Storage**

```python
def end_session(self):
    """End the current session and calculate duration"""
    self.session_end = timezone.now()
    if self.session_start:
        self.session_duration = self.session_end - self.session_start
    self.save()

def get_session_duration_str(self):
    """Get session duration as formatted string"""
    if self.session_duration:
        total_seconds = int(self.session_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"
```

### 3. **Statistics Aggregation**

```python
def update_stats(self):
    """Update user statistics based on session logs"""
    sessions = SessionLog.objects.filter(user=self.user)
    self.total_sessions = sessions.count()
    self.total_alerts = sum(session.alert_count for session in sessions)
    self.save()
```

---

## 🔄 Database Operations in Views

### 1. **Session Creation and Management**

```python
# Start New Session
def start_monitoring(request):
    user_id = request.user.id
    
    # End any existing session
    end_active_session(user_id)
    
    # Create new session
    session = SessionLog.objects.create(user=request.user)
    active_sessions[user_id] = session
    
    return render(request, 'drowsiness_app/monitoring.html', {
        'session_id': session.id
    })

# Session Termination
def end_active_session(user_id):
    if user_id in active_sessions:
        session = active_sessions[user_id]
        session.end_session()  # Calculates and saves duration
        return session
    return None
```

### 2. **User Registration with Profile Creation**

```python
def register_view(request):
    try:
        # Create Django user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=username.title()
        )
        
        # Create extended profile
        UserProfile.objects.create(
            user=user,
            enrollment_no=enrollment_no,
            batch_year=batch_year
        )
        
        messages.success(request, 'Registration successful!')
        return redirect('login')
        
    except Exception as e:
        messages.error(request, f'Registration failed: {str(e)}')
```

### 3. **Data Retrieval and Analytics**

```python
# Dashboard Statistics
@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get recent sessions
    recent_sessions = SessionLog.objects.filter(user=request.user)[:5]
    
    # Analytics aggregation
    stats = SessionLog.objects.filter(user=request.user).aggregate(
        total_sessions=Count('id'),
        total_alerts=Sum('alert_count'),
        avg_duration=Avg('session_duration')
    )

# Session History
def session_history(request):
    sessions = SessionLog.objects.filter(user=request.user).order_by('-session_start')
```

---

## 🎯 Database Performance Optimizations

### 1. **Indexing Strategy**
```sql
-- Automatic Django indexes
CREATE INDEX "session_logs_user_id_idx" ON "session_logs" ("user_id");
CREATE INDEX "session_logs_session_start_idx" ON "session_logs" ("session_start");
CREATE INDEX "user_profiles_user_id_unique" ON "user_profiles" ("user_id");

-- Query optimization for frequent operations
-- Most common queries:
-- 1. SELECT sessions by user_id (indexed)
-- 2. ORDER BY session_start DESC (indexed)
-- 3. JOIN user_profiles with auth_user (indexed FK)
```

### 2. **Query Optimization Patterns**

```python
# Efficient session retrieval with select_related
def get_user_sessions_optimized(user):
    return SessionLog.objects.filter(user=user)\
                           .select_related('user')\
                           .order_by('-session_start')

# Bulk statistics calculation
def get_dashboard_stats(user):
    return {
        'sessions': SessionLog.objects.filter(user=user).count(),
        'alerts': SessionLog.objects.filter(user=user)
                             .aggregate(Sum('alert_count'))['alert_count__sum'] or 0,
        'avg_duration': SessionLog.objects.filter(user=user)
                                  .aggregate(Avg('session_duration'))['session_duration__avg']
    }
```

### 3. **Memory Management for JSON Data**

```python
# Efficient JSON handling for large timestamp arrays
def get_drowsy_events_paginated(session, page_size=50):
    """Handle large JSON arrays efficiently"""
    try:
        all_timestamps = json.loads(session.drowsy_timestamps)
        start = (page - 1) * page_size
        end = start + page_size
        return all_timestamps[start:end]
    except (json.JSONDecodeError, TypeError):
        return []
```

---

## 📈 Database Growth and Scaling Considerations

### Current Storage Requirements
```
Estimated Storage per User per Month:
- UserProfile: ~150 bytes per user
- SessionLog: ~200 bytes per session
- Average 20 sessions/user/month = 4KB per user per month
- drowsy_timestamps JSON: ~50 bytes per alert
- Average 10 alerts per session = 500 bytes per session

Total: ~4.5KB per active user per month
```

### Scaling Strategy
```python
# Database maintenance commands
# 1. Clean old sessions (run monthly)
def cleanup_old_sessions(days_old=90):
    cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
    SessionLog.objects.filter(session_start__lt=cutoff_date).delete()

# 2. Optimize JSON storage for large datasets
def compress_drowsy_timestamps():
    sessions = SessionLog.objects.filter(alert_count__gt=100)
    for session in sessions:
        # Implement timestamp compression if needed
        pass

# 3. Archive completed sessions
def archive_completed_sessions():
    completed_sessions = SessionLog.objects.filter(
        session_end__isnull=False,
        session_start__lt=timezone.now() - timezone.timedelta(days=30)
    )
    # Move to archive table or file
```

---

## 🔐 Database Security and Integrity

### 1. **Data Integrity Constraints**
```python
# Model-level validation
class UserProfile(models.Model):
    enrollment_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    def clean(self):
        # Custom validation
        if self.enrollment_no and not self.enrollment_no.isalnum():
            raise ValidationError('Enrollment number must be alphanumeric')

# Database-level constraints
# - Foreign key constraints prevent orphaned records
# - Unique constraints prevent duplicate enrollments
# - NOT NULL constraints ensure data completeness
```

### 2. **Backup and Recovery Strategy**
```bash
# Automated backup (run daily)
# Location: db.sqlite3
# Size: Typically < 10MB for moderate usage

# Backup command (Windows)
copy "db.sqlite3" "backups\db_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sqlite3"

# Recovery process
# 1. Stop Django application
# 2. Replace db.sqlite3 with backup
# 3. Run migrations if needed: python manage.py migrate
# 4. Restart application
```

---

## 🛠️ Database Maintenance and Monitoring

### Regular Maintenance Tasks
```python
# Django management commands for database maintenance

# 1. Database integrity check
python manage.py dbshell
# PRAGMA integrity_check;

# 2. Vacuum database (reclaim space)
# VACUUM;

# 3. Analyze database (update statistics)
# ANALYZE;

# 4. Check foreign key constraints
# PRAGMA foreign_key_check;
```

### Monitoring Queries
```sql
-- Database size monitoring
SELECT 
    page_count * page_size as size_bytes,
    page_count * page_size / 1024.0 / 1024.0 as size_mb 
FROM pragma_page_count(), pragma_page_size();

-- Table sizes
SELECT 
    name,
    COUNT(*) as row_count
FROM sqlite_master sm
JOIN (
    SELECT name FROM sqlite_master WHERE type='table'
) tables ON tables.name = sm.name
GROUP BY name;

-- Session statistics
SELECT 
    DATE(session_start) as date,
    COUNT(*) as sessions,
    SUM(alert_count) as total_alerts,
    AVG(alert_count) as avg_alerts_per_session
FROM session_logs
WHERE session_start >= date('now', '-30 days')
GROUP BY DATE(session_start)
ORDER BY date DESC;
```

---

## 📝 Database Migration History

### Migration Files Structure
```
drowsiness_app/migrations/
├── __init__.py
├── 0001_initial.py          # Creates SessionLog and UserProfile tables
└── __pycache__/             # Compiled migration files
```

### Initial Migration (0001_initial.py)
```python
# Generated by Django 5.2.5 on 2025-01-15 08:34

operations = [
    migrations.CreateModel(
        name='SessionLog',
        fields=[
            ('id', models.BigAutoField(primary_key=True)),
            ('session_start', models.DateTimeField(default=django.utils.timezone.now)),
            ('session_end', models.DateTimeField(blank=True, null=True)),
            ('alert_count', models.IntegerField(default=0)),
            ('drowsy_timestamps', models.TextField(default='[]')),
            ('session_duration', models.DurationField(blank=True, null=True)),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ],
        options={
            'db_table': 'session_logs',
            'ordering': ['-session_start'],
        },
    ),
    migrations.CreateModel(
        name='UserProfile',
        fields=[
            ('id', models.BigAutoField(primary_key=True)),
            ('enrollment_no', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ('batch_year', models.CharField(blank=True, max_length=20, null=True)),
            ('total_sessions', models.IntegerField(default=0)),
            ('total_alerts', models.IntegerField(default=0)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ],
        options={
            'db_table': 'user_profiles',
        },
    ),
]
```

---

## 🔚 Conclusion

The SQLite database implementation in SEDDS provides:

### ✅ **Strengths**
- **Lightweight**: Zero-configuration, embedded database
- **ACID Compliance**: Ensures data integrity
- **Django Integration**: Seamless ORM integration
- **JSON Support**: Flexible drowsiness timestamp storage
- **Performance**: Optimized for read-heavy workloads

### 📊 **Use Cases Covered**
- User authentication and profile management
- Real-time session logging
- Drowsiness event timestamping
- Historical data analysis
- Performance statistics

### 🚀 **Scalability Path**
- Current: SQLite for development/small deployments
- Future: PostgreSQL/MySQL for production scaling
- Data migration path available through Django ORM

This database architecture efficiently supports the core functionality of the drowsiness detection system while maintaining simplicity and reliability.
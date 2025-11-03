""" 
Models for Student Eye Drowsiness Detection System
Using SQLite for data storage
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class SessionLog(models.Model):
    """
    Model to store drowsiness detection session logs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_start = models.DateTimeField(default=timezone.now)
    session_end = models.DateTimeField(null=True, blank=True)
    alert_count = models.IntegerField(default=0)
    drowsy_timestamps = models.TextField(default='[]')  # Store timestamps of drowsiness alerts as JSON string
    session_duration = models.DurationField(null=True, blank=True)
    
    class Meta:
        db_table = 'session_logs'
        ordering = ['-session_start']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def add_drowsy_alert(self, timestamp=None):
        """Add a drowsiness alert timestamp"""
        if timestamp is None:
            timestamp = timezone.now().isoformat()
        
        try:
            timestamps = json.loads(self.drowsy_timestamps)
        except (json.JSONDecodeError, TypeError):
            timestamps = []
        
        timestamps.append(timestamp)
        self.drowsy_timestamps = json.dumps(timestamps)
        self.alert_count += 1
        self.save()
    
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


class UserProfile(models.Model):
    """
    Extended user profile for additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    batch_year = models.CharField(max_length=20, null=True, blank=True)
    total_sessions = models.IntegerField(default=0)
    total_alerts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def update_stats(self):
        """Update user statistics based on session logs"""
        sessions = SessionLog.objects.filter(user=self.user)
        self.total_sessions = sessions.count()
        self.total_alerts = sum(session.alert_count for session in sessions)
        self.save()


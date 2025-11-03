"""
Admin configuration for Student Eye Drowsiness Detection System
"""
from django.contrib import admin
from .models import SessionLog, UserProfile


@admin.register(SessionLog)
class SessionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_start', 'session_end', 'alert_count', 'get_session_duration_str']
    list_filter = ['session_start', 'user']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['session_start', 'drowsy_timestamps']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrollment_no', 'batch_year', 'total_sessions', 'total_alerts', 'created_at']
    list_filter = ['batch_year', 'created_at']
    search_fields = ['user__username', 'user__email', 'enrollment_no']
    readonly_fields = ['total_sessions', 'total_alerts', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
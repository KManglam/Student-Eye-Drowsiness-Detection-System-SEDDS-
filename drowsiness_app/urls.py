"""
URL patterns for Student Eye Drowsiness Detection System
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and monitoring URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-monitoring/', views.start_monitoring, name='start_monitoring'),
    path('stop-monitoring/', views.stop_monitoring, name='stop_monitoring'),
    
    # Session management URLs
    path('session-report/<int:session_id>/', views.session_report, name='session_report'),
    path('session-history/', views.session_history, name='session_history'),
    
    # API endpoints
    path('api/drowsiness-alert/', views.drowsiness_alert, name='drowsiness_alert'),
    path('api/session-stats/', views.get_session_stats, name='session_stats'),
    path('video-feed/', views.video_feed, name='video_feed'),
]
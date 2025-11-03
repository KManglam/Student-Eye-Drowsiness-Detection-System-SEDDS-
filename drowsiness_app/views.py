"""
Views for Student Eye Drowsiness Detection System
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timezone import localtime
from django.db.models import Sum, Avg
import json
import cv2
import threading
import time
from .models import SessionLog, UserProfile
from .drowsiness_detector import DrowsinessDetector


# Global variables for video streaming
active_detectors = {}
active_sessions = {}


def home(request):
    """
    Home page view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'drowsiness_app/home.html')


def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        enrollment_no = request.POST.get('enrollment_no')
        batch_year = request.POST.get('batch_year')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'drowsiness_app/register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'drowsiness_app/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'drowsiness_app/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'drowsiness_app/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=username.title()
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                enrollment_no=enrollment_no,
                batch_year=batch_year
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'drowsiness_app/register.html')


def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'drowsiness_app/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'drowsiness_app/login.html')


def logout_view(request):
    """
    User logout view
    """
    # End any active session
    if request.user.is_authenticated:
        end_active_session(request.user.id)
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """
    User dashboard view
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get recent sessions
    recent_sessions = SessionLog.objects.filter(user=request.user)[:5]
    
    # Calculate statistics
    total_sessions = SessionLog.objects.filter(user=request.user).count()
    total_alerts = SessionLog.objects.filter(user=request.user).aggregate(
        total=Sum('alert_count')
    )['total'] or 0
    
    avg_alerts = SessionLog.objects.filter(user=request.user).aggregate(
        avg=Avg('alert_count')
    )['avg'] or 0
    
    context = {
        'profile': profile,
        'recent_sessions': recent_sessions,
        'total_sessions': total_sessions,
        'total_alerts': total_alerts,
        'avg_alerts': round(avg_alerts, 2),
    }
    
    return render(request, 'drowsiness_app/dashboard.html', context)


@login_required
def start_monitoring(request):
    """
    Start drowsiness monitoring session
    """
    user_id = request.user.id
    
    # End any existing session
    end_active_session(user_id)
    
    # Create new session
    session = SessionLog.objects.create(user=request.user)
    active_sessions[user_id] = session
    
    return render(request, 'drowsiness_app/monitoring.html', {
        'session_id': session.id
    })


@login_required
def stop_monitoring(request):
    """
    Stop drowsiness monitoring session
    """
    user_id = request.user.id
    
    # End active session
    session = end_active_session(user_id)
    
    if session:
        messages.success(request, 'Monitoring session ended successfully.')
        return redirect('session_report', session_id=session.id)
    
    return redirect('dashboard')


def end_active_session(user_id):
    """
    Helper function to end active session
    """
    if user_id in active_sessions:
        session = active_sessions[user_id]
        session.end_session()
        
        # Stop detector if running
        if user_id in active_detectors:
            active_detectors[user_id].stop_detection()
            del active_detectors[user_id]
        
        del active_sessions[user_id]
        return session
    return None


@login_required
def session_report(request, session_id):
    """
    Display session report
    """
    try:
        session = SessionLog.objects.get(id=session_id, user=request.user)
        
        # Parse drowsy timestamps
        drowsy_times = []
        if session.drowsy_timestamps:
            if isinstance(session.drowsy_timestamps, str):
                drowsy_times = json.loads(session.drowsy_timestamps)
            else:
                drowsy_times = session.drowsy_timestamps
        
        context = {
            'session': session,
            'drowsy_times': drowsy_times,
        }
        
        return render(request, 'drowsiness_app/session_report.html', context)
        
    except SessionLog.DoesNotExist:
        messages.error(request, 'Session not found.')
        return redirect('dashboard')


@login_required
def session_history(request):
    """
    Display user's session history
    """
    sessions = SessionLog.objects.filter(user=request.user).order_by('-session_start')
    
    context = {
        'sessions': sessions,
    }
    
    return render(request, 'drowsiness_app/session_history.html', context)


@csrf_exempt
@login_required
def drowsiness_alert(request):
    """
    Handle drowsiness alert from frontend
    """
    if request.method == 'POST':
        user_id = request.user.id
        
        if user_id in active_sessions:
            session = active_sessions[user_id]
            session.add_drowsy_alert()
            
            return JsonResponse({
                'status': 'success',
                'alert_count': session.alert_count
            })
    
    return JsonResponse({'status': 'error'})


def generate_video_feed(user_id):
    """
    Generate video feed for streaming
    """
    detector = DrowsinessDetector()
    active_detectors[user_id] = detector
    
    # Set up callbacks
    def on_drowsiness():
        if user_id in active_sessions:
            session = active_sessions[user_id]
            session.add_drowsy_alert()
    
    detector.on_drowsiness_detected = on_drowsiness
    
    # Start camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        while user_id in active_detectors:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally
            frame = cv2.flip(frame, 1)
            
            # Process frame
            processed_frame, ear_value, is_drowsy = detector.process_frame(frame)
            
            if processed_frame is not None:
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', processed_frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS
            
    finally:
        cap.release()
        if user_id in active_detectors:
            del active_detectors[user_id]


@login_required
def video_feed(request):
    """
    Video streaming endpoint
    """
    user_id = request.user.id
    
    return StreamingHttpResponse(
        generate_video_feed(user_id),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@login_required
def get_session_stats(request):
    """
    Get current session statistics
    """
    user_id = request.user.id
    
    if user_id in active_sessions:
        session = active_sessions[user_id]
        
        # Calculate session duration
        duration = timezone.now() - session.session_start
        duration_str = str(duration).split('.')[0]  # Remove microseconds
        
        # Convert session start time to local timezone
        local_start_time = localtime(session.session_start)
        
        return JsonResponse({
            'status': 'active',
            'alert_count': session.alert_count,
            'duration': duration_str,
            'session_start': local_start_time.strftime('%H:%M:%S')
        })
    
    return JsonResponse({'status': 'inactive'})
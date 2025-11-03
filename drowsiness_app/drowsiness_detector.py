"""
Core Drowsiness Detection Algorithm
Student Eye Drowsiness Detection System
This module implements the Eye Aspect Ratio (EAR) algorithm using MediaPipe
for real-time drowsiness detection through webcam feed.
"""

import cv2
import numpy as np
import time
import threading
import platform
import os
from scipy.spatial import distance as dist

# MediaPipe for face detection
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: MediaPipe not available, falling back to Haar Cascades")

# Audio alert imports
try:
    if platform.system() == "Windows":
        import winsound
    else:
        # For non-Windows systems, we'll use a simple beep
        pass
except ImportError:
    print("Warning: Audio alert libraries not available")


class DrowsinessDetector:
    """
    Real-time drowsiness detection using Eye Aspect Ratio (EAR) calculation
    Enhanced with MediaPipe for better performance and accuracy
    """
    
    def __init__(self):
        # Detection method setup
        self.use_mediapipe = MEDIAPIPE_AVAILABLE
        
        if self.use_mediapipe:
            # MediaPipe face mesh setup
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.mp_drawing = mp.solutions.drawing_utils
            
            # Eye landmark indices for MediaPipe Face Mesh
            self.LEFT_EYE_LANDMARKS = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
            self.RIGHT_EYE_LANDMARKS = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
            
            # Simplified eye landmarks for EAR calculation (6 points each eye)
            self.LEFT_EYE_POINTS = [33, 160, 158, 133, 153, 144]  # outer, top, bottom, inner, top, bottom
            self.RIGHT_EYE_POINTS = [362, 385, 387, 263, 373, 380]
        else:
            # Fallback to OpenCV Haar Cascades
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Eye detection parameters
        self.EAR_THRESHOLD = 0.25  # EAR threshold for drowsiness
        self.CONSECUTIVE_FRAMES = 20  # Frames to consider drowsy
        self.FRAME_SKIP = 2  # Process every nth frame for performance
        
        # State variables
        self.ear_values = []
        self.frame_counter = 0
        self.drowsy_counter = 0
        self.alert_triggered = False
        self.is_running = False
        self.frame_count = 0
        
        # Performance optimization
        self.process_size = (320, 240)  # Smaller size for processing
        self.display_size = (640, 480)  # Full size for display
        
        # Callback functions
        self.on_drowsiness_detected = None
        self.on_frame_processed = None
        
    def calculate_ear(self, eye_points):
        """
        Calculate Eye Aspect Ratio (EAR) for given eye points
        
        Args:
            eye_points: Array of 6 (x, y) coordinates for eye landmarks
            
        Returns:
            float: EAR value
        """
        # Vertical eye distances
        A = dist.euclidean(eye_points[1], eye_points[5])
        B = dist.euclidean(eye_points[2], eye_points[4])
        
        # Horizontal eye distance
        C = dist.euclidean(eye_points[0], eye_points[3])
        
        # Eye Aspect Ratio calculation
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_eyes_mediapipe(self, frame):
        """
        Detect eyes and calculate EAR using MediaPipe Face Mesh
        Returns average EAR of both eyes
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            landmarks = []
            
            # Extract landmark coordinates
            h, w = frame.shape[:2]
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                landmarks.append((x, y))
            
            # Extract eye points
            left_eye_points = [landmarks[i] for i in self.LEFT_EYE_POINTS]
            right_eye_points = [landmarks[i] for i in self.RIGHT_EYE_POINTS]
            
            # Calculate EAR for both eyes
            left_ear = self.calculate_ear(left_eye_points)
            right_ear = self.calculate_ear(right_eye_points)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Draw eye landmarks
            for point in left_eye_points + right_eye_points:
                cv2.circle(frame, point, 2, (0, 255, 0), -1)
            
            return avg_ear
        
        return None
    
    def detect_eyes_haar(self, frame):
        """
        Fallback eye detection using Haar Cascades
        Returns estimated EAR based on eye count
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 4)
        
        eye_count = 0
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Region of interest for eyes (upper 60% of face)
            roi_gray = gray[y:y+int(h*0.6), x:x+w]
            roi_color = frame[y:y+int(h*0.6), x:x+w]
            
            # Detect eyes in the face region
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            eye_count = len(eyes)
            
            # Draw rectangles around eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        # Estimate EAR based on eye count (rough approximation)
        if eye_count >= 2:
            return 0.3  # Eyes open
        elif eye_count == 1:
            return 0.2  # Partially closed
        else:
            return 0.15  # Eyes closed
    
    def detect_eyes(self, frame):
        """
        Main eye detection method that uses the best available approach
        """
        if self.use_mediapipe:
            return self.detect_eyes_mediapipe(frame)
        else:
            return self.detect_eyes_haar(frame)
    
    def play_alert_sound(self):
        """
        Play alert sound using system capabilities
        """
        try:
            if platform.system() == "Windows":
                # Use Windows system beep
                winsound.Beep(1000, 500)  # 1000Hz for 500ms
            else:
                # For Linux/Mac, try to use system bell
                os.system('echo -e "\a"')
        except Exception as e:
            print(f"Could not play alert sound: {e}")
    
    def process_frame(self, frame):
        """
        Process a single frame for drowsiness detection
        
        Returns:
            tuple: (processed_frame, ear_value, is_drowsy)
        """
        if frame is None:
            return None, 0.0, False
        
        self.frame_count += 1
        is_drowsy = False
        ear_value = 0.0
        
        # Skip frames for performance optimization
        if self.frame_count % self.FRAME_SKIP != 0:
            # Return previous EAR value for skipped frames
            if len(self.ear_values) > 0:
                ear_value = self.ear_values[-1]
            
            # Display previous state information
            self._draw_frame_info(frame, ear_value, is_drowsy)
            return frame, ear_value, is_drowsy
        
        # Resize frame for processing (performance optimization)
        small_frame = cv2.resize(frame, self.process_size)
        
        # Detect eyes and calculate EAR
        ear_value = self.detect_eyes(small_frame)
        
        if ear_value is None:
            ear_value = 0.3  # Default value when no face detected
        
        # Store EAR value for analysis
        self.ear_values.append(ear_value)
        if len(self.ear_values) > 100:  # Keep last 100 values
            self.ear_values.pop(0)
        
        # Check for drowsiness (EAR below threshold)
        if ear_value < self.EAR_THRESHOLD:
            self.frame_counter += 1
            
            if self.frame_counter >= self.CONSECUTIVE_FRAMES:
                if not self.alert_triggered:
                    is_drowsy = True
                    self.alert_triggered = True
                    self.drowsy_counter += 1
                    
                    # Play alert sound in separate thread
                    threading.Thread(target=self.play_alert_sound, daemon=True).start()
                    
                    # Trigger callback if set
                    if self.on_drowsiness_detected:
                        self.on_drowsiness_detected()
                
                # Draw drowsiness warning
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, "Wake Up!", (10, 65),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            self.frame_counter = 0
            self.alert_triggered = False
        
        # Draw frame information
        self._draw_frame_info(frame, ear_value, is_drowsy)
        
        # Trigger frame processed callback
        if self.on_frame_processed:
            self.on_frame_processed(ear_value, is_drowsy)
        
        return frame, ear_value, is_drowsy
    
    def _draw_frame_info(self, frame, ear_value, is_drowsy):
        """
        Draw information overlay on the frame
        """
        # Status color based on drowsiness
        color = (0, 0, 255) if is_drowsy else (0, 255, 0)
        
        # Display EAR value and status
        cv2.putText(frame, f"EAR: {ear_value:.3f}", (frame.shape[1] - 150, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"Alerts: {self.drowsy_counter}", (frame.shape[1] - 150, 55),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Status indicator
        status_text = "DROWSY" if is_drowsy else "ALERT"
        cv2.putText(frame, status_text, (frame.shape[1] - 150, 80),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Threshold line visualization
        bar_width = 200
        bar_height = 10
        bar_x = 10
        bar_y = frame.shape[0] - 30
        
        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        
        # EAR level bar
        ear_width = int((ear_value / 0.5) * bar_width)  # Normalize to 0.5 max
        ear_width = min(ear_width, bar_width)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + ear_width, bar_y + bar_height), color, -1)
        
        # Threshold indicator
        threshold_x = int(self.EAR_THRESHOLD / 0.5 * bar_width) + bar_x
        cv2.line(frame, (threshold_x, bar_y - 5), (threshold_x, bar_y + bar_height + 5), (255, 255, 0), 2)
    
    def start_detection(self, camera_index=0):
        """
        Start real-time drowsiness detection using webcam
        """
        self.is_running = True
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            raise Exception("Could not open camera")
        
        # Set camera properties for optimal performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.display_size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.display_size[1])
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to decrease latency
        
        try:
            while self.is_running:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                processed_frame, ear_value, is_drowsy = self.process_frame(frame)
                
                if processed_frame is not None:
                    # Display frame
                    cv2.imshow('Student Eye Drowsiness Detection System', processed_frame)
                
                # Check for exit key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def stop_detection(self):
        """
        Stop the drowsiness detection
        """
        self.is_running = False
    
    def reset_counters(self):
        """
        Reset all counters for new session
        """
        self.frame_counter = 0
        self.drowsy_counter = 0
        self.alert_triggered = False
        self.ear_values = []
        self.frame_count = 0
    
    def get_statistics(self):
        """
        Get detection statistics
        """
        return {
            'total_alerts': self.drowsy_counter,
            'average_ear': np.mean(self.ear_values) if self.ear_values else 0.0,
            'min_ear': np.min(self.ear_values) if self.ear_values else 0.0,
            'max_ear': np.max(self.ear_values) if self.ear_values else 0.0,
            'current_ear': self.ear_values[-1] if self.ear_values else 0.0
        }


# Test function for standalone usage
if __name__ == "__main__":
    detector = DrowsinessDetector()
    
    def on_drowsy():
        print("DROWSINESS DETECTED!")
    
    detector.on_drowsiness_detected = on_drowsy
    
    try:
        print("Starting drowsiness detection... Press 'q' to quit")
        detector.start_detection()
    except KeyboardInterrupt:
        print("Detection stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        detector.stop_detection()
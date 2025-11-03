// Main JavaScript for Student Eye Drowsiness Detection System      

// Global variables
let isMonitoring = false;
let sessionStartTime = null;
let alertCount = 0;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit' || this.classList.contains('btn-primary')) {
                addLoadingState(this);
            }
        });
    });
}

// Add loading state to button
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    button.disabled = true;

    // Remove loading state after 3 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 3000);
}

// Remove loading state from button
function removeLoadingState(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    // Auto remove after duration
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, duration);
}

// Format duration
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Get current time string
function getCurrentTimeString() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Validate form inputs
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return isValid;
}

// Handle form submission
function handleFormSubmit(formId, callback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm(formId)) {
            if (callback) callback(form);
        } else {
            showNotification('Please fill in all required fields.', 'warning');
        }
    });
}

// Camera permission check
async function checkCameraPermission() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.getTracks().forEach(track => track.stop());
        return true;
    } catch (error) {
        console.error('Camera permission denied:', error);
        return false;
    }
}

// Start monitoring session
async function startMonitoringSession() {
    // Check camera permission
    const hasPermission = await checkCameraPermission();
    if (!hasPermission) {
        showNotification('Camera permission is required for monitoring.', 'error');
        return false;
    }

    isMonitoring = true;
    sessionStartTime = new Date();
    alertCount = 0;

    showNotification('Monitoring session started successfully!', 'success');
    return true;
}

// Stop monitoring session
function stopMonitoringSession() {
    isMonitoring = false;
    sessionStartTime = null;
    
    showNotification('Monitoring session stopped.', 'info');
}

// Handle drowsiness alert
function handleDrowsinessAlert() {
    alertCount++;
    
    // Play alert sound
    playAlertSound();
    
    // Show visual alert
    showNotification('Drowsiness detected! Please stay alert.', 'warning', 3000);
    
    // Log alert
    logDrowsinessAlert();
}

// Play alert sound
function playAlertSound() {
    try {
        // Create audio context for beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800; // 800 Hz
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
        console.error('Could not play alert sound:', error);
    }
}

// Log drowsiness alert
function logDrowsinessAlert() {
    const timestamp = new Date().toISOString();
    console.log(`Drowsiness alert logged at: ${timestamp}`);
    
    // Send to server if monitoring is active
    if (isMonitoring) {
        fetch('/api/drowsiness-alert/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                timestamp: timestamp,
                alert_count: alertCount
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Alert logged successfully:', data);
        })
        .catch(error => {
            console.error('Error logging alert:', error);
        });
    }
}

// Get CSRF token
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Update session statistics
function updateSessionStats() {
    if (!isMonitoring || !sessionStartTime) return;

    const now = new Date();
    const duration = Math.floor((now - sessionStartTime) / 1000);
    
    // Update duration display
    const durationElement = document.getElementById('sessionDuration');
    if (durationElement) {
        durationElement.textContent = formatDuration(duration);
    }
    
    // Update alert count display
    const alertElement = document.getElementById('alertCount');
    if (alertElement) {
        alertElement.textContent = alertCount;
    }
    
    // Update current time display
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        timeElement.textContent = getCurrentTimeString();
    }
}

// Initialize session statistics updater
function initSessionStatsUpdater() {
    setInterval(updateSessionStats, 1000); // Update every second
}

// Handle page visibility change
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('Page hidden - monitoring continues in background');
    } else {
        console.log('Page visible - full monitoring active');
        // Refresh session stats when page becomes visible
        updateSessionStats();
    }
});

// Handle beforeunload event
window.addEventListener('beforeunload', function(e) {
    if (isMonitoring) {
        e.preventDefault();
        e.returnValue = 'You have an active monitoring session. Are you sure you want to leave?';
        return e.returnValue;
    }
});

// Utility function to debounce function calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Utility function to throttle function calls
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Export functions for global use
window.SEDDS = {
    showNotification,
    startMonitoringSession,
    stopMonitoringSession,
    handleDrowsinessAlert,
    formatDuration,
    validateForm,
    checkCameraPermission
};

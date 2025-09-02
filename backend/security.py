#!/usr/bin/env python3
"""
Security module for EduAccess API
Provides rate limiting, input validation, and security utilities
"""

from flask import request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import re
import html
import bleach
from datetime import datetime
import logging

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour"],
    storage_uri="memory://"
)

# Security constants
MAX_STRING_LENGTH = 1000
MAX_TEXT_LENGTH = 10000
ALLOWED_HTML_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
ALLOWED_HTML_ATTRIBUTES = {}

# Input validation patterns
PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'username': r'^[a-zA-Z0-9_]{3,30}$',
    'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$',
    'filename': r'^[a-zA-Z0-9._-]+$',
    'subject': r'^[a-zA-Z0-9\s_-]{1,50}$',
    'exam_type': r'^[a-zA-Z0-9\s_-]{1,30}$',
    'year': r'^(19|20)\d{2}$'
}

class SecurityError(Exception):
    """Custom security exception"""
    pass

class InputValidator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or len(email) > 254:
            return False
        return re.match(PATTERNS['email'], email.strip()) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if not username:
            return False
        return re.match(PATTERNS['username'], username.strip()) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or len(password) < 8 or len(password) > 128:
            return False
        return re.match(PATTERNS['password'], password) is not None
    
    @staticmethod
    def validate_string(value, max_length=MAX_STRING_LENGTH, pattern=None):
        """Validate string input"""
        if not isinstance(value, str):
            return False
        if len(value) > max_length:
            return False
        if pattern and not re.match(pattern, value):
            return False
        return True
    
    @staticmethod
    def validate_integer(value, min_val=None, max_val=None):
        """Validate integer input"""
        try:
            int_val = int(value)
            if min_val is not None and int_val < min_val:
                return False
            if max_val is not None and int_val > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_year(year):
        """Validate year format"""
        if not year:
            return False
        return re.match(PATTERNS['year'], str(year)) is not None
    
    @staticmethod
    def validate_subject(subject):
        """Validate subject name"""
        if not subject:
            return False
        return re.match(PATTERNS['subject'], subject.strip()) is not None
    
    @staticmethod
    def validate_exam_type(exam_type):
        """Validate exam type"""
        if not exam_type:
            return False
        return re.match(PATTERNS['exam_type'], exam_type.strip()) is not None

class InputSanitizer:
    """Input sanitization utilities"""
    
    @staticmethod
    def sanitize_string(value):
        """Sanitize string input"""
        if not isinstance(value, str):
            return str(value)
        # HTML escape
        sanitized = html.escape(value.strip())
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        return sanitized
    
    @staticmethod
    def sanitize_html(value):
        """Sanitize HTML content"""
        if not isinstance(value, str):
            return str(value)
        return bleach.clean(
            value,
            tags=ALLOWED_HTML_TAGS,
            attributes=ALLOWED_HTML_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename"""
        if not isinstance(filename, str):
            return 'file'
        # Remove path separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        sanitized = sanitized.strip('. ')
        return sanitized[:255] if sanitized else 'file'

def require_json(f):
    """Decorator to ensure request contains JSON data"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Request must contain JSON data'}), 400
        return f(*args, **kwargs)
    return decorated_function

def validate_request_data(required_fields=None, optional_fields=None, validators=None):
    """Decorator to validate request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            # Check required fields
            if required_fields:
                for field in required_fields:
                    if field not in data or not data[field]:
                        return jsonify({'error': f'Field "{field}" is required'}), 400
            
            # Validate fields
            if validators:
                for field, validator in validators.items():
                    if field in data:
                        if not validator(data[field]):
                            return jsonify({'error': f'Invalid value for field "{field}"'}), 400
            
            # Sanitize all string fields
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = InputSanitizer.sanitize_string(value)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_security_event(event_type, details=None, user_id=None):
    """Log security events"""
    logger = logging.getLogger('security')
    
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'ip_address': get_remote_address(),
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'user_id': user_id
    }
    
    if details:
        log_data['details'] = details
    
    logger.warning(f"Security Event: {log_data}")

def check_file_security(file):
    """Check uploaded file security"""
    if not file:
        raise SecurityError("No file provided")
    
    # Check file size (already handled by Flask's MAX_CONTENT_LENGTH)
    
    # Check filename
    if not file.filename:
        raise SecurityError("No filename provided")
    
    # Sanitize filename
    safe_filename = InputSanitizer.sanitize_filename(file.filename)
    if not safe_filename or safe_filename == 'file':
        raise SecurityError("Invalid filename")
    
    # Check file extension
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())
    if allowed_extensions:
        file_ext = safe_filename.rsplit('.', 1)[-1].lower() if '.' in safe_filename else ''
        if file_ext not in allowed_extensions:
            raise SecurityError(f"File type '{file_ext}' not allowed")
    
    return safe_filename

def setup_security_headers(app):
    """Setup security headers for the application"""
    
    @app.after_request
    def add_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (basic)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self' https:;"
        )
        
        return response

def setup_error_handlers(app):
    """Setup comprehensive error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        log_security_event('bad_request', {'error': str(error)})
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        log_security_event('unauthorized_access', {'error': str(error)})
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        log_security_event('forbidden_access', {'error': str(error)})
        return jsonify({
            'error': 'Forbidden',
            'message': 'Access denied'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(413)
    def payload_too_large(error):
        log_security_event('payload_too_large', {'error': str(error)})
        return jsonify({
            'error': 'Payload Too Large',
            'message': 'The uploaded file is too large'
        }), 413
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        log_security_event('rate_limit_exceeded', {'error': str(error)})
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        log_security_event('internal_error', {'error': str(error)})
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(SecurityError)
    def security_error(error):
        log_security_event('security_violation', {'error': str(error)})
        return jsonify({
            'error': 'Security Error',
            'message': str(error)
        }), 400

def init_security(app):
    """Initialize security features for the application"""
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Setup security headers
    setup_security_headers(app)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Setup security logging
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.WARNING)
    
    # Create file handler for security logs
    security_handler = logging.FileHandler('security.log')
    security_handler.setLevel(logging.WARNING)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    security_handler.setFormatter(formatter)
    
    # Add handler to logger
    security_logger.addHandler(security_handler)
    
    return limiter
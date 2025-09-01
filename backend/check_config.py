#!/usr/bin/env python3
"""
Check JWT configuration at runtime
"""

from app import create_app
import os

# Create app instance
app = create_app('development')

with app.app_context():
    print("=== JWT Configuration Check ===")
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV', 'not set')}")
    print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY', 'not set')[:20]}...")
    print(f"JWT_CSRF_PROTECT: {app.config.get('JWT_CSRF_PROTECT', 'not set')}")
    print(f"JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 'not set')}")
    print(f"DEBUG: {app.config.get('DEBUG', 'not set')}")
    print(f"SQLALCHEMY_ECHO: {app.config.get('SQLALCHEMY_ECHO', 'not set')}")
    
    # Check all JWT-related config keys
    print("\n=== All JWT Config Keys ===")
    jwt_keys = [key for key in app.config.keys() if 'JWT' in key]
    for key in sorted(jwt_keys):
        value = app.config[key]
        if 'SECRET' in key and isinstance(value, str):
            value = value[:20] + '...' if len(value) > 20 else value
        print(f"{key}: {value}")
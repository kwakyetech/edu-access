#!/usr/bin/env python3
"""
Decode JWT token to debug the issue
"""

import requests
import jwt
import json
from datetime import datetime

# Get token first
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})

print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"\nToken received: {token[:50]}...")
    
    # Try to decode the token without verification first
    try:
        decoded_unverified = jwt.decode(token, options={"verify_signature": False})
        print(f"\nDecoded token (unverified): {json.dumps(decoded_unverified, indent=2)}")
        
        # Check expiration
        exp_timestamp = decoded_unverified.get('exp')
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            current_datetime = datetime.now()
            print(f"\nToken expires at: {exp_datetime}")
            print(f"Current time: {current_datetime}")
            print(f"Token is {'expired' if current_datetime > exp_datetime else 'valid'}")
        
        # Try to decode with the secret key from config
        try:
            # Use the same secret key as in .env file
            secret_key = 'eduaccess-jwt-secret-key-change-in-production-2024'
            decoded_verified = jwt.decode(token, secret_key, algorithms=['HS256'])
            print(f"\nDecoded token (verified): {json.dumps(decoded_verified, indent=2)}")
        except jwt.InvalidTokenError as e:
            print(f"\nToken verification failed: {e}")
            
    except Exception as e:
        print(f"\nFailed to decode token: {e}")
else:
    print("Login failed")
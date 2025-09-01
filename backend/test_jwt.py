#!/usr/bin/env python3
"""
Test JWT token functionality
"""

import requests
import json

# Get token first
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})

print(f"Login status: {login_response.status_code}")
print(f"Login response: {login_response.text}")

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"\nToken received: {token[:50]}...")
    
    # Test profile endpoint (should work with JWT)
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\nTesting profile endpoint...")
    profile_response = requests.get('http://localhost:5000/api/auth/profile', 
                                  headers=headers)
    
    print(f"Profile status: {profile_response.status_code}")
    print(f"Profile response: {profile_response.text}")
    
    # Test notes endpoint (should work with JWT)
    print("\nTesting notes endpoint...")
    notes_response = requests.get('http://localhost:5000/api/notes/', 
                                headers=headers)
    
    print(f"Notes status: {notes_response.status_code}")
    print(f"Notes response: {notes_response.text}")
else:
    print("Login failed, cannot test JWT")
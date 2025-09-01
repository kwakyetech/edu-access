#!/usr/bin/env python3
"""
Debug script for file upload
"""

import requests
import json
from io import BytesIO

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
    
    # Test file upload
    headers = {'Authorization': f'Bearer {token}'}
    test_file = BytesIO(b"Test file content")
    files = {'file': ('test.txt', test_file, 'text/plain')}
    
    print("\nTesting file upload...")
    upload_response = requests.post('http://localhost:5000/api/files/upload', 
                                  headers=headers, files=files)
    
    print(f"Upload status: {upload_response.status_code}")
    print(f"Upload response: {upload_response.text}")
    
    # Test without file
    print("\nTesting without file...")
    no_file_response = requests.post('http://localhost:5000/api/files/upload', 
                                   headers=headers)
    print(f"No file status: {no_file_response.status_code}")
    print(f"No file response: {no_file_response.text}")
else:
    print("Login failed, cannot test upload")
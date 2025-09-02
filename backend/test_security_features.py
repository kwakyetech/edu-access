#!/usr/bin/env python3
"""
Test script for security features
"""

import requests
import json
import time
from io import BytesIO

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_EMAIL = 'security_test@example.com'
TEST_PASSWORD = 'SecurePass123!'

def test_rate_limiting():
    """Test rate limiting on authentication endpoints"""
    print("\n=== Testing Rate Limiting ===")
    
    # Test registration rate limiting (5 per minute)
    print("\n1. Testing registration rate limiting...")
    for i in range(7):  # Try 7 requests (should fail after 5)
        response = requests.post(f'{BASE_URL}/auth/register', json={
            'username': f'testuser{i}',
            'email': f'test{i}@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        })
        
        if response.status_code == 429:  # Rate limited
            print(f"✓ Request {i+1}: Rate limited (429) - Working correctly")
            break
        elif response.status_code in [200, 201, 400]:  # Success or validation error
            print(f"✓ Request {i+1}: {response.status_code}")
        else:
            print(f"✗ Request {i+1}: Unexpected status {response.status_code}")
    
    # Test login rate limiting (10 per minute)
    print("\n2. Testing login rate limiting...")
    for i in range(12):  # Try 12 requests (should fail after 10)
        response = requests.post(f'{BASE_URL}/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        
        if response.status_code == 429:  # Rate limited
            print(f"✓ Request {i+1}: Rate limited (429) - Working correctly")
            break
        elif response.status_code in [401, 400]:  # Invalid credentials
            print(f"✓ Request {i+1}: {response.status_code}")
        else:
            print(f"✗ Request {i+1}: Unexpected status {response.status_code}")

def test_input_validation():
    """Test input validation"""
    print("\n=== Testing Input Validation ===")
    
    # Test invalid email format
    print("\n1. Testing invalid email format...")
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    if response.status_code == 400:
        print("✓ Invalid email rejected correctly")
    else:
        print(f"✗ Invalid email not rejected: {response.status_code}")
    
    # Test weak password
    print("\n2. Testing weak password...")
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': '123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    if response.status_code == 400:
        print("✓ Weak password rejected correctly")
    else:
        print(f"✗ Weak password not rejected: {response.status_code}")
    
    # Test missing required fields
    print("\n3. Testing missing required fields...")
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'username': 'testuser3',
        'email': 'test3@example.com'
        # Missing password, first_name, last_name
    })
    
    if response.status_code == 400:
        print("✓ Missing fields rejected correctly")
    else:
        print(f"✗ Missing fields not rejected: {response.status_code}")

def test_file_upload_security():
    """Test file upload security"""
    print("\n=== Testing File Upload Security ===")
    
    # First, get a valid token
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    })
    
    if login_response.status_code != 200:
        print("✗ Could not login for file upload tests")
        return
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test malicious file extension
    print("\n1. Testing malicious file extension...")
    malicious_file = BytesIO(b"malicious content")
    files = {'file': ('malware.exe', malicious_file, 'application/octet-stream')}
    
    response = requests.post(f'{BASE_URL}/files/upload', headers=headers, files=files)
    
    if response.status_code == 400:
        print("✓ Malicious file extension rejected correctly")
    else:
        print(f"✗ Malicious file not rejected: {response.status_code}")
    
    # Test oversized file (if configured)
    print("\n2. Testing file size limits...")
    large_content = b"x" * (20 * 1024 * 1024)  # 20MB file
    large_file = BytesIO(large_content)
    files = {'file': ('large.txt', large_file, 'text/plain')}
    
    response = requests.post(f'{BASE_URL}/files/upload', headers=headers, files=files)
    
    if response.status_code in [400, 413]:  # Bad request or payload too large
        print("✓ Large file rejected correctly")
    else:
        print(f"✗ Large file not rejected: {response.status_code}")

def test_authentication_security():
    """Test authentication security features"""
    print("\n=== Testing Authentication Security ===")
    
    # Test accessing protected endpoint without token
    print("\n1. Testing access without authentication...")
    response = requests.get(f'{BASE_URL}/dashboard/overview')
    
    if response.status_code == 401:
        print("✓ Unauthorized access rejected correctly")
    else:
        print(f"✗ Unauthorized access not rejected: {response.status_code}")
    
    # Test with invalid token
    print("\n2. Testing access with invalid token...")
    headers = {'Authorization': 'Bearer invalid_token_here'}
    response = requests.get(f'{BASE_URL}/dashboard/overview', headers=headers)
    
    if response.status_code == 422:  # Unprocessable entity (invalid JWT)
        print("✓ Invalid token rejected correctly")
    else:
        print(f"✗ Invalid token not rejected: {response.status_code}")

def test_cors_headers():
    """Test CORS headers"""
    print("\n=== Testing CORS Headers ===")
    
    response = requests.options(f'{BASE_URL}/auth/login')
    
    if 'Access-Control-Allow-Origin' in response.headers:
        print("✓ CORS headers present")
        print(f"  Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    else:
        print("✗ CORS headers missing")

def test_security_headers():
    """Test security headers"""
    print("\n=== Testing Security Headers ===")
    
    response = requests.get(f'{BASE_URL}/health')
    
    security_headers = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection',
        'Strict-Transport-Security'
    ]
    
    for header in security_headers:
        if header in response.headers:
            print(f"✓ {header}: {response.headers[header]}")
        else:
            print(f"✗ {header}: Missing")

def register_test_user():
    """Register a test user for other tests"""
    print("\n=== Registering Test User ===")
    
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'username': 'securitytest',
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'first_name': 'Security',
        'last_name': 'Test'
    })
    
    if response.status_code in [200, 201]:
        print("✓ Test user registered successfully")
        return True
    elif response.status_code == 400 and 'already' in response.text.lower():
        print("✓ Test user already exists")
        return True
    else:
        print(f"✗ Failed to register test user: {response.status_code}")
        return False

def main():
    """Run all security tests"""
    print("🔒 Security Features Test Suite")
    print("=" * 50)
    
    # Register test user first
    if not register_test_user():
        print("❌ Cannot proceed without test user")
        return
    
    # Wait a moment to avoid rate limiting
    time.sleep(2)
    
    # Run all tests
    test_input_validation()
    time.sleep(2)
    
    test_authentication_security()
    time.sleep(2)
    
    test_file_upload_security()
    time.sleep(2)
    
    test_cors_headers()
    time.sleep(2)
    
    test_security_headers()
    time.sleep(2)
    
    # Rate limiting test last (as it may trigger limits)
    test_rate_limiting()
    
    print("\n🎉 Security tests completed!")
    print("\n⚠️  Note: Some tests may show failures if the server is not configured")
    print("   with all security features enabled. Check the implementation.")

if __name__ == '__main__':
    main()
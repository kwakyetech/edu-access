#!/usr/bin/env python3
"""
Test script for file upload functionality
"""

import requests
import json
import os
from io import BytesIO

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_EMAIL = 'john@example.com'
TEST_PASSWORD = 'password123'

def test_file_upload():
    """Test the complete file upload workflow"""
    
    print("=== Testing File Upload System ===")
    
    # Step 1: Login to get JWT token
    print("\n1. Logging in...")
    login_data = {
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print(f"✓ Login successful")
        else:
            print(f"✗ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"✗ Login error: {e}")
        return
    
    # Step 2: Create a test file
    print("\n2. Creating test file...")
    test_content = "This is a test file for upload functionality.\nCreated by test script."
    test_file = BytesIO(test_content.encode('utf-8'))
    test_file.name = 'test_upload.txt'
    
    # Step 3: Upload file
    print("\n3. Uploading file...")
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': ('test_upload.txt', test_file, 'text/plain')}
    
    try:
        response = requests.post(f'{BASE_URL}/files/upload', headers=headers, files=files)
        if response.status_code == 201:
            upload_result = response.json()
            filename = upload_result['data']['filename']
            print(f"✓ File uploaded successfully: {filename}")
            print(f"  - Original name: {upload_result['data']['original_filename']}")
            print(f"  - File type: {upload_result['data']['file_type']}")
            print(f"  - File size: {upload_result['data']['file_size']} bytes")
        else:
            print(f"✗ Upload failed: {response.text}")
            return
    except Exception as e:
        print(f"✗ Upload error: {e}")
        return
    
    # Step 4: List files
    print("\n4. Listing files...")
    try:
        response = requests.get(f'{BASE_URL}/files/list', headers=headers)
        if response.status_code == 200:
            files_list = response.json()['data']
            print(f"✓ Found {len(files_list)} files")
            for file_info in files_list:
                print(f"  - {file_info['filename']} ({file_info['file_type']}, {file_info['file_size']} bytes)")
        else:
            print(f"✗ List files failed: {response.text}")
    except Exception as e:
        print(f"✗ List files error: {e}")
    
    # Step 5: Get file info
    print("\n5. Getting file info...")
    try:
        response = requests.get(f'{BASE_URL}/files/info/{filename}')
        if response.status_code == 200:
            file_info = response.json()['data']
            print(f"✓ File info retrieved")
            print(f"  - Filename: {file_info['filename']}")
            print(f"  - Type: {file_info['file_type']}")
            print(f"  - Size: {file_info['file_size']} bytes")
        else:
            print(f"✗ Get file info failed: {response.text}")
    except Exception as e:
        print(f"✗ Get file info error: {e}")
    
    # Step 6: Download file
    print("\n6. Downloading file...")
    try:
        response = requests.get(f'{BASE_URL}/files/download/{filename}')
        if response.status_code == 200:
            downloaded_content = response.text
            print(f"✓ File downloaded successfully")
            print(f"  - Content preview: {downloaded_content[:50]}...")
        else:
            print(f"✗ Download failed: {response.text}")
    except Exception as e:
        print(f"✗ Download error: {e}")
    
    # Step 7: Delete file
    print("\n7. Deleting file...")
    try:
        response = requests.delete(f'{BASE_URL}/files/delete/{filename}', headers=headers)
        if response.status_code == 200:
            print(f"✓ File deleted successfully")
        else:
            print(f"✗ Delete failed: {response.text}")
    except Exception as e:
        print(f"✗ Delete error: {e}")
    
    print("\n=== File Upload Test Complete ===")

def test_file_validation():
    """Test file validation (file type, size limits)"""
    
    print("\n=== Testing File Validation ===")
    
    # Login first
    login_data = {
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
    except:
        print("✗ Could not login for validation tests")
        return
    
    # Test 1: Invalid file type
    print("\n1. Testing invalid file type...")
    invalid_file = BytesIO(b"fake executable content")
    files = {'file': ('test.exe', invalid_file, 'application/octet-stream')}
    
    try:
        response = requests.post(f'{BASE_URL}/files/upload', headers=headers, files=files)
        if response.status_code == 400:
            print("✓ Invalid file type correctly rejected")
        else:
            print(f"✗ Invalid file type not rejected: {response.status_code}")
    except Exception as e:
        print(f"✗ Validation test error: {e}")
    
    # Test 2: Empty file
    print("\n2. Testing empty file...")
    try:
        response = requests.post(f'{BASE_URL}/files/upload', headers=headers, files={})
        if response.status_code == 400:
            print("✓ Empty file request correctly rejected")
        else:
            print(f"✗ Empty file request not rejected: {response.status_code}")
    except Exception as e:
        print(f"✗ Empty file test error: {e}")
    
    print("\n=== File Validation Test Complete ===")

if __name__ == '__main__':
    # Test basic file upload functionality
    test_file_upload()
    
    # Test file validation
    test_file_validation()
    
    print("\n🎉 All tests completed!")
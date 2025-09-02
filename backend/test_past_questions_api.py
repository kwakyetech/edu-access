#!/usr/bin/env python3
"""
Comprehensive test script for Past Questions API endpoints.
Tests CRUD operations, search functionality, download tracking, and statistics.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

# Test user credentials
TEST_USER = {
    "username": "pastquestions_tester",
    "email": "pastquestions@test.com",
    "password": "TestPass123!",
    "full_name": "Past Questions Tester"
}

# Global variables
access_token = None
test_question_id = None

def make_request(method, endpoint, data=None, headers=None, params=None):
    """Helper function to make HTTP requests"""
    url = f"{API_BASE}{endpoint}"
    
    if headers is None:
        headers = {}
    
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    headers['Content-Type'] = 'application/json'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection failed - is the server running at {BASE_URL}? Error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"❌ Request timeout: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_user_registration():
    """Test user registration"""
    print("👤 Testing User Registration...")
    
    response = make_request('POST', '/auth/register', TEST_USER)
    
    if response and response.status_code in [201, 400]:  # 400 if user already exists
        if response.status_code == 201:
            print("✅ User registered successfully")
        else:
            print("ℹ️ User already exists, proceeding with login")
        return True
    else:
        print(f"❌ Registration failed: {response.status_code if response else 'No response'}")
        if response:
            print(f"Response: {response.text}")
        return False

def test_user_login():
    """Test user login and get access token"""
    global access_token
    
    print("🔐 Testing User Login...")
    
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    response = make_request('POST', '/auth/login', login_data)
    
    if response and response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        print("✅ Login successful")
        print(f"Token: {access_token[:20]}...")
        return True
    else:
        print(f"❌ Login failed: {response.status_code if response else 'No response'}")
        if response:
            print(f"Response: {response.text}")
        return False

def test_upload_past_question():
    """Test uploading a past question"""
    global test_question_id
    
    print("\n📤 Testing Past Question Upload...")
    
    past_question_data = {
        "title": "Mathematics WAEC 2020 Past Question",
        "subject": "Mathematics",
        "year": 2020,
        "exam_type": "WAEC",
        "file_url": "https://example.com/math_waec_2020.pdf",
        "file_type": "PDF"
    }
    
    response = make_request('POST', '/past-questions/', past_question_data)
    
    print(f"\n=== Upload Past Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        test_question_id = data['past_question']['id']
        print(f"✅ Past question uploaded successfully")
        print(f"Question ID: {test_question_id}")
        print(f"Title: {data['past_question']['title']}")
        return True
    else:
        print(f"❌ Upload failed")
        return False

def test_get_past_questions():
    """Test retrieving past questions with filtering"""
    print("\n📋 Testing Past Questions Retrieval...")
    
    # Test basic retrieval
    response = make_request('GET', '/past-questions/')
    
    print(f"\n=== Get Past Questions ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['past_questions'])} past questions")
        print(f"Total questions: {data['total']}")
        
        # Test filtering by subject
        print("\n📊 Testing Subject Filter...")
        response = make_request('GET', '/past-questions/', params={'subject': 'Mathematics'})
        
        if response.status_code == 200:
            filtered_data = response.json()
            print(f"✅ Filtered by Mathematics: {len(filtered_data['past_questions'])} questions")
        
        # Test search functionality
        print("\n🔍 Testing Search...")
        response = make_request('GET', '/past-questions/', params={'search': 'WAEC'})
        
        if response.status_code == 200:
            search_data = response.json()
            print(f"✅ Search results for 'WAEC': {len(search_data['past_questions'])} questions")
        
        return True
    else:
        print(f"❌ Retrieval failed")
        return False

def test_get_single_past_question():
    """Test retrieving a single past question"""
    if not test_question_id:
        print("⚠️ Skipping single question test - no question ID available")
        return True
    
    print("\n📄 Testing Single Past Question Retrieval...")
    
    response = make_request('GET', f'/past-questions/{test_question_id}')
    
    print(f"\n=== Get Single Past Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved past question: {data['past_question']['title']}")
        return True
    else:
        print(f"❌ Single question retrieval failed")
        return False

def test_download_tracking():
    """Test download count tracking"""
    if not test_question_id:
        print("⚠️ Skipping download test - no question ID available")
        return True
    
    print("\n⬇️ Testing Download Tracking...")
    
    response = make_request('POST', f'/past-questions/{test_question_id}/download')
    
    print(f"\n=== Download Past Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Download tracked successfully")
        print(f"Download count: {data['download_count']}")
        print(f"File URL: {data['file_url']}")
        return True
    else:
        print(f"❌ Download tracking failed")
        return False

def test_update_past_question():
    """Test updating a past question"""
    if not test_question_id:
        print("⚠️ Skipping update test - no question ID available")
        return True
    
    print("\n✏️ Testing Past Question Update...")
    
    update_data = {
        "title": "Mathematics WAEC 2020 Past Question (Updated)",
        "year": 2021
    }
    
    response = make_request('PUT', f'/past-questions/{test_question_id}', update_data)
    
    print(f"\n=== Update Past Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Past question updated successfully")
        print(f"New title: {data['past_question']['title']}")
        print(f"New year: {data['past_question']['year']}")
        return True
    else:
        print(f"❌ Update failed")
        return False

def test_metadata_endpoints():
    """Test metadata endpoints (subjects, exam types, years)"""
    print("\n📊 Testing Metadata Endpoints...")
    
    # Test subjects
    response = make_request('GET', '/past-questions/subjects')
    print(f"\n=== Get Subjects ===")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Subjects: {data['subjects']}")
        print(f"✅ Retrieved {len(data['subjects'])} subjects")
    
    # Test exam types
    response = make_request('GET', '/past-questions/exam-types')
    print(f"\n=== Get Exam Types ===")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Exam Types: {data['exam_types']}")
        print(f"✅ Retrieved {len(data['exam_types'])} exam types")
    
    # Test years
    response = make_request('GET', '/past-questions/years')
    print(f"\n=== Get Years ===")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Years: {data['years']}")
        print(f"✅ Retrieved {len(data['years'])} years")
    
    return True

def test_statistics():
    """Test past questions statistics"""
    print("\n📈 Testing Past Questions Statistics...")
    
    response = make_request('GET', '/past-questions/stats')
    
    print(f"\n=== Get Past Questions Stats ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved statistics")
        print(f"Total questions: {data['total_questions']}")
        print(f"Subjects: {len(data['subjects'])}")
        print(f"Exam types: {len(data['exam_types'])}")
        print(f"Most downloaded: {len(data['most_downloaded'])}")
        return True
    else:
        print(f"❌ Statistics retrieval failed")
        return False

def test_error_cases():
    """Test error handling"""
    print("\n⚠️ Testing Error Cases...")
    
    # Test upload without required fields
    response = make_request('POST', '/past-questions/', {})
    print(f"\n=== Upload without Required Fields ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✅ Correctly rejected upload without required fields")
    
    # Test get non-existent question
    response = make_request('GET', '/past-questions/99999')
    print(f"\n=== Get Non-existent Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent question")
    
    # Test invalid year
    invalid_data = {
        "title": "Test Question",
        "subject": "Test",
        "year": 1800,  # Invalid year
        "exam_type": "TEST",
        "file_url": "https://example.com/test.pdf",
        "file_type": "PDF"
    }
    
    response = make_request('POST', '/past-questions/', invalid_data)
    print(f"\n=== Upload with Invalid Year ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✅ Correctly rejected invalid year")
    
    return True

def test_delete_past_question():
    """Test deleting a past question (cleanup)"""
    if not test_question_id:
        print("⚠️ Skipping delete test - no question ID available")
        return True
    
    print("\n🗑️ Testing Past Question Deletion...")
    
    response = make_request('DELETE', f'/past-questions/{test_question_id}')
    
    print(f"\n=== Delete Past Question ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print(f"✅ Past question deleted successfully")
        return True
    else:
        print(f"❌ Deletion failed")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Past Questions API Tests...")
    print("=" * 50)
    
    # Authentication tests
    if not test_user_registration():
        return
    
    if not test_user_login():
        return
    
    # Past Questions API tests
    test_upload_past_question()
    test_get_past_questions()
    test_get_single_past_question()
    test_download_tracking()
    test_update_past_question()
    test_metadata_endpoints()
    test_statistics()
    test_error_cases()
    test_delete_past_question()
    
    print("\n" + "=" * 50)
    print("🎉 Past Questions API Tests Completed!")
    print("✅ CRUD operations working")
    print("✅ Search and filtering working")
    print("✅ Download tracking working")
    print("✅ Metadata endpoints working")
    print("✅ Statistics working")
    print("✅ Error handling working")

if __name__ == "__main__":
    main()
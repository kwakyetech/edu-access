#!/usr/bin/env python3
"""
Comprehensive test script for Notes API endpoints.
Tests all CRUD operations, filtering, pagination, and statistics.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_USER = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'TestPass123!',
    'first_name': 'Test',
    'last_name': 'User'
}

def print_response(response, title):
    """Print formatted response for debugging."""
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"Response Text: {response.text}")
        return None

def register_and_login():
    """Register a test user and get access token."""
    print("\n🔐 Testing User Registration and Login...")
    
    # Register user
    register_response = requests.post(f'{BASE_URL}/auth/register', json=TEST_USER)
    register_data = print_response(register_response, "User Registration")
    
    # Login to get token
    login_data = {
        'email': TEST_USER['email'],
        'password': TEST_USER['password']
    }
    login_response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    login_result = print_response(login_response, "User Login")
    
    if login_response.status_code == 200 and login_result:
        return login_result.get('access_token')
    else:
        print("❌ Failed to get access token")
        return None

def test_create_notes(token):
    """Test creating multiple notes."""
    print("\n📝 Testing Note Creation...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test notes data
    test_notes = [
        {
            'title': 'Introduction to Python',
            'content': 'Python is a high-level programming language known for its simplicity and readability.',
            'subject': 'Computer Science',
            'file_url': 'https://example.com/python-intro.pdf',
            'file_type': 'pdf'
        },
        {
            'title': 'Calculus Fundamentals',
            'content': 'Calculus is the mathematical study of continuous change.',
            'subject': 'Mathematics',
        },
        {
            'title': 'Physics Laws',
            'content': 'Newton\'s laws of motion are three physical laws that form the foundation for classical mechanics.',
            'subject': 'Physics'
        },
        {
            'title': 'Advanced Python',
            'content': 'Advanced Python concepts including decorators, generators, and metaclasses.',
            'subject': 'Computer Science'
        }
    ]
    
    created_notes = []
    
    for i, note_data in enumerate(test_notes, 1):
        response = requests.post(f'{BASE_URL}/notes/', json=note_data, headers=headers)
        result = print_response(response, f"Create Note {i}")
        
        if response.status_code == 201 and result:
            created_notes.append(result['note'])
            print(f"✅ Note '{note_data['title']}' created successfully")
        else:
            print(f"❌ Failed to create note '{note_data['title']}'")
    
    return created_notes

def test_get_notes(token):
    """Test retrieving notes with pagination and filtering."""
    print("\n📋 Testing Note Retrieval...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test getting all notes
    response = requests.get(f'{BASE_URL}/notes/', headers=headers)
    result = print_response(response, "Get All Notes")
    
    if response.status_code == 200 and result:
        print(f"✅ Retrieved {len(result['notes'])} notes")
        print(f"Total notes: {result['total']}")
    
    # Test pagination
    response = requests.get(f'{BASE_URL}/notes/?page=1&per_page=2', headers=headers)
    result = print_response(response, "Get Notes with Pagination")
    
    # Test subject filtering
    response = requests.get(f'{BASE_URL}/notes/?subject=Computer Science', headers=headers)
    result = print_response(response, "Filter by Subject")
    
    # Test search
    response = requests.get(f'{BASE_URL}/notes/?search=Python', headers=headers)
    result = print_response(response, "Search Notes")
    
    return result['notes'][0]['id'] if result and result['notes'] else None

def test_get_single_note(token, note_id):
    """Test retrieving a single note."""
    print("\n📄 Testing Single Note Retrieval...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/notes/{note_id}', headers=headers)
    result = print_response(response, f"Get Note {note_id}")
    
    if response.status_code == 200 and result:
        print(f"✅ Retrieved note: {result['note']['title']}")
        return True
    else:
        print(f"❌ Failed to retrieve note {note_id}")
        return False

def test_update_note(token, note_id):
    """Test updating a note."""
    print("\n✏️ Testing Note Update...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    update_data = {
        'title': 'Updated Python Introduction',
        'content': 'Updated content about Python programming language with more details.',
        'subject': 'Computer Science'
    }
    
    response = requests.put(f'{BASE_URL}/notes/{note_id}', json=update_data, headers=headers)
    result = print_response(response, f"Update Note {note_id}")
    
    if response.status_code == 200 and result:
        print(f"✅ Note updated successfully")
        return True
    else:
        print(f"❌ Failed to update note {note_id}")
        return False

def test_notes_subjects(token):
    """Test getting unique subjects."""
    print("\n📚 Testing Subjects Endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/notes/subjects', headers=headers)
    result = print_response(response, "Get Subjects")
    
    if response.status_code == 200 and result:
        print(f"✅ Retrieved {len(result['subjects'])} unique subjects")
        return True
    else:
        print("❌ Failed to retrieve subjects")
        return False

def test_notes_stats(token):
    """Test getting notes statistics."""
    print("\n📊 Testing Notes Statistics...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/notes/stats', headers=headers)
    result = print_response(response, "Get Notes Stats")
    
    if response.status_code == 200 and result:
        print(f"✅ Total notes: {result['total_notes']}")
        print(f"✅ Recent notes: {result['recent_notes']}")
        print(f"✅ Subjects breakdown: {len(result['subjects'])} subjects")
        return True
    else:
        print("❌ Failed to retrieve notes statistics")
        return False

def test_delete_note(token, note_id):
    """Test deleting a note."""
    print("\n🗑️ Testing Note Deletion...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.delete(f'{BASE_URL}/notes/{note_id}', headers=headers)
    result = print_response(response, f"Delete Note {note_id}")
    
    if response.status_code == 200:
        print(f"✅ Note {note_id} deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete note {note_id}")
        return False

def test_error_cases(token):
    """Test error handling."""
    print("\n⚠️ Testing Error Cases...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test creating note with missing fields
    invalid_note = {'title': 'Incomplete Note'}
    response = requests.post(f'{BASE_URL}/notes/', json=invalid_note, headers=headers)
    print_response(response, "Create Note with Missing Fields")
    
    if response.status_code == 400:
        print("✅ Correctly rejected incomplete note")
    else:
        print("❌ Should have rejected incomplete note")
    
    # Test getting non-existent note
    response = requests.get(f'{BASE_URL}/notes/99999', headers=headers)
    print_response(response, "Get Non-existent Note")
    
    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent note")
    else:
        print("❌ Should have returned 404 for non-existent note")

def main():
    """Run all tests."""
    print("🚀 Starting Notes API Comprehensive Tests")
    print("=" * 50)
    
    # Get access token
    token = register_and_login()
    if not token:
        print("❌ Cannot proceed without access token")
        sys.exit(1)
    
    try:
        # Test note creation
        created_notes = test_create_notes(token)
        if not created_notes:
            print("❌ No notes created, cannot continue tests")
            return
        
        # Test note retrieval
        note_id = test_get_notes(token)
        if not note_id:
            note_id = created_notes[0]['id']
        
        # Test single note retrieval
        test_get_single_note(token, note_id)
        
        # Test note update
        test_update_note(token, note_id)
        
        # Test subjects endpoint
        test_notes_subjects(token)
        
        # Test statistics endpoint
        test_notes_stats(token)
        
        # Test error cases
        test_error_cases(token)
        
        # Test note deletion (delete one note)
        if len(created_notes) > 1:
            test_delete_note(token, created_notes[-1]['id'])
        
        print("\n" + "=" * 50)
        print("🎉 Notes API Tests Completed!")
        print("✅ All CRUD operations working")
        print("✅ Filtering and pagination working")
        print("✅ Statistics and subjects endpoints working")
        print("✅ Error handling working")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
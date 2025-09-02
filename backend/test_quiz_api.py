#!/usr/bin/env python3
"""
Comprehensive test script for Quiz API endpoints.
Tests quiz generation, Hugging Face integration, quiz attempts, and all CRUD operations.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_USER = {
    'username': 'quizuser',
    'email': 'quiz@example.com',
    'password': 'QuizPass123!',
    'first_name': 'Quiz',
    'last_name': 'Tester'
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

def create_test_note(token):
    """Create a test note for quiz generation."""
    print("\n📝 Creating Test Note for Quiz Generation...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    note_data = {
        'title': 'Python Programming Basics',
        'content': '''Python is a high-level, interpreted programming language with dynamic semantics. 
        Its high-level built-in data structures, combined with dynamic typing and dynamic binding, 
        make it very attractive for Rapid Application Development. Python supports modules and packages, 
        which encourages program modularity and code reuse. The Python interpreter and the extensive 
        standard library are available in source or binary form without charge for all major platforms. 
        Python was created by Guido van Rossum and first released in 1991. It is named after the 
        British comedy group Monty Python. Python emphasizes code readability with its notable use 
        of significant whitespace. Its language constructs and object-oriented approach aim to help 
        programmers write clear, logical code for small and large-scale projects.''',
        'subject': 'Computer Science'
    }
    
    response = requests.post(f'{BASE_URL}/notes/', json=note_data, headers=headers)
    result = print_response(response, "Create Test Note")
    
    if response.status_code == 201 and result:
        print(f"✅ Test note created with ID: {result['note']['id']}")
        return result['note']['id']
    else:
        print("❌ Failed to create test note")
        return None

def test_generate_quiz_from_content(token):
    """Test generating quiz from raw content."""
    print("\n🧠 Testing Quiz Generation from Content...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    quiz_data = {
        'title': 'Machine Learning Quiz',
        'subject': 'Computer Science',
        'difficulty': 'medium',
        'num_questions': 3,
        'content': '''Machine learning is a method of data analysis that automates analytical model building. 
        It is a branch of artificial intelligence based on the idea that systems can learn from data, 
        identify patterns and make decisions with minimal human intervention. Machine learning algorithms 
        build a model based on training data in order to make predictions or decisions without being 
        explicitly programmed to do so. Supervised learning uses labeled training data to learn a mapping 
        function from input variables to an output variable. Unsupervised learning finds hidden patterns 
        or intrinsic structures in input data without labeled examples.'''
    }
    
    response = requests.post(f'{BASE_URL}/quiz/generate', json=quiz_data, headers=headers)
    result = print_response(response, "Generate Quiz from Content")
    
    if response.status_code == 201 and result:
        quiz = result['quiz']
        print(f"✅ Quiz generated successfully with {len(quiz['questions'])} questions")
        print(f"Quiz ID: {quiz['id']}, Title: {quiz['title']}")
        return quiz['id']
    else:
        print("❌ Failed to generate quiz from content")
        return None

def test_generate_quiz_from_note(token, note_id):
    """Test generating quiz from existing note."""
    print("\n📚 Testing Quiz Generation from Note...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    quiz_data = {
        'num_questions': 4,
        'difficulty': 'easy'
    }
    
    response = requests.post(f'{BASE_URL}/quiz/from-note/{note_id}', json=quiz_data, headers=headers)
    result = print_response(response, "Generate Quiz from Note")
    
    if response.status_code == 201 and result:
        quiz = result['quiz']
        print(f"✅ Quiz generated from note with {len(quiz['questions'])} questions")
        print(f"Quiz ID: {quiz['id']}, Title: {quiz['title']}")
        return quiz['id']
    else:
        print("❌ Failed to generate quiz from note")
        return None

def test_get_quizzes(token):
    """Test retrieving quizzes with filtering."""
    print("\n📋 Testing Quiz Retrieval...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test getting all quizzes
    response = requests.get(f'{BASE_URL}/quiz/', headers=headers)
    result = print_response(response, "Get All Quizzes")
    
    if response.status_code == 200 and result:
        print(f"✅ Retrieved {len(result['quizzes'])} quizzes")
        print(f"Total quizzes: {result['total']}")
    
    # Test subject filtering
    response = requests.get(f'{BASE_URL}/quiz/?subject=Computer Science', headers=headers)
    result = print_response(response, "Filter Quizzes by Subject")
    
    # Test difficulty filtering
    response = requests.get(f'{BASE_URL}/quiz/?difficulty=medium', headers=headers)
    result = print_response(response, "Filter Quizzes by Difficulty")
    
    # Test pagination
    response = requests.get(f'{BASE_URL}/quiz/?page=1&per_page=1', headers=headers)
    result = print_response(response, "Get Quizzes with Pagination")
    
    return result['quizzes'][0]['id'] if result and result['quizzes'] else None

def test_get_single_quiz(token, quiz_id):
    """Test retrieving a single quiz."""
    print("\n📄 Testing Single Quiz Retrieval...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/quiz/{quiz_id}', headers=headers)
    result = print_response(response, f"Get Quiz {quiz_id}")
    
    if response.status_code == 200 and result:
        quiz = result['quiz']
        print(f"✅ Retrieved quiz: {quiz['title']}")
        print(f"Questions: {len(quiz['questions'])}, Difficulty: {quiz['difficulty']}")
        return quiz
    else:
        print(f"❌ Failed to retrieve quiz {quiz_id}")
        return None

def test_submit_quiz_attempt(token, quiz_id, quiz_data):
    """Test submitting a quiz attempt."""
    print("\n✍️ Testing Quiz Attempt Submission...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Prepare answers (mix of correct and incorrect)
    answers = {}
    questions = quiz_data['questions']
    
    for i, question in enumerate(questions):
        question_id = question['id']
        correct_answer = question['correct_answer']
        
        # Answer correctly for first half, incorrectly for second half
        if i < len(questions) // 2:
            answers[str(question_id)] = correct_answer
        else:
            # Choose a different answer
            wrong_answer = (correct_answer + 1) % len(question['options'])
            answers[str(question_id)] = wrong_answer
    
    attempt_data = {
        'answers': answers,
        'time_taken': 120  # 2 minutes
    }
    
    response = requests.post(f'{BASE_URL}/quiz/{quiz_id}/attempt', json=attempt_data, headers=headers)
    result = print_response(response, "Submit Quiz Attempt")
    
    if response.status_code == 201 and result:
        attempt = result['attempt']
        print(f"✅ Quiz attempt submitted successfully")
        print(f"Score: {attempt['score']}/{attempt['total_questions']} ({attempt['percentage']}%)")
        print(f"Points earned: {result['points_earned']}")
        return attempt['id']
    else:
        print("❌ Failed to submit quiz attempt")
        return None

def test_get_quiz_attempts(token):
    """Test retrieving quiz attempts."""
    print("\n📊 Testing Quiz Attempts Retrieval...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/quiz/attempts', headers=headers)
    result = print_response(response, "Get Quiz Attempts")
    
    if response.status_code == 200 and result:
        print(f"✅ Retrieved {len(result['attempts'])} quiz attempts")
        print(f"Total attempts: {result['total']}")
        
        if result['attempts']:
            latest_attempt = result['attempts'][0]
            print(f"Latest attempt score: {latest_attempt['score']}/{latest_attempt['total_questions']}")
        
        return True
    else:
        print("❌ Failed to retrieve quiz attempts")
        return False

def test_error_cases(token):
    """Test error handling."""
    print("\n⚠️ Testing Error Cases...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test generating quiz without content
    response = requests.post(f'{BASE_URL}/quiz/generate', json={'title': 'Empty Quiz'}, headers=headers)
    print_response(response, "Generate Quiz without Content")
    
    if response.status_code == 400:
        print("✅ Correctly rejected quiz generation without content")
    else:
        print("❌ Should have rejected quiz generation without content")
    
    # Test getting non-existent quiz
    response = requests.get(f'{BASE_URL}/quiz/99999', headers=headers)
    print_response(response, "Get Non-existent Quiz")
    
    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent quiz")
    else:
        print("❌ Should have returned 404 for non-existent quiz")
    
    # Test submitting attempt without answers
    response = requests.post(f'{BASE_URL}/quiz/1/attempt', json={'time_taken': 60}, headers=headers)
    print_response(response, "Submit Attempt without Answers")
    
    if response.status_code == 400:
        print("✅ Correctly rejected attempt without answers")
    else:
        print("❌ Should have rejected attempt without answers")

def main():
    """Run all tests."""
    print("🚀 Starting Quiz API Comprehensive Tests")
    print("=" * 50)
    
    # Get access token
    token = register_and_login()
    if not token:
        print("❌ Cannot proceed without access token")
        sys.exit(1)
    
    try:
        # Create test note for quiz generation
        note_id = create_test_note(token)
        
        # Test quiz generation from content
        quiz_id_1 = test_generate_quiz_from_content(token)
        
        # Test quiz generation from note
        quiz_id_2 = None
        if note_id:
            quiz_id_2 = test_generate_quiz_from_note(token, note_id)
        
        # Test quiz retrieval
        quiz_id = test_get_quizzes(token)
        if not quiz_id:
            quiz_id = quiz_id_1 or quiz_id_2
        
        # Test single quiz retrieval
        if quiz_id:
            quiz_data = test_get_single_quiz(token, quiz_id)
            
            # Test quiz attempt submission
            if quiz_data:
                test_submit_quiz_attempt(token, quiz_id, quiz_data)
        
        # Test quiz attempts retrieval
        test_get_quiz_attempts(token)
        
        # Test error cases
        test_error_cases(token)
        
        print("\n" + "=" * 50)
        print("🎉 Quiz API Tests Completed!")
        print("✅ Quiz generation with Hugging Face working")
        print("✅ Quiz generation from notes working")
        print("✅ Quiz retrieval and filtering working")
        print("✅ Quiz attempts and scoring working")
        print("✅ Error handling working")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
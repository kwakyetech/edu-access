#!/usr/bin/env python3
"""
Test script for Leaderboard and Dashboard API endpoints
"""

import requests
import json
import time
from requests.exceptions import ConnectionError, Timeout

BASE_URL = "http://localhost:5000/api"

def make_request(method, url, **kwargs):
    """Make HTTP request with error handling and timeout"""
    try:
        kwargs['timeout'] = 10  # 10 second timeout
        response = getattr(requests, method.lower())(url, **kwargs)
        return response
    except ConnectionError:
        print(f"❌ Connection error for {method} {url}")
        return None
    except Timeout:
        print(f"❌ Timeout error for {method} {url}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error for {method} {url}: {e}")
        return None

def test_user_registration_and_login():
    """Test user registration and login"""
    print("\n=== Testing User Registration and Login ===")
    
    # Register a test user
    register_data = {
        "username": "testuser_leaderboard",
        "email": "testuser_leaderboard@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = make_request('POST', f"{BASE_URL}/auth/register", json=register_data)
    if not response:
        print("❌ No response from registration")
        return None
    
    if response.status_code == 201:
        print("✅ User registered successfully")
    elif response.status_code == 400 and "already exists" in response.text:
        print("ℹ️ User already exists, proceeding with login")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
        return None
    
    # Login
    login_data = {
        "username": "testuser_leaderboard",
        "password": "testpassword123"
    }
    
    response = make_request('POST', f"{BASE_URL}/auth/login", json=login_data)
    if not response:
        print("❌ No response from login")
        return None
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_leaderboard_endpoints(token):
    """Test all leaderboard endpoints"""
    print("\n=== Testing Leaderboard Endpoints ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get leaderboard
    print("\n--- Testing GET /leaderboard ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Leaderboard retrieved: {len(data.get('leaderboard', []))} entries")
        print(f"   Page: {data.get('page', 'N/A')}, Total Pages: {data.get('total_pages', 'N/A')}")
    else:
        print(f"❌ Failed to get leaderboard: {response.status_code if response else 'No response'}")
    
    # Test get top users
    print("\n--- Testing GET /leaderboard/top ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard/top?limit=5", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Top users retrieved: {len(data.get('top_users', []))} users")
    else:
        print(f"❌ Failed to get top users: {response.status_code if response else 'No response'}")
    
    # Test get user rank by ID (using user ID 1)
    print("\n--- Testing GET /leaderboard/user/1 ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard/user/1", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ User rank retrieved: Rank {data.get('rank', 'N/A')}")
    else:
        print(f"❌ Failed to get user rank: {response.status_code if response else 'No response'}")
    
    # Test get my rank
    print("\n--- Testing GET /leaderboard/my_rank ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard/my_rank", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ My rank retrieved: Rank {data.get('rank', 'N/A')}")
        print(f"   Nearby users: {len(data.get('nearby_users', []))} users")
    else:
        print(f"❌ Failed to get my rank: {response.status_code if response else 'No response'}")
    
    # Test leaderboard stats
    print("\n--- Testing GET /leaderboard/stats ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard/stats", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Leaderboard stats retrieved")
        print(f"   Total users: {data.get('total_users', 'N/A')}")
        print(f"   Average points: {data.get('average_points', 'N/A')}")
    else:
        print(f"❌ Failed to get leaderboard stats: {response.status_code if response else 'No response'}")
    
    # Test refresh leaderboard
    print("\n--- Testing POST /leaderboard/refresh ---")
    response = make_request('POST', f"{BASE_URL}/leaderboard/refresh", headers=headers)
    if response and response.status_code == 200:
        print("✅ Leaderboard refreshed successfully")
    else:
        print(f"❌ Failed to refresh leaderboard: {response.status_code if response else 'No response'}")
    
    # Test subject-specific leaderboard (should return not implemented)
    print("\n--- Testing GET /leaderboard/subject/mathematics ---")
    response = make_request('GET', f"{BASE_URL}/leaderboard/subject/mathematics", headers=headers)
    if response and response.status_code == 501:
        print("✅ Subject leaderboard correctly returns 'Not Implemented'")
    else:
        print(f"❌ Unexpected response for subject leaderboard: {response.status_code if response else 'No response'}")

def test_dashboard_endpoints(token):
    """Test all dashboard endpoints"""
    print("\n=== Testing Dashboard Endpoints ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test dashboard overview
    print("\n--- Testing GET /dashboard/overview ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/overview", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print("✅ Dashboard overview retrieved")
        print(f"   User: {data.get('user_info', {}).get('username', 'N/A')}")
        print(f"   Points: {data.get('user_info', {}).get('points', 'N/A')}")
        print(f"   Total notes: {data.get('stats', {}).get('total_notes', 'N/A')}")
        print(f"   Total quiz attempts: {data.get('stats', {}).get('total_quiz_attempts', 'N/A')}")
    else:
        print(f"❌ Failed to get dashboard overview: {response.status_code if response else 'No response'}")
    
    # Test activity timeline
    print("\n--- Testing GET /dashboard/activity ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/activity?days=7", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Activity timeline retrieved: {len(data.get('activity_timeline', []))} days")
        print(f"   Period: {data.get('period_days', 'N/A')} days")
    else:
        print(f"❌ Failed to get activity timeline: {response.status_code if response else 'No response'}")
    
    # Test quiz performance
    print("\n--- Testing GET /dashboard/quiz-performance ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/quiz-performance", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        perf = data.get('quiz_performance', {})
        print("✅ Quiz performance retrieved")
        print(f"   Total attempts: {perf.get('total_attempts', 'N/A')}")
        print(f"   Average score: {perf.get('average_score', 'N/A')}%")
        print(f"   Best score: {perf.get('best_score', 'N/A')}%")
    else:
        print(f"❌ Failed to get quiz performance: {response.status_code if response else 'No response'}")
    
    # Test notes analytics
    print("\n--- Testing GET /dashboard/notes-analytics ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/notes-analytics", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        analytics = data.get('notes_analytics', {})
        print("✅ Notes analytics retrieved")
        print(f"   Total notes: {analytics.get('total_notes', 'N/A')}")
        print(f"   Subjects: {len(analytics.get('subjects', []))} different subjects")
    else:
        print(f"❌ Failed to get notes analytics: {response.status_code if response else 'No response'}")
    
    # Test achievements
    print("\n--- Testing GET /dashboard/achievements ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/achievements", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Achievements retrieved: {data.get('total_earned', 0)} earned")
        for achievement in data.get('achievements', [])[:3]:  # Show first 3
            print(f"   {achievement.get('icon', '')} {achievement.get('title', 'N/A')}")
    else:
        print(f"❌ Failed to get achievements: {response.status_code if response else 'No response'}")
    
    # Test goals
    print("\n--- Testing GET /dashboard/goals ---")
    response = make_request('GET', f"{BASE_URL}/dashboard/goals", headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        print(f"✅ Goals retrieved: {len(data.get('goals', []))} goals")
        for goal in data.get('goals', []):
            print(f"   {goal.get('title', 'N/A')}: {goal.get('progress', 0):.1f}% complete")
    else:
        print(f"❌ Failed to get goals: {response.status_code if response else 'No response'}")

def main():
    """Main test function"""
    print("🚀 Starting Leaderboard and Dashboard API Tests")
    print("=" * 50)
    
    # Test user registration and login
    token = test_user_registration_and_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test leaderboard endpoints
    test_leaderboard_endpoints(token)
    
    # Test dashboard endpoints
    test_dashboard_endpoints(token)
    
    print("\n" + "=" * 50)
    print("🏁 Leaderboard and Dashboard API Tests Completed")

if __name__ == "__main__":
    main()
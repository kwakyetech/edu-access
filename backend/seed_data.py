#!/usr/bin/env python3
"""
Seed data script for EduAccess backend.
This script populates the database with sample data for testing and demonstration.
"""

import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Note, Quiz, QuizAttempt, PastQuestion, Leaderboard
from config import config

def create_sample_users():
    """Create sample users"""
    print("Creating sample users...")
    
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@eduaccess.com',
            'password': 'Admin123!',
            'first_name': 'Admin',
            'last_name': 'User'
        },
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'Password123!',
            'first_name': 'John',
            'last_name': 'Doe'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'Password123!',
            'first_name': 'Jane',
            'last_name': 'Smith'
        },
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'password': 'Student123!',
            'first_name': 'Alice',
            'last_name': 'Johnson'
        },
        {
            'username': 'student2',
            'email': 'student2@example.com',
            'password': 'Student123!',
            'first_name': 'Bob',
            'last_name': 'Wilson'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            print(f"User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
            
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            created_at=datetime.utcnow()
        )
        
        db.session.add(user)
        created_users.append(user)
        print(f"Created user: {user_data['email']}")
    
    db.session.commit()
    return created_users

def create_sample_notes(users):
    """Create sample notes"""
    print("Creating sample notes...")
    
    notes_data = [
        {
            'title': 'Introduction to Python Programming',
            'content': 'Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development.',
            'subject': 'Computer Science',
            'user_id': 1
        },
        {
            'title': 'Calculus Fundamentals',
            'content': 'Calculus is the mathematical study of continuous change. It has two major branches: differential calculus (concerning rates of change and slopes of curves) and integral calculus (concerning accumulation of quantities and areas under curves).',
            'subject': 'Mathematics',
            'user_id': 2
        },
        {
            'title': 'World War II Overview',
            'content': 'World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world\'s countries and was the most widespread war in history.',
            'subject': 'History',
            'user_id': 3
        },
        {
            'title': 'Cell Biology Basics',
            'content': 'Cell biology is a branch of biology studying the structure and function of the cell, the basic unit of life. Cells are the fundamental working units of every living system.',
            'subject': 'Biology',
            'user_id': 4
        },
        {
            'title': 'JavaScript ES6 Features',
            'content': 'ES6 introduced many new features including arrow functions, template literals, destructuring, classes, modules, and promises that make JavaScript more powerful and easier to work with.',
            'subject': 'Computer Science',
            'user_id': 1
        }
    ]
    
    created_notes = []
    for note_data in notes_data:
        note = Note(
            title=note_data['title'],
            content=note_data['content'],
            subject=note_data['subject'],
            user_id=note_data['user_id'],
            created_at=datetime.utcnow() - timedelta(days=note_data.get('days_ago', 0))
        )
        
        db.session.add(note)
        created_notes.append(note)
        print(f"Created note: {note_data['title']}")
    
    db.session.commit()
    return created_notes

def create_sample_past_questions(users):
    """Create sample past questions"""
    print("Creating sample past questions...")
    
    questions_data = [
        {
            'title': 'Computer Science Final Exam 2023',
            'subject': 'Computer Science',
            'exam_type': 'Final Exam',
            'year': 2023,
            'file_url': '/uploads/cs_final_2023.pdf',
            'user_id': 1
        },
        {
            'title': 'Mathematics Midterm 2023',
            'subject': 'Mathematics',
            'exam_type': 'Midterm',
            'year': 2023,
            'file_url': '/uploads/math_midterm_2023.pdf',
            'user_id': 2
        },
        {
            'title': 'Biology Quiz 2023',
            'subject': 'Biology',
            'exam_type': 'Quiz',
            'year': 2023,
            'file_url': '/uploads/bio_quiz_2023.pdf',
            'user_id': 3
        },
        {
            'title': 'History Essay Questions 2022',
            'subject': 'History',
            'exam_type': 'Essay',
            'year': 2022,
            'file_url': '/uploads/history_essay_2022.pdf',
            'user_id': 4
        }
    ]
    
    created_questions = []
    for question_data in questions_data:
        question = PastQuestion(
            title=question_data['title'],
            subject=question_data['subject'],
            exam_type=question_data['exam_type'],
            year=question_data['year'],
            file_url=question_data['file_url'],
            file_type='pdf',
            uploaded_by=question_data['user_id'],
            created_at=datetime.utcnow() - timedelta(days=question_data.get('days_ago', 0))
        )
        
        db.session.add(question)
        created_questions.append(question)
        print(f"Created past question: {question_data['title']}")
    
    db.session.commit()
    return created_questions

def create_sample_quizzes(users):
    """Create sample quizzes"""
    print("Creating sample quizzes...")
    
    quizzes_data = [
        {
            'title': 'Python Basics Quiz',
            'subject': 'Computer Science',
            'questions': [
                {
                    'question': 'What is Python?',
                    'options': ['A snake', 'A programming language', 'A web browser', 'An operating system'],
                    'correct_answer': 1
                },
                {
                    'question': 'Which of the following is used to define a function in Python?',
                    'options': ['function', 'def', 'define', 'func'],
                    'correct_answer': 1
                }
            ],
            'user_id': 1
        },
        {
            'title': 'Basic Mathematics Quiz',
            'subject': 'Mathematics',
            'questions': [
                {
                    'question': 'What is 2 + 2?',
                    'options': ['3', '4', '5', '6'],
                    'correct_answer': 1
                },
                {
                    'question': 'What is the square root of 16?',
                    'options': ['2', '4', '6', '8'],
                    'correct_answer': 1
                }
            ],
            'user_id': 2
        }
    ]
    
    created_quizzes = []
    for quiz_data in quizzes_data:
        quiz = Quiz(
            title=quiz_data['title'],
            subject=quiz_data['subject'],
            questions=quiz_data['questions'],
            created_by=quiz_data['user_id'],
            created_at=datetime.utcnow() - timedelta(days=quiz_data.get('days_ago', 0))
        )
        
        db.session.add(quiz)
        created_quizzes.append(quiz)
        print(f"Created quiz: {quiz_data['title']}")
    
    db.session.commit()
    return created_quizzes

def create_sample_quiz_attempts(users, quizzes):
    """Create sample quiz attempts"""
    print("Creating sample quiz attempts...")
    
    attempts_data = [
        {
            'quiz_id': 1,
            'user_id': 2,
            'score': 85,
            'total_questions': 2,
            'answers': [1, 1],
            'days_ago': 5
        },
        {
            'quiz_id': 1,
            'user_id': 3,
            'score': 100,
            'total_questions': 2,
            'answers': [1, 1],
            'days_ago': 3
        },
        {
            'quiz_id': 2,
            'user_id': 1,
            'score': 100,
            'total_questions': 2,
            'answers': [1, 1],
            'days_ago': 2
        }
    ]
    
    created_attempts = []
    for attempt_data in attempts_data:
        attempt = QuizAttempt(
            quiz_id=attempt_data['quiz_id'],
            user_id=attempt_data['user_id'],
            score=attempt_data['score'],
            total_questions=attempt_data['total_questions'],
            answers=attempt_data['answers'],
            completed_at=datetime.utcnow() - timedelta(days=attempt_data['days_ago'])
        )
        
        db.session.add(attempt)
        created_attempts.append(attempt)
        print(f"Created quiz attempt: User {attempt_data['user_id']} -> Quiz {attempt_data['quiz_id']}")
    
    db.session.commit()
    return created_attempts

def create_sample_leaderboard(users, quiz_attempts):
    """Create sample leaderboard entries"""
    print("Creating sample leaderboard entries...")
    
    leaderboard_data = [
        {'user_id': 1, 'total_points': 100, 'quizzes_completed': 1, 'average_score': 100.0},
        {'user_id': 2, 'total_points': 85, 'quizzes_completed': 1, 'average_score': 85.0},
        {'user_id': 3, 'total_points': 100, 'quizzes_completed': 1, 'average_score': 100.0},
        {'user_id': 4, 'total_points': 0, 'quizzes_completed': 0, 'average_score': 0.0},
        {'user_id': 5, 'total_points': 0, 'quizzes_completed': 0, 'average_score': 0.0}
    ]
    
    created_entries = []
    for entry_data in leaderboard_data:
        # Check if entry already exists
        existing_entry = Leaderboard.query.filter_by(user_id=entry_data['user_id']).first()
        if existing_entry:
            print(f"Leaderboard entry for user {entry_data['user_id']} already exists, updating...")
            existing_entry.total_points = entry_data['total_points']
            existing_entry.quizzes_completed = entry_data['quizzes_completed']
            existing_entry.average_score = entry_data['average_score']
            existing_entry.updated_at = datetime.utcnow()
            created_entries.append(existing_entry)
            continue
            
        entry = Leaderboard(
            user_id=entry_data['user_id'],
            total_points=entry_data['total_points'],
            quizzes_completed=entry_data['quizzes_completed'],
            average_score=entry_data['average_score'],
            updated_at=datetime.utcnow()
        )
        
        db.session.add(entry)
        created_entries.append(entry)
        print(f"Created leaderboard entry for user {entry_data['user_id']}")
    
    db.session.commit()
    return created_entries

def seed_database():
    """Main function to seed the database"""
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    try:
        # Create sample data
        users = create_sample_users()
        notes = create_sample_notes(users)
        past_questions = create_sample_past_questions(users)
        quizzes = create_sample_quizzes(users)
        quiz_attempts = create_sample_quiz_attempts(users, quizzes)
        leaderboard = create_sample_leaderboard(users, quiz_attempts)
        
        print("\n✅ Database seeding completed successfully!")
        print(f"Created:")
        print(f"  - {len(users)} users")
        print(f"  - {len(notes)} notes")
        print(f"  - {len(past_questions)} past questions")
        print(f"  - {len(quizzes)} quizzes")
        print(f"  - {len(quiz_attempts)} quiz attempts")
        print(f"  - {len(leaderboard)} leaderboard entries")
        
        print("\n📋 Sample login credentials:")
        print("  Admin: admin@eduaccess.com / Admin123!")
        print("  User: john@example.com / Password123!")
        print("  User: jane@example.com / Password123!")
        print("  Student: student1@example.com / Student123!")
        print("  Student: student2@example.com / Student123!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    # Get configuration from environment variable or default to development
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create the Flask application
    app = create_app(config_name)
    
    with app.app_context():
        seed_database()
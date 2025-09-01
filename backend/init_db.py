#!/usr/bin/env python3
"""
Database initialization script for EduAccess backend.
This script creates the database, tables, and initial data.
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Note, Quiz, QuizAttempt, PastQuestion, Leaderboard
from config import config

def create_database():
    """Create the database and all tables."""
    app = create_app(config_name='development')
    
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables (be careful in production!)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Create initial data
        create_sample_data()
        
        print("Sample data created successfully!")

def create_sample_data():
    """Create sample data for testing."""
    
    # Create sample users
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@eduaccess.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_admin': True
        },
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith'
        },
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'password': 'student123',
            'first_name': 'Alice',
            'last_name': 'Johnson'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"Created {len(users)} sample users")
    
    # Create sample notes
    notes_data = [
        {
            'title': 'Introduction to Python',
            'content': 'Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.',
            'subject': 'Computer Science',
            'tags': 'python,programming,basics',
            'user_id': users[1].id
        },
        {
            'title': 'Calculus Fundamentals',
            'content': 'Calculus is the mathematical study of continuous change. It has two major branches: differential calculus and integral calculus, which are related by the fundamental theorem of calculus.',
            'subject': 'Mathematics',
            'tags': 'calculus,mathematics,derivatives,integrals',
            'user_id': users[1].id
        },
        {
            'title': 'World War II Overview',
            'content': 'World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world\'s countries and was the deadliest conflict in human history.',
            'subject': 'History',
            'tags': 'wwii,history,war,global',
            'user_id': users[2].id
        },
        {
            'title': 'Cell Biology Basics',
            'content': 'Cells are the basic units of life. All living organisms are composed of one or more cells. The cell theory states that all life is composed of cells and that cells are the basic unit of life.',
            'subject': 'Biology',
            'tags': 'biology,cells,life,organisms',
            'user_id': users[2].id
        }
    ]
    
    notes = []
    for note_data in notes_data:
        note = Note(
            title=note_data['title'],
            content=note_data['content'],
            subject=note_data['subject'],
            user_id=note_data['user_id']
        )
        notes.append(note)
        db.session.add(note)
    
    db.session.commit()
    print(f"Created {len(notes)} sample notes")
    
    # Create sample quizzes
    quizzes_data = [
        {
            'title': 'Python Basics Quiz',
            'description': 'Test your knowledge of Python programming fundamentals',
            'subject': 'Computer Science',
            'difficulty': 'beginner',
            'questions': [
                {
                    'question': 'What is Python?',
                    'options': ['A programming language', 'A snake', 'A web browser', 'An operating system'],
                    'correct_answer': 0
                },
                {
                    'question': 'Which of the following is used to define a function in Python?',
                    'options': ['function', 'def', 'define', 'func'],
                    'correct_answer': 1
                }
            ],
            'user_id': users[0].id
        },
        {
            'title': 'Mathematics Quiz',
            'description': 'Basic mathematics and calculus questions',
            'subject': 'Mathematics',
            'difficulty': 'intermediate',
            'questions': [
                {
                    'question': 'What is the derivative of x²?',
                    'options': ['x', '2x', 'x²', '2x²'],
                    'correct_answer': 1
                },
                {
                    'question': 'What is the integral of 2x?',
                    'options': ['x²', 'x² + C', '2', '2x + C'],
                    'correct_answer': 1
                }
            ],
            'user_id': users[0].id
        }
    ]
    
    quizzes = []
    for quiz_data in quizzes_data:
        quiz = Quiz(
            title=quiz_data['title'],
            subject=quiz_data['subject'],
            difficulty=quiz_data['difficulty'],
            questions=quiz_data['questions'],
            created_by=quiz_data['user_id']
        )
        quizzes.append(quiz)
        db.session.add(quiz)
    
    db.session.commit()
    print(f"Created {len(quizzes)} sample quizzes")
    
    # Create sample past questions
    past_questions_data = [
        {
            'title': 'Computer Science Final Exam 2023',
            'subject': 'Computer Science',
            'exam_type': 'Final Exam',
            'year': 2023,
            'institution': 'University of Technology',
            'description': 'Final examination covering algorithms, data structures, and programming concepts',
            'file_path': 'cs_final_2023.pdf',
            'user_id': users[0].id
        },
        {
            'title': 'Calculus Midterm 2023',
            'subject': 'Mathematics',
            'exam_type': 'Midterm',
            'year': 2023,
            'institution': 'State University',
            'description': 'Midterm examination on differential and integral calculus',
            'file_path': 'calc_midterm_2023.pdf',
            'user_id': users[0].id
        }
    ]
    
    past_questions = []
    for pq_data in past_questions_data:
        pq = PastQuestion(
            title=pq_data['title'],
            subject=pq_data['subject'],
            exam_type=pq_data['exam_type'],
            year=pq_data['year'],
            file_url=pq_data['file_path'],
            file_type='pdf',
            uploaded_by=pq_data['user_id']
        )
        past_questions.append(pq)
        db.session.add(pq)
    
    db.session.commit()
    print(f"Created {len(past_questions)} sample past questions")
    
    # Create sample quiz attempts and leaderboard entries
    quiz_attempts_data = [
        {'user_id': users[1].id, 'quiz_id': quizzes[0].id, 'score': 85, 'total_questions': 2},
        {'user_id': users[2].id, 'quiz_id': quizzes[0].id, 'score': 92, 'total_questions': 2},
        {'user_id': users[3].id, 'quiz_id': quizzes[1].id, 'score': 78, 'total_questions': 2},
        {'user_id': users[1].id, 'quiz_id': quizzes[1].id, 'score': 88, 'total_questions': 2}
    ]
    
    for attempt_data in quiz_attempts_data:
        attempt = QuizAttempt(
            user_id=attempt_data['user_id'],
            quiz_id=attempt_data['quiz_id'],
            score=attempt_data['score'],
            total_questions=attempt_data['total_questions'],
            answers=[0, 1]  # Sample answers
        )
        db.session.add(attempt)
    
    db.session.commit()
    print("Created sample quiz attempts")
    
    # Create leaderboard entries
    leaderboard_data = [
        {'user_id': users[1].id, 'total_points': 173, 'quizzes_completed': 2, 'average_score': 86.5},
        {'user_id': users[2].id, 'total_points': 92, 'quizzes_completed': 1, 'average_score': 92.0},
        {'user_id': users[3].id, 'total_points': 78, 'quizzes_completed': 1, 'average_score': 78.0}
    ]
    
    for lb_data in leaderboard_data:
        leaderboard = Leaderboard(
            user_id=lb_data['user_id'],
            total_points=lb_data['total_points'],
            quizzes_completed=lb_data['quizzes_completed'],
            average_score=lb_data['average_score']
        )
        db.session.add(leaderboard)
    
    db.session.commit()
    print("Created leaderboard entries")

if __name__ == '__main__':
    print("Initializing EduAccess database...")
    create_database()
    print("Database initialization completed!")
    print("\nSample login credentials:")
    print("Admin: admin@eduaccess.com / admin123")
    print("User: john@example.com / password123")
    print("User: jane@example.com / password123")
    print("User: student1@example.com / student123")
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Quiz, QuizAttempt, Note, PastQuestion
from security import limiter
from sqlalchemy import func, desc
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_dashboard_overview():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get basic stats
        total_notes = Note.query.filter_by(user_id=user_id).count()
        total_quizzes_created = Quiz.query.filter_by(created_by=user_id).count()
        total_quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).count()
        total_past_questions_uploaded = PastQuestion.query.filter_by(uploaded_by=user_id).count()
        
        # Get recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_notes = Note.query.filter(
            Note.user_id == user_id,
            Note.created_at >= week_ago
        ).count()
        
        recent_quiz_attempts = QuizAttempt.query.filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.completed_at >= week_ago
        ).count()
        
        # Get average quiz score
        avg_score_result = db.session.query(
            func.avg(QuizAttempt.score * 100.0 / QuizAttempt.total_questions)
        ).filter_by(user_id=user_id).scalar()
        
        average_quiz_score = round(avg_score_result, 2) if avg_score_result else 0.0
        
        # Get user rank
        leaderboard_entry = Leaderboard.query.filter_by(user_id=user_id).first()
        user_rank = leaderboard_entry.rank if leaderboard_entry else None
        
        # Get total users for rank context
        total_users = User.query.count()
        
        return jsonify({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'points': user.points,
                'rank': user_rank,
                'total_users': total_users
            },
            'stats': {
                'total_notes': total_notes,
                'total_quizzes_created': total_quizzes_created,
                'total_quiz_attempts': total_quiz_attempts,
                'total_past_questions_uploaded': total_past_questions_uploaded,
                'average_quiz_score': average_quiz_score
            },
            'recent_activity': {
                'notes_this_week': recent_notes,
                'quiz_attempts_this_week': recent_quiz_attempts
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get dashboard overview', 'details': str(e)}), 500

@dashboard_bp.route('/activity', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_activity_timeline():
    try:
        user_id = int(get_jwt_identity())
        days = request.args.get('days', 30, type=int)
        
        # Limit days to reasonable range
        days = min(days, 365)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily activity data
        activity_data = []
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            # Count activities for this day
            notes_created = Note.query.filter(
                Note.user_id == user_id,
                Note.created_at >= current_date,
                Note.created_at < next_date
            ).count()
            
            quizzes_taken = QuizAttempt.query.filter(
                QuizAttempt.user_id == user_id,
                QuizAttempt.completed_at >= current_date,
                QuizAttempt.completed_at < next_date
            ).count()
            
            quizzes_created = Quiz.query.filter(
                Quiz.created_by == user_id,
                Quiz.created_at >= current_date,
                Quiz.created_at < next_date
            ).count()
            
            activity_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'notes_created': notes_created,
                'quizzes_taken': quizzes_taken,
                'quizzes_created': quizzes_created,
                'total_activity': notes_created + quizzes_taken + quizzes_created
            })
        
        return jsonify({
            'activity_timeline': activity_data,
            'period_days': days
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get activity timeline', 'details': str(e)}), 500

@dashboard_bp.route('/quiz-performance', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_quiz_performance():
    try:
        user_id = int(get_jwt_identity())
        
        # Get all quiz attempts
        attempts = QuizAttempt.query.filter_by(user_id=user_id)\
            .order_by(QuizAttempt.completed_at.desc()).all()
        
        if not attempts:
            return jsonify({
                'quiz_performance': {
                    'total_attempts': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'recent_attempts': [],
                    'performance_trend': [],
                    'subject_performance': []
                }
            }), 200
        
        # Calculate performance metrics
        total_attempts = len(attempts)
        scores = [(attempt.score / attempt.total_questions) * 100 for attempt in attempts]
        average_score = round(sum(scores) / len(scores), 2)
        best_score = round(max(scores), 2)
        
        # Get recent attempts (last 10)
        recent_attempts = [{
            'id': attempt.id,
            'quiz_id': attempt.quiz_id,
            'score': attempt.score,
            'total_questions': attempt.total_questions,
            'percentage': round((attempt.score / attempt.total_questions) * 100, 2),
            'time_taken': attempt.time_taken,
            'completed_at': attempt.completed_at.isoformat()
        } for attempt in attempts[:10]]
        
        # Performance trend (last 20 attempts)
        trend_data = [{
            'attempt_number': i + 1,
            'score_percentage': round((attempt.score / attempt.total_questions) * 100, 2),
            'date': attempt.completed_at.strftime('%Y-%m-%d')
        } for i, attempt in enumerate(attempts[:20][::-1])]
        
        # Subject performance
        subject_performance = db.session.query(
            Quiz.subject,
            func.count(QuizAttempt.id).label('attempts'),
            func.avg(QuizAttempt.score * 100.0 / QuizAttempt.total_questions).label('avg_score')
        ).join(Quiz, QuizAttempt.quiz_id == Quiz.id)\
         .filter(QuizAttempt.user_id == user_id)\
         .group_by(Quiz.subject).all()
        
        subject_data = [{
            'subject': perf[0],
            'attempts': perf[1],
            'average_score': round(perf[2], 2)
        } for perf in subject_performance]
        
        return jsonify({
            'quiz_performance': {
                'total_attempts': total_attempts,
                'average_score': average_score,
                'best_score': best_score,
                'recent_attempts': recent_attempts,
                'performance_trend': trend_data,
                'subject_performance': subject_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get quiz performance', 'details': str(e)}), 500

@dashboard_bp.route('/notes-analytics', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_notes_analytics():
    try:
        user_id = int(get_jwt_identity())
        
        # Get all notes
        notes = Note.query.filter_by(user_id=user_id).all()
        
        if not notes:
            return jsonify({
                'notes_analytics': {
                    'total_notes': 0,
                    'subjects': [],
                    'creation_timeline': [],
                    'recent_notes': []
                }
            }), 200
        
        # Subject distribution
        subject_counts = {}
        for note in notes:
            subject = note.subject
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        subject_data = [{
            'subject': subject,
            'count': count
        } for subject, count in subject_counts.items()]
        
        # Creation timeline (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        timeline_data = []
        
        for i in range(30):
            current_date = thirty_days_ago + timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            notes_count = Note.query.filter(
                Note.user_id == user_id,
                Note.created_at >= current_date,
                Note.created_at < next_date
            ).count()
            
            timeline_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'notes_created': notes_count
            })
        
        # Recent notes (last 5)
        recent_notes = Note.query.filter_by(user_id=user_id)\
            .order_by(Note.created_at.desc()).limit(5).all()
        
        recent_notes_data = [{
            'id': note.id,
            'title': note.title,
            'subject': note.subject,
            'created_at': note.created_at.isoformat()
        } for note in recent_notes]
        
        return jsonify({
            'notes_analytics': {
                'total_notes': len(notes),
                'subjects': subject_data,
                'creation_timeline': timeline_data,
                'recent_notes': recent_notes_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get notes analytics', 'details': str(e)}), 500

@dashboard_bp.route('/achievements', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_achievements():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Calculate achievements
        achievements = []
        
        # Points-based achievements
        if user.points >= 1000:
            achievements.append({
                'title': 'Point Master',
                'description': 'Earned 1000+ points',
                'icon': '🏆',
                'earned': True
            })
        elif user.points >= 500:
            achievements.append({
                'title': 'Point Collector',
                'description': 'Earned 500+ points',
                'icon': '🥉',
                'earned': True
            })
        
        # Notes-based achievements
        notes_count = Note.query.filter_by(user_id=user_id).count()
        if notes_count >= 50:
            achievements.append({
                'title': 'Note Taking Pro',
                'description': 'Created 50+ notes',
                'icon': '📚',
                'earned': True
            })
        elif notes_count >= 10:
            achievements.append({
                'title': 'Note Taker',
                'description': 'Created 10+ notes',
                'icon': '📝',
                'earned': True
            })
        
        # Quiz-based achievements
        quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).count()
        if quiz_attempts >= 100:
            achievements.append({
                'title': 'Quiz Master',
                'description': 'Completed 100+ quizzes',
                'icon': '🧠',
                'earned': True
            })
        elif quiz_attempts >= 25:
            achievements.append({
                'title': 'Quiz Enthusiast',
                'description': 'Completed 25+ quizzes',
                'icon': '🎯',
                'earned': True
            })
        
        # Perfect score achievement
        perfect_scores = QuizAttempt.query.filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.score == QuizAttempt.total_questions
        ).count()
        
        if perfect_scores >= 5:
            achievements.append({
                'title': 'Perfectionist',
                'description': 'Achieved 5+ perfect quiz scores',
                'icon': '⭐',
                'earned': True
            })
        
        # Streak achievements (simplified - would need more complex logic for real streaks)
        recent_activity = QuizAttempt.query.filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.completed_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        if recent_activity >= 7:
            achievements.append({
                'title': 'Weekly Warrior',
                'description': 'Active for 7 days straight',
                'icon': '🔥',
                'earned': True
            })
        
        return jsonify({
            'achievements': achievements,
            'total_earned': len(achievements)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get achievements', 'details': str(e)}), 500

@dashboard_bp.route('/goals', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_goals():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Define goals and calculate progress
        goals = []
        
        # Points goal
        next_point_milestone = 100
        if user.points >= 1000:
            next_point_milestone = 2000
        elif user.points >= 500:
            next_point_milestone = 1000
        elif user.points >= 100:
            next_point_milestone = 500
        
        goals.append({
            'title': f'Reach {next_point_milestone} Points',
            'description': f'Earn {next_point_milestone - user.points} more points',
            'current': user.points,
            'target': next_point_milestone,
            'progress': min(100, (user.points / next_point_milestone) * 100),
            'category': 'points'
        })
        
        # Notes goal
        notes_count = Note.query.filter_by(user_id=user_id).count()
        next_notes_milestone = 10 if notes_count < 10 else 25 if notes_count < 25 else 50
        
        goals.append({
            'title': f'Create {next_notes_milestone} Notes',
            'description': f'Create {next_notes_milestone - notes_count} more notes',
            'current': notes_count,
            'target': next_notes_milestone,
            'progress': min(100, (notes_count / next_notes_milestone) * 100),
            'category': 'notes'
        })
        
        # Quiz attempts goal
        quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).count()
        next_quiz_milestone = 10 if quiz_attempts < 10 else 25 if quiz_attempts < 25 else 50
        
        goals.append({
            'title': f'Complete {next_quiz_milestone} Quizzes',
            'description': f'Complete {next_quiz_milestone - quiz_attempts} more quizzes',
            'current': quiz_attempts,
            'target': next_quiz_milestone,
            'progress': min(100, (quiz_attempts / next_quiz_milestone) * 100),
            'category': 'quizzes'
        })
        
        return jsonify({'goals': goals}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get goals', 'details': str(e)}), 500
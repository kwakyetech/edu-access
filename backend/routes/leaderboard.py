from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Leaderboard, User, QuizAttempt, Note, db
from sqlalchemy import func, desc

leaderboard_bp = Blueprint('leaderboard', __name__)

def update_user_leaderboard_stats(user_id):
    """Update leaderboard statistics for a user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return
        
        # Get or create leaderboard entry
        leaderboard_entry = Leaderboard.query.filter_by(user_id=user_id).first()
        if not leaderboard_entry:
            leaderboard_entry = Leaderboard(user_id=user_id)
            db.session.add(leaderboard_entry)
        
        # Calculate stats
        total_points = user.points
        quizzes_completed = QuizAttempt.query.filter_by(user_id=user_id).count()
        notes_uploaded = Note.query.filter_by(user_id=user_id).count()
        
        # Calculate average score
        avg_score_result = db.session.query(
            func.avg(QuizAttempt.score * 100.0 / QuizAttempt.total_questions)
        ).filter_by(user_id=user_id).scalar()
        
        average_score = round(avg_score_result, 2) if avg_score_result else 0.0
        
        # Update leaderboard entry
        leaderboard_entry.total_points = total_points
        leaderboard_entry.quizzes_completed = quizzes_completed
        leaderboard_entry.notes_uploaded = notes_uploaded
        leaderboard_entry.average_score = average_score
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating leaderboard stats: {e}")

def update_all_ranks():
    """Update ranks for all users in leaderboard"""
    try:
        # Get all leaderboard entries ordered by total points (desc), then by average score (desc)
        entries = Leaderboard.query.order_by(
            desc(Leaderboard.total_points),
            desc(Leaderboard.average_score),
            desc(Leaderboard.quizzes_completed)
        ).all()
        
        # Update ranks
        for index, entry in enumerate(entries, 1):
            entry.rank = index
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating ranks: {e}")

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Update all user stats first
        users = User.query.all()
        for user in users:
            update_user_leaderboard_stats(user.id)
        
        # Update ranks
        update_all_ranks()
        
        # Get leaderboard with pagination
        leaderboard = Leaderboard.query.order_by(
            Leaderboard.rank.asc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'leaderboard': [entry.to_dict() for entry in leaderboard.items],
            'total': leaderboard.total,
            'pages': leaderboard.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get leaderboard', 'details': str(e)}), 500

@leaderboard_bp.route('/top/<int:limit>', methods=['GET'])
def get_top_users(limit):
    try:
        # Limit the number of top users (max 50)
        limit = min(limit, 50)
        
        # Update all user stats first
        users = User.query.all()
        for user in users:
            update_user_leaderboard_stats(user.id)
        
        # Update ranks
        update_all_ranks()
        
        # Get top users
        top_users = Leaderboard.query.order_by(
            Leaderboard.rank.asc()
        ).limit(limit).all()
        
        return jsonify({
            'top_users': [entry.to_dict() for entry in top_users],
            'count': len(top_users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get top users', 'details': str(e)}), 500

@leaderboard_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_rank(user_id):
    try:
        # Update user stats
        update_user_leaderboard_stats(user_id)
        
        # Update all ranks
        update_all_ranks()
        
        # Get user's leaderboard entry
        entry = Leaderboard.query.filter_by(user_id=user_id).first()
        
        if not entry:
            return jsonify({'error': 'User not found in leaderboard'}), 404
        
        return jsonify({'user_rank': entry.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user rank', 'details': str(e)}), 500

@leaderboard_bp.route('/my-rank', methods=['GET'])
@jwt_required()
def get_my_rank():
    try:
        user_id = get_jwt_identity()
        
        # Update user stats
        update_user_leaderboard_stats(user_id)
        
        # Update all ranks
        update_all_ranks()
        
        # Get user's leaderboard entry
        entry = Leaderboard.query.filter_by(user_id=user_id).first()
        
        if not entry:
            return jsonify({'error': 'User not found in leaderboard'}), 404
        
        # Get users around current user's rank
        current_rank = entry.rank
        
        # Get 2 users above and 2 users below
        nearby_users = Leaderboard.query.filter(
            Leaderboard.rank.between(max(1, current_rank - 2), current_rank + 2)
        ).order_by(Leaderboard.rank.asc()).all()
        
        return jsonify({
            'my_rank': entry.to_dict(),
            'nearby_users': [user.to_dict() for user in nearby_users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get my rank', 'details': str(e)}), 500

@leaderboard_bp.route('/stats', methods=['GET'])
def get_leaderboard_stats():
    try:
        # Update all user stats
        users = User.query.all()
        for user in users:
            update_user_leaderboard_stats(user.id)
        
        # Get general stats
        total_users = User.query.count()
        total_points_awarded = db.session.query(func.sum(User.points)).scalar() or 0
        total_quizzes_completed = QuizAttempt.query.count()
        total_notes_uploaded = Note.query.count()
        
        # Get average stats
        avg_points = db.session.query(func.avg(User.points)).scalar() or 0
        avg_quiz_score = db.session.query(
            func.avg(QuizAttempt.score * 100.0 / QuizAttempt.total_questions)
        ).scalar() or 0
        
        # Get top performers
        top_scorer = Leaderboard.query.order_by(
            desc(Leaderboard.total_points)
        ).first()
        
        most_active_quiz_taker = Leaderboard.query.order_by(
            desc(Leaderboard.quizzes_completed)
        ).first()
        
        most_active_note_uploader = Leaderboard.query.order_by(
            desc(Leaderboard.notes_uploaded)
        ).first()
        
        return jsonify({
            'general_stats': {
                'total_users': total_users,
                'total_points_awarded': int(total_points_awarded),
                'total_quizzes_completed': total_quizzes_completed,
                'total_notes_uploaded': total_notes_uploaded,
                'average_points_per_user': round(avg_points, 2),
                'average_quiz_score': round(avg_quiz_score, 2)
            },
            'top_performers': {
                'highest_points': top_scorer.to_dict() if top_scorer else None,
                'most_quizzes': most_active_quiz_taker.to_dict() if most_active_quiz_taker else None,
                'most_notes': most_active_note_uploader.to_dict() if most_active_note_uploader else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get leaderboard stats', 'details': str(e)}), 500

@leaderboard_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_leaderboard():
    try:
        # Update all user stats
        users = User.query.all()
        for user in users:
            update_user_leaderboard_stats(user.id)
        
        # Update ranks
        update_all_ranks()
        
        return jsonify({'message': 'Leaderboard refreshed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to refresh leaderboard', 'details': str(e)}), 500

@leaderboard_bp.route('/subject/<subject>', methods=['GET'])
def get_subject_leaderboard(subject):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get users with quiz attempts in the specific subject
        # This is a more complex query that would need to join with Quiz table
        # For now, we'll return the general leaderboard with a note
        
        # In a full implementation, you would:
        # 1. Join QuizAttempt with Quiz on quiz_id
        # 2. Filter by Quiz.subject
        # 3. Calculate subject-specific stats
        
        return jsonify({
            'message': f'Subject-specific leaderboard for {subject} not yet implemented',
            'suggestion': 'Use general leaderboard endpoint for now'
        }), 501  # Not Implemented
        
    except Exception as e:
        return jsonify({'error': 'Failed to get subject leaderboard', 'details': str(e)}), 500
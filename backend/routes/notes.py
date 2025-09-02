from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User, db
from utils import format_response, format_error
from security import limiter, require_json, validate_request_data, InputValidator, log_security_event, InputSanitizer
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/', methods=['GET'])
@jwt_required()
@limiter.limit("200 per hour")
def get_notes():
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        subject = request.args.get('subject')
        search = request.args.get('search')
        
        # Build query
        query = Note.query.filter_by(user_id=user_id)
        
        if subject:
            query = query.filter(Note.subject.ilike(f'%{subject}%'))
        
        if search:
            query = query.filter(
                db.or_(
                    Note.title.ilike(f'%{search}%'),
                    Note.content.ilike(f'%{search}%')
                )
            )
        
        # Order by creation date (newest first)
        query = query.order_by(Note.created_at.desc())
        
        # Paginate
        notes = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'notes': [note.to_dict() for note in notes.items],
            'total': notes.total,
            'pages': notes.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get notes', 'details': str(e)}), 500

@notes_bp.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    try:
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        return jsonify({'note': note.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get note', 'details': str(e)}), 500

@notes_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
@require_json
@validate_request_data(
    required_fields=['title', 'content', 'subject'],
    validators={
        'subject': InputValidator.validate_subject
    }
)
def create_note():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Extract and sanitize validated data
        title = InputSanitizer.sanitize_string(data['title'].strip())
        content = InputSanitizer.sanitize_string(data['content'].strip())
        subject = data['subject'].strip()
        file_url = data.get('file_url')
        file_type = data.get('file_type')
        tags = data.get('tags', [])
        is_public = data.get('is_public', True)
        
        # Create new note
        note = Note(
            title=title,
            content=content,
            subject=subject,
            file_url=file_url,
            file_type=file_type,
            user_id=user_id
        )
        
        db.session.add(note)
        db.session.commit()
        
        # Log note creation
        log_security_event('note_created', {
            'user_id': user_id,
            'note_id': note.id,
            'subject': subject,
            'is_public': is_public
        })
        
        # Award points for creating a note
        user = User.query.get(user_id)
        if user:
            user.points += 10  # 10 points for creating a note
            db.session.commit()
        
        return jsonify({
            'message': 'Note created successfully',
            'note': note.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create note', 'details': str(e)}), 500

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per hour")
@require_json
def update_note(note_id):
    try:
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            note.title = InputSanitizer.sanitize_string(data['title'].strip())
        if 'content' in data:
            note.content = InputSanitizer.sanitize_string(data['content'].strip())
        if 'subject' in data:
            note.subject = data['subject'].strip()
        if 'file_url' in data:
            note.file_url = data['file_url']
        if 'file_type' in data:
            note.file_type = data['file_type']
        if 'tags' in data:
            note.tags = data['tags']
        if 'is_public' in data:
            note.is_public = data['is_public']
        
        note.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log note update
        log_security_event('note_updated', {
            'user_id': user_id,
            'note_id': note_id,
            'subject': note.subject
        })
        
        return jsonify({
            'message': 'Note updated successfully',
            'note': note.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update note', 'details': str(e)}), 500

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    try:
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': 'Note deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete note', 'details': str(e)}), 500

@notes_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    try:
        user_id = int(get_jwt_identity())
        
        # Get unique subjects for the user
        subjects = db.session.query(Note.subject).filter_by(user_id=user_id).distinct().all()
        subject_list = [subject[0] for subject in subjects]
        
        return jsonify({'subjects': subject_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get subjects', 'details': str(e)}), 500

@notes_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_notes_stats():
    try:
        user_id = int(get_jwt_identity())
        
        # Get total notes count
        total_notes = Note.query.filter_by(user_id=user_id).count()
        
        # Get notes by subject
        subject_stats = db.session.query(
            Note.subject,
            db.func.count(Note.id).label('count')
        ).filter_by(user_id=user_id).group_by(Note.subject).all()
        
        subject_data = [{
            'subject': stat[0],
            'count': stat[1]
        } for stat in subject_stats]
        
        # Get recent notes (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_notes = Note.query.filter(
            Note.user_id == user_id,
            Note.created_at >= week_ago
        ).count()
        
        return jsonify({
            'total_notes': total_notes,
            'subjects': subject_data,
            'recent_notes': recent_notes
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get notes stats', 'details': str(e)}), 500
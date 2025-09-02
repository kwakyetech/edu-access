from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import PastQuestion, User, db
from datetime import datetime
from security import limiter, require_json, validate_request_data, InputValidator, log_security_event

past_questions_bp = Blueprint('past_questions', __name__)

@past_questions_bp.route('/', methods=['GET'])
@limiter.limit("100 per hour")
def get_past_questions():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        subject = request.args.get('subject')
        exam_type = request.args.get('exam_type')
        year = request.args.get('year', type=int)
        search = request.args.get('search')
        
        # Build query
        query = PastQuestion.query
        
        if subject:
            query = query.filter(PastQuestion.subject.ilike(f'%{subject}%'))
        
        if exam_type:
            query = query.filter(PastQuestion.exam_type.ilike(f'%{exam_type}%'))
        
        if year:
            query = query.filter_by(year=year)
        
        if search:
            query = query.filter(
                db.or_(
                    PastQuestion.title.ilike(f'%{search}%'),
                    PastQuestion.subject.ilike(f'%{search}%'),
                    PastQuestion.exam_type.ilike(f'%{search}%')
                )
            )
        
        # Order by year (newest first), then by download count
        query = query.order_by(
            PastQuestion.year.desc(),
            PastQuestion.download_count.desc()
        )
        
        # Paginate
        past_questions = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'past_questions': [pq.to_dict() for pq in past_questions.items],
            'total': past_questions.total,
            'pages': past_questions.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get past questions', 'details': str(e)}), 500

@past_questions_bp.route('/<int:question_id>', methods=['GET'])
def get_past_question(question_id):
    try:
        past_question = PastQuestion.query.get(question_id)
        
        if not past_question:
            return jsonify({'error': 'Past question not found'}), 404
        
        return jsonify({'past_question': past_question.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get past question', 'details': str(e)}), 500

@past_questions_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("10 per hour")
@require_json
@validate_request_data(
    required_fields=['title', 'subject', 'year', 'exam_type'],
    validators={
        'year': InputValidator.validate_year,
        'subject': InputValidator.validate_subject,
        'exam_type': InputValidator.validate_exam_type
    }
)
def upload_past_question():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Extract validated data
        title = data['title'].strip()
        subject = data['subject'].strip()
        year = data['year']
        exam_type = data['exam_type'].strip()
        file_url = data.get('file_url', '')
        file_type = data.get('file_type', 'PDF')
        
        # Validate year
        current_year = datetime.now().year
        if year < 1990 or year > current_year:
            return jsonify({'error': f'Year must be between 1990 and {current_year}'}), 400
        
        # Check if similar past question already exists
        existing = PastQuestion.query.filter_by(
            subject=subject,
            year=year,
            exam_type=exam_type
        ).first()
        
        if existing:
            return jsonify({
                'error': f'Past question for {subject} {exam_type} {year} already exists'
            }), 400
        
        # Create new past question
        past_question = PastQuestion(
            title=title,
            subject=subject,
            year=year,
            exam_type=exam_type,
            file_url=file_url,
            file_type=file_type,
            uploaded_by=user_id
        )
        
        db.session.add(past_question)
        db.session.commit()
        
        # Award points for uploading past question
        user = User.query.get(user_id)
        if user:
            user.points += 25  # 25 points for uploading past question
            db.session.commit()
        
        # Log successful upload
        log_security_event('past_question_uploaded', {
            'user_id': user_id,
            'question_id': past_question.id,
            'subject': subject,
            'year': year
        })
        
        return jsonify({
            'message': 'Past question uploaded successfully',
            'past_question': past_question.to_dict()
        }), 201
        
    except ValueError:
        return jsonify({'error': 'Invalid year format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload past question', 'details': str(e)}), 500

@past_questions_bp.route('/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_past_question(question_id):
    try:
        user_id = int(get_jwt_identity())
        past_question = PastQuestion.query.filter_by(
            id=question_id, 
            uploaded_by=user_id
        ).first()
        
        if not past_question:
            return jsonify({'error': 'Past question not found or not authorized'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            past_question.title = data['title'].strip()
        if 'subject' in data:
            past_question.subject = data['subject'].strip()
        if 'year' in data:
            year = int(data['year'])
            current_year = datetime.now().year
            if year < 1990 or year > current_year:
                return jsonify({'error': f'Year must be between 1990 and {current_year}'}), 400
            past_question.year = year
        if 'exam_type' in data:
            past_question.exam_type = data['exam_type'].strip()
        if 'file_url' in data:
            past_question.file_url = data['file_url']
        if 'file_type' in data:
            past_question.file_type = data['file_type']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Past question updated successfully',
            'past_question': past_question.to_dict()
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid year format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update past question', 'details': str(e)}), 500

@past_questions_bp.route('/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_past_question(question_id):
    try:
        user_id = int(get_jwt_identity())
        past_question = PastQuestion.query.filter_by(
            id=question_id, 
            uploaded_by=user_id
        ).first()
        
        if not past_question:
            return jsonify({'error': 'Past question not found or not authorized'}), 404
        
        db.session.delete(past_question)
        db.session.commit()
        
        return jsonify({'message': 'Past question deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete past question', 'details': str(e)}), 500

@past_questions_bp.route('/<int:question_id>/download', methods=['POST'])
@limiter.limit("50 per hour")
def download_past_question(question_id):
    try:
        past_question = PastQuestion.query.get(question_id)
        
        if not past_question:
            return jsonify({'error': 'Past question not found'}), 404
        
        # Log download attempt
        log_security_event('past_question_downloaded', {
            'question_id': question_id,
            'title': past_question.title,
            'subject': past_question.subject
        })
        
        # Increment download count
        past_question.download_count += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Download count updated',
            'file_url': past_question.file_url,
            'download_count': past_question.download_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process download', 'details': str(e)}), 500

@past_questions_bp.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        # Get unique subjects
        subjects = db.session.query(PastQuestion.subject).distinct().all()
        subject_list = [subject[0] for subject in subjects]
        
        return jsonify({'subjects': subject_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get subjects', 'details': str(e)}), 500

@past_questions_bp.route('/exam-types', methods=['GET'])
def get_exam_types():
    try:
        # Get unique exam types
        exam_types = db.session.query(PastQuestion.exam_type).distinct().all()
        exam_type_list = [exam_type[0] for exam_type in exam_types]
        
        return jsonify({'exam_types': exam_type_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get exam types', 'details': str(e)}), 500

@past_questions_bp.route('/years', methods=['GET'])
def get_years():
    try:
        # Get unique years
        years = db.session.query(PastQuestion.year).distinct().order_by(PastQuestion.year.desc()).all()
        year_list = [year[0] for year in years]
        
        return jsonify({'years': year_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get years', 'details': str(e)}), 500

@past_questions_bp.route('/stats', methods=['GET'])
def get_past_questions_stats():
    try:
        # Get total count
        total_questions = PastQuestion.query.count()
        
        # Get stats by subject
        subject_stats = db.session.query(
            PastQuestion.subject,
            db.func.count(PastQuestion.id).label('count')
        ).group_by(PastQuestion.subject).all()
        
        # Get stats by exam type
        exam_type_stats = db.session.query(
            PastQuestion.exam_type,
            db.func.count(PastQuestion.id).label('count')
        ).group_by(PastQuestion.exam_type).all()
        
        # Get most downloaded
        most_downloaded = PastQuestion.query.order_by(
            PastQuestion.download_count.desc()
        ).limit(5).all()
        
        return jsonify({
            'total_questions': total_questions,
            'subjects': [{
                'subject': stat[0],
                'count': stat[1]
            } for stat in subject_stats],
            'exam_types': [{
                'exam_type': stat[0],
                'count': stat[1]
            } for stat in exam_type_stats],
            'most_downloaded': [pq.to_dict() for pq in most_downloaded]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get past questions stats', 'details': str(e)}), 500
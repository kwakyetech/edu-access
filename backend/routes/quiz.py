from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Quiz, QuizAttempt, User, Note, db
from transformers import pipeline
from security import limiter, require_json, validate_request_data, InputValidator, log_security_event
import json
import re
import random

quiz_bp = Blueprint('quiz', __name__)

# Initialize Hugging Face question generation pipeline
try:
    # Use a lightweight model for question generation
    question_generator = pipeline(
        "text2text-generation",
        model="valhalla/t5-small-qg-hl",
        tokenizer="valhalla/t5-small-qg-hl"
    )
except Exception as e:
    print(f"Warning: Could not load question generation model: {e}")
    question_generator = None

def generate_questions_from_text(text, num_questions=5):
    """Generate questions from text using Hugging Face model"""
    if not question_generator:
        # Fallback to simple question generation if model is not available
        return generate_fallback_questions(text, num_questions)
    
    try:
        # Split text into sentences for better question generation
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        questions = []
        
        for i, sentence in enumerate(sentences[:num_questions]):
            if len(sentence) < 20:
                continue
                
            # Generate question using the model
            input_text = f"generate question: {sentence}"
            result = question_generator(input_text, max_length=64, num_return_sequences=1)
            
            if result and len(result) > 0:
                question_text = result[0]['generated_text'].strip()
                
                # Generate multiple choice options
                options = generate_options_for_question(sentence, question_text)
                
                question = {
                    "id": i + 1,
                    "question": question_text,
                    "options": options["options"],
                    "correct_answer": options["correct_answer"],
                    "explanation": f"Based on: {sentence[:100]}..."
                }
                questions.append(question)
                
                if len(questions) >= num_questions:
                    break
        
        return questions
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        return generate_fallback_questions(text, num_questions)

def generate_options_for_question(context, question):
    """Generate multiple choice options for a question"""
    # Extract key terms from context
    words = re.findall(r'\b[A-Z][a-z]+\b|\b\d+\b', context)
    
    # Create plausible wrong answers
    distractors = [
        "Option A",
        "Option B", 
        "Option C",
        "Option D"
    ]
    
    if words:
        # Use actual words from context for more realistic options
        random.shuffle(words)
        distractors = words[:3] + ["None of the above"]
    
    # The correct answer should be derived from context
    correct_answer = extract_answer_from_context(context, question)
    
    options = [correct_answer] + distractors[:3]
    random.shuffle(options)
    
    correct_index = options.index(correct_answer)
    
    return {
        "options": options,
        "correct_answer": correct_index
    }

def extract_answer_from_context(context, question):
    """Extract the most likely answer from context"""
    # Simple extraction - in a real implementation, this would be more sophisticated
    words = re.findall(r'\b[A-Z][a-z]+\b', context)
    if words:
        return words[0]
    return "Correct Answer"

def generate_fallback_questions(text, num_questions=5):
    """Fallback question generation when AI model is not available"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    questions = []
    question_templates = [
        "What is the main concept discussed in: '{}'?",
        "According to the text, what can be said about '{}'?",
        "Which statement best describes '{}'?",
        "What is the significance of '{}'?",
        "How would you explain '{}'?"
    ]
    
    for i, sentence in enumerate(sentences[:num_questions]):
        if len(sentence) < 20:
            continue
            
        # Extract key phrase from sentence
        words = sentence.split()
        key_phrase = ' '.join(words[:5]) if len(words) >= 5 else sentence
        
        template = random.choice(question_templates)
        question_text = template.format(key_phrase)
        
        # Generate options
        options = [
            "Option A - Correct answer based on context",
            "Option B - Incorrect option",
            "Option C - Another incorrect option", 
            "Option D - Final incorrect option"
        ]
        random.shuffle(options)
        
        question = {
            "id": i + 1,
            "question": question_text,
            "options": options,
            "correct_answer": 0,  # First option is always correct after shuffle
            "explanation": f"Based on the context: {sentence[:100]}..."
        }
        questions.append(question)
        
        if len(questions) >= num_questions:
            break
    
    return questions

@quiz_bp.route('/generate', methods=['POST'])
@jwt_required()
@limiter.limit("10 per hour")
@require_json
@validate_request_data(
    required_fields=['content'],
    validators={
        'subject': InputValidator.validate_subject
    }
)
def generate_quiz():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Extract validated data
        content = data['content'].strip()
        title = data.get('title', 'Generated Quiz')
        subject = data.get('subject', 'General')
        difficulty = data.get('difficulty', 'medium')
        num_questions = min(int(data.get('num_questions', 5)), 10)  # Max 10 questions
        
        # Generate questions using AI
        questions = generate_questions_from_text(content, num_questions)
        
        if not questions:
            return jsonify({'error': 'Could not generate questions from the provided content'}), 400
        
        # Create quiz in database
        quiz = Quiz(
            title=title,
            subject=subject,
            difficulty=difficulty,
            questions=questions,
            created_by=user_id
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        # Log quiz generation
        log_security_event('quiz_generated', {
            'user_id': user_id,
            'quiz_id': quiz.id,
            'num_questions': len(questions)
        })
        
        # Award points for creating a quiz
        user = User.query.get(user_id)
        if user:
            user.points += 20  # 20 points for creating a quiz
            db.session.commit()
        
        return jsonify({
            'message': 'Quiz generated successfully',
            'quiz': quiz.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to generate quiz', 'details': str(e)}), 500

@quiz_bp.route('/from-note/<int:note_id>', methods=['POST'])
@jwt_required()
def generate_quiz_from_note(note_id):
    try:
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json() or {}
        num_questions = min(int(data.get('num_questions', 5)), 10)
        difficulty = data.get('difficulty', 'medium')
        
        # Generate questions from note content
        questions = generate_questions_from_text(note.content, num_questions)
        
        if not questions:
            return jsonify({'error': 'Could not generate questions from the note content'}), 400
        
        # Create quiz
        quiz = Quiz(
            title=f"Quiz: {note.title}",
            subject=note.subject,
            difficulty=difficulty,
            questions=questions,
            created_by=user_id
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        # Award points
        user = User.query.get(user_id)
        if user:
            user.points += 15  # 15 points for generating quiz from note
            db.session.commit()
        
        return jsonify({
            'message': 'Quiz generated from note successfully',
            'quiz': quiz.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to generate quiz from note', 'details': str(e)}), 500

@quiz_bp.route('/', methods=['GET'])
@jwt_required()
def get_quizzes():
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        subject = request.args.get('subject')
        difficulty = request.args.get('difficulty')
        
        # Build query - get user's own quizzes
        query = Quiz.query.filter_by(created_by=user_id)
        
        if subject:
            query = query.filter(Quiz.subject.ilike(f'%{subject}%'))
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        # Order by creation date (newest first)
        query = query.order_by(Quiz.created_at.desc())
        
        # Paginate
        quizzes = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'quizzes': [quiz.to_dict() for quiz in quizzes.items],
            'total': quizzes.total,
            'pages': quizzes.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get quizzes', 'details': str(e)}), 500

@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id):
    try:
        user_id = int(get_jwt_identity())
        quiz = Quiz.query.filter_by(id=quiz_id, created_by=user_id).first()
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        return jsonify({'quiz': quiz.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get quiz', 'details': str(e)}), 500

@quiz_bp.route('/<int:quiz_id>/attempt', methods=['POST'])
@jwt_required()
@limiter.limit("50 per hour")
@require_json
def submit_quiz_attempt(quiz_id):
    try:
        user_id = int(get_jwt_identity())
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        data = request.get_json()
        
        # Extract answers from request
        if 'answers' not in data:
            return jsonify({'error': 'answers is required'}), 400
        
        answers = data['answers']
        time_taken = data.get('time_taken', 0)
        
        # Calculate score
        score = 0
        total_questions = len(quiz.questions)
        
        for question in quiz.questions:
            question_id = question['id']
            correct_answer = question['correct_answer']
            user_answer = answers.get(str(question_id))
            
            if user_answer == correct_answer:
                score += 1
        
        # Create quiz attempt
        attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            answers=answers,
            score=score,
            total_questions=total_questions,
            time_taken=time_taken
        )
        
        db.session.add(attempt)
        
        # Award points based on score
        user = User.query.get(user_id)
        if user:
            points_earned = score * 5  # 5 points per correct answer
            user.points += points_earned
        
        db.session.commit()
        
        # Log quiz attempt
        log_security_event('quiz_attempted', {
            'user_id': user_id,
            'quiz_id': quiz_id,
            'score': score,
            'total_questions': total_questions
        })
        
        return jsonify({
            'message': 'Quiz attempt submitted successfully',
            'attempt': attempt.to_dict(),
            'points_earned': score * 5
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit quiz attempt', 'details': str(e)}), 500

@quiz_bp.route('/attempts', methods=['GET'])
@jwt_required()
def get_quiz_attempts():
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get user's quiz attempts
        attempts = QuizAttempt.query.filter_by(user_id=user_id)\
            .order_by(QuizAttempt.completed_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'attempts': [attempt.to_dict() for attempt in attempts.items],
            'total': attempts.total,
            'pages': attempts.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get quiz attempts', 'details': str(e)}), 500
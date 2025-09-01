import os
import secrets
import requests
from werkzeug.utils import secure_filename
from flask import current_app
from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file, upload_folder=None):
    """Save uploaded file to the specified folder."""
    if file and allowed_file(file.filename):
        # Generate a secure filename
        filename = secure_filename(file.filename)
        
        # Add random string to avoid filename conflicts
        name, ext = os.path.splitext(filename)
        random_string = secrets.token_hex(8)
        filename = f"{name}_{random_string}{ext}"
        
        # Use provided upload folder or default from config
        folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        
        # Create upload directory if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(folder, filename)
        file.save(file_path)
        
        return filename, file_path
    
    return None, None

def delete_file(filename, upload_folder=None):
    """Delete a file from the upload folder."""
    try:
        folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(folder, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {str(e)}")
        return False

class HuggingFaceAPI:
    """Wrapper class for Hugging Face API interactions."""
    
    def __init__(self):
        self.api_token = current_app.config.get('HUGGINGFACE_API_TOKEN')
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Initialize local pipeline as fallback
        try:
            self.qa_pipeline = pipeline("question-answering", 
                                      model="distilbert-base-cased-distilled-squad")
        except Exception as e:
            logger.warning(f"Could not initialize local QA pipeline: {str(e)}")
            self.qa_pipeline = None
    
    def generate_questions(self, context, num_questions=5):
        """Generate questions from given context using Hugging Face API."""
        try:
            # Try API first if token is available
            if self.api_token:
                return self._generate_questions_api(context, num_questions)
            else:
                return self._generate_questions_local(context, num_questions)
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return self._fallback_questions(context, num_questions)
    
    def _generate_questions_api(self, context, num_questions):
        """Generate questions using Hugging Face API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        # Use a question generation model
        model_url = f"{self.base_url}/valhalla/t5-small-qg-hl"
        
        payload = {
            "inputs": context,
            "parameters": {
                "max_length": 64,
                "num_return_sequences": num_questions
            }
        }
        
        response = requests.post(model_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            results = response.json()
            questions = []
            
            for result in results:
                if isinstance(result, dict) and 'generated_text' in result:
                    question = result['generated_text'].strip()
                    if question and question.endswith('?'):
                        questions.append({
                            'question': question,
                            'options': self._generate_options(context, question),
                            'correct_answer': 0  # First option is correct by default
                        })
            
            return questions[:num_questions]
        else:
            logger.error(f"API request failed: {response.status_code}")
            return self._generate_questions_local(context, num_questions)
    
    def _generate_questions_local(self, context, num_questions):
        """Generate questions using local pipeline."""
        if not self.qa_pipeline:
            return self._fallback_questions(context, num_questions)
        
        # Simple question templates
        question_templates = [
            "What is {}?",
            "How does {} work?",
            "Why is {} important?",
            "When should you use {}?",
            "What are the benefits of {}?"
        ]
        
        # Extract key terms from context (simple approach)
        words = context.split()
        key_terms = [word.strip('.,!?;:') for word in words if len(word) > 5]
        
        questions = []
        for i, template in enumerate(question_templates[:num_questions]):
            if i < len(key_terms):
                question = template.format(key_terms[i])
                questions.append({
                    'question': question,
                    'options': self._generate_options(context, question),
                    'correct_answer': 0
                })
        
        return questions
    
    def _generate_options(self, context, question):
        """Generate multiple choice options for a question."""
        # Simple option generation - in production, use more sophisticated methods
        words = context.split()
        options = []
        
        # Try to extract a relevant answer from context
        if self.qa_pipeline:
            try:
                result = self.qa_pipeline(question=question, context=context)
                correct_answer = result['answer']
                options.append(correct_answer)
            except:
                options.append("Answer from context")
        else:
            options.append("Answer from context")
        
        # Add some plausible distractors
        distractors = [
            "Alternative option A",
            "Alternative option B", 
            "Alternative option C"
        ]
        
        options.extend(distractors[:3])
        return options[:4]
    
    def _fallback_questions(self, context, num_questions):
        """Generate fallback questions when AI services are unavailable."""
        fallback_questions = [
            {
                'question': 'What is the main topic discussed in this content?',
                'options': ['Topic A', 'Topic B', 'Topic C', 'Topic D'],
                'correct_answer': 0
            },
            {
                'question': 'Which concept is most important in this material?',
                'options': ['Concept 1', 'Concept 2', 'Concept 3', 'Concept 4'],
                'correct_answer': 0
            },
            {
                'question': 'What should you remember from this content?',
                'options': ['Key point 1', 'Key point 2', 'Key point 3', 'Key point 4'],
                'correct_answer': 0
            }
        ]
        
        return fallback_questions[:num_questions]

def format_response(data, message="Success", status_code=200):
    """Format API response consistently."""
    return {
        'status': 'success' if status_code < 400 else 'error',
        'message': message,
        'data': data,
        'status_code': status_code
    }, status_code

def format_error(message, status_code=400, details=None):
    """Format error response consistently."""
    response = {
        'status': 'error',
        'message': message,
        'status_code': status_code
    }
    
    if details:
        response['details'] = details
    
    return response, status_code

def paginate_query(query, page, per_page):
    """Paginate SQLAlchemy query results."""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in items],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total
    }
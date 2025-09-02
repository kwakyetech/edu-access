from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import RequestEntityTooLarge
from models import User
from utils import allowed_file, save_file, delete_file, format_response, format_error
from security import limiter, check_file_security, InputSanitizer, log_security_event
import os

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload', methods=['POST'])
@jwt_required()
@limiter.limit("20 per hour")
def upload_file():
    """Upload a file to the server."""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return format_error('No file provided', 400)
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return format_error('No file selected', 400)
        
        # Validate file upload
        try:
            safe_filename = check_file_security(file)
        except Exception as e:
            log_security_event('file_upload_rejected', {
                'user_id': int(get_jwt_identity()),
                'filename': file.filename,
                'reason': str(e)
            })
            return format_error(str(e), 400)
        
        # Get current user
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.query.get(current_user_id)
        if not user:
            return format_error('User not found', 404)
        
        # Save file with sanitized filename
        original_filename = file.filename
        file.filename = InputSanitizer.sanitize_filename(file.filename)
        filename, file_path = save_file(file)
        
        if not filename:
            return format_error('Failed to save file', 500)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown'
        
        # Log successful upload
        log_security_event('file_uploaded', {
            'user_id': current_user_id,
            'filename': filename,
            'original_filename': original_filename,
            'file_size': file_size
        })
        
        # Return file information
        file_info = {
            'filename': filename,
            'original_filename': original_filename,
            'file_type': file_type,
            'file_size': file_size,
            'file_url': f'/api/files/download/{filename}',
            'uploaded_by': user.username,
            'upload_date': 'now'  # You might want to store this in database
        }
        
        return format_response(file_info, 'File uploaded successfully', 201)
        
    except RequestEntityTooLarge:
        max_size = current_app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)  # Convert to MB
        return format_error(f'File too large. Maximum size allowed: {max_size}MB', 413)
    except Exception as e:
        current_app.logger.error(f'File upload error: {str(e)}')
        return format_error('Internal server error during file upload', 500)

@files_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from the server."""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Check if file exists
        file_path = os.path.join(upload_folder, filename)
        if not os.path.exists(file_path):
            return format_error('File not found', 404)
        
        return send_from_directory(upload_folder, filename, as_attachment=True)
        
    except Exception as e:
        current_app.logger.error(f'File download error: {str(e)}')
        return format_error('Internal server error during file download', 500)

@files_bp.route('/view/<filename>', methods=['GET'])
def view_file(filename):
    """View a file in the browser (for images, PDFs, etc.)."""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Check if file exists
        file_path = os.path.join(upload_folder, filename)
        if not os.path.exists(file_path):
            return format_error('File not found', 404)
        
        return send_from_directory(upload_folder, filename)
        
    except Exception as e:
        current_app.logger.error(f'File view error: {str(e)}')
        return format_error('Internal server error during file view', 500)

@files_bp.route('/delete/<filename>', methods=['DELETE'])
@jwt_required()
def delete_file_endpoint(filename):
    """Delete a file from the server."""
    try:
        # Get current user
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.query.get(current_user_id)
        if not user:
            return format_error('User not found', 404)
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return format_error('File not found', 404)
        
        # Delete the file
        delete_file(filename)
        
        return format_response({'filename': filename}, 'File deleted successfully', 200)
        
    except Exception as e:
        current_app.logger.error(f'File deletion error: {str(e)}')
        return format_error('Internal server error during file deletion', 500)

@files_bp.route('/info/<filename>', methods=['GET'])
def get_file_info(filename):
    """Get information about a file."""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return format_error('File not found', 404)
        
        # Get file stats
        file_stats = os.stat(file_path)
        file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
        
        file_info = {
            'filename': filename,
            'file_type': file_type,
            'file_size': file_stats.st_size,
            'created_date': file_stats.st_ctime,
            'modified_date': file_stats.st_mtime,
            'download_url': f'/api/files/download/{filename}',
            'view_url': f'/api/files/view/{filename}'
        }
        
        return format_response(file_info, 'File information retrieved successfully', 200)
        
    except Exception as e:
        current_app.logger.error(f'File info error: {str(e)}')
        return format_error('Internal server error while getting file info', 500)

@files_bp.route('/list', methods=['GET'])
@jwt_required()
def list_files():
    """List all uploaded files (admin only or user's own files)."""
    try:
        # Get current user
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.query.get(current_user_id)
        if not user:
            return format_error('User not found', 404)
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Check if upload folder exists
        if not os.path.exists(upload_folder):
            return format_response([], 'No files found', 200)
        
        # Get all files in upload folder
        files = []
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                file_stats = os.stat(file_path)
                file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
                
                files.append({
                    'filename': filename,
                    'file_type': file_type,
                    'file_size': file_stats.st_size,
                    'created_date': file_stats.st_ctime,
                    'download_url': f'/api/files/download/{filename}',
                    'view_url': f'/api/files/view/{filename}'
                })
        
        return format_response(files, f'Found {len(files)} files', 200)
        
    except Exception as e:
        current_app.logger.error(f'File listing error: {str(e)}')
        return format_error('Internal server error while listing files', 500)
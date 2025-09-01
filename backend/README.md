# EduAccess Backend

A Flask-based REST API backend for the EduAccess educational platform, featuring AI-powered quiz generation using Hugging Face APIs.

## Features

- **User Authentication**: JWT-based authentication with registration, login, and profile management
- **Notes Management**: CRUD operations for study notes with tagging and search
- **AI-Powered Quizzes**: Automatic quiz generation using Hugging Face question-answering models
- **Past Questions**: Upload, manage, and download past exam papers
- **Leaderboard**: User ranking system based on quiz performance
- **Dashboard Analytics**: User statistics and performance tracking
- **File Upload**: Secure file handling for documents and images
- **Rate Limiting**: API protection against abuse
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Technology Stack

- **Framework**: Flask 3.1.2
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **AI Integration**: Hugging Face Transformers
- **File Storage**: Local filesystem (configurable for cloud storage)
- **Environment**: Python 3.8+

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
cd edu-access/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:
   ```env
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-super-secret-key-change-this-in-production
   
   # JWT Configuration
   JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
   
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=eduaccess
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   
   # Hugging Face Configuration
   HUGGINGFACE_API_TOKEN=your-huggingface-api-token
   ```

### 5. Database Setup

1. Create MySQL database:
   ```sql
   CREATE DATABASE eduaccess CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Initialize database tables and sample data:
   ```bash
   python init_db.py
   ```

## Running the Application

### Development Server

```bash
python run.py
```

The server will start at `http://127.0.0.1:5000`

### Production Server

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password

### Notes
- `GET /api/notes` - Get all notes (with pagination and filtering)
- `POST /api/notes` - Create new note
- `GET /api/notes/<id>` - Get specific note
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note
- `GET /api/notes/subjects` - Get unique subjects
- `GET /api/notes/stats` - Get notes statistics

### Quizzes
- `GET /api/quiz` - Get all quizzes
- `POST /api/quiz/generate` - Generate AI-powered quiz
- `POST /api/quiz` - Create manual quiz
- `GET /api/quiz/<id>` - Get specific quiz
- `POST /api/quiz/<id>/attempt` - Submit quiz attempt
- `GET /api/quiz/attempts` - Get user's quiz attempts

### Past Questions
- `GET /api/past-questions` - Get all past questions
- `POST /api/past-questions` - Upload past question
- `GET /api/past-questions/<id>` - Get specific past question
- `PUT /api/past-questions/<id>` - Update past question
- `DELETE /api/past-questions/<id>` - Delete past question
- `GET /api/past-questions/<id>/download` - Download file

### Leaderboard
- `GET /api/leaderboard` - Get leaderboard
- `GET /api/leaderboard/top` - Get top users
- `GET /api/leaderboard/user/<id>` - Get user rank
- `GET /api/leaderboard/me` - Get current user's rank

### Dashboard
- `GET /api/dashboard/overview` - Dashboard overview
- `GET /api/dashboard/activity` - Activity timeline
- `GET /api/dashboard/quiz-performance` - Quiz performance stats
- `GET /api/dashboard/notes-analytics` - Notes analytics

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Flask secret key | Required |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_NAME` | Database name | `eduaccess` |
| `DB_USER` | Database username | Required |
| `DB_PASSWORD` | Database password | Required |
| `HUGGINGFACE_API_TOKEN` | Hugging Face API token | Optional |
| `UPLOAD_FOLDER` | File upload directory | `uploads` |
| `MAX_CONTENT_LENGTH` | Max file size (bytes) | `16777216` (16MB) |

### Hugging Face Integration

The application uses Hugging Face models for AI-powered quiz generation:

1. **With API Token**: Uses Hugging Face Inference API for better performance
2. **Without API Token**: Falls back to local transformers pipeline
3. **Fallback Mode**: Uses predefined question templates if AI services fail

To get a Hugging Face API token:
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to Settings > Access Tokens
3. Create a new token with read permissions
4. Add it to your `.env` file

## Development

### Project Structure

```
backend/
├── app.py              # Flask application factory
├── models.py           # SQLAlchemy database models
├── config.py           # Configuration classes
├── utils.py            # Utility functions and AI integration
├── run.py              # Application entry point
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── routes/             # API route modules
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── notes.py        # Notes management routes
│   ├── quiz.py         # Quiz and AI routes
│   ├── past_questions.py # Past questions routes
│   ├── leaderboard.py  # Leaderboard routes
│   └── dashboard.py    # Dashboard analytics routes
└── uploads/            # File upload directory (created automatically)
```

### Adding New Features

1. **New Model**: Add to `models.py`
2. **New Routes**: Create new file in `routes/` directory
3. **New Utilities**: Add to `utils.py`
4. **Database Changes**: Update `init_db.py` and run migration

### Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## Deployment

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

### Production Considerations

1. **Security**: Change default secret keys
2. **Database**: Use connection pooling and SSL
3. **File Storage**: Consider cloud storage (AWS S3, etc.)
4. **Monitoring**: Add logging and error tracking
5. **Caching**: Implement Redis for session storage
6. **Load Balancing**: Use nginx or similar reverse proxy

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check MySQL service is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Import Errors**:
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **File Upload Issues**:
   - Check `uploads/` directory permissions
   - Verify `MAX_CONTENT_LENGTH` setting

4. **AI Features Not Working**:
   - Check Hugging Face API token
   - Verify internet connection for API calls
   - Check transformers library installation

### Logs

Application logs are written to `app.log` in the backend directory. Check this file for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License.
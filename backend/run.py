#!/usr/bin/env python3
"""
Main entry point for the EduAccess Flask application.
This script starts the development server.
"""

import os
from app import create_app
from config import config

# Get configuration from environment variable or default to development
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask application
app = create_app(config_name)

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting EduAccess backend server...")
    print(f"Environment: {config_name}")
    print(f"Server: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print("Press Ctrl+C to stop the server")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
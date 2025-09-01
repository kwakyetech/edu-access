#!/usr/bin/env python3
"""
MySQL Database Setup Script for EduAccess

This script creates a MySQL database and user for the EduAccess application.
Run this script before initializing the database with init_db.py
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """
    Create MySQL database and user for EduAccess
    """
    try:
        # Database configuration
        db_config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': int(os.environ.get('DB_PORT', 3306)),
            'user': 'root',  # Use root to create database and user
            'password': input("Enter MySQL root password: ")
        }
        
        # Target database configuration
        target_db = os.environ.get('DB_NAME', 'eduaccess')
        target_user = os.environ.get('DB_USER', 'eduaccess_user')
        target_password = os.environ.get('DB_PASSWORD', 'eduaccess_password')
        
        print(f"Connecting to MySQL server at {db_config['host']}:{db_config['port']}...")
        
        # Connect to MySQL server
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        print("Connected successfully!")
        
        # Create database
        print(f"Creating database '{target_db}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {target_db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{target_db}' created successfully!")
        
        # Create user and grant privileges
        print(f"Creating user '{target_user}'...")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{target_user}'@'localhost' IDENTIFIED BY '{target_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {target_db}.* TO '{target_user}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print(f"User '{target_user}' created and granted privileges successfully!")
        
        # Test connection with new user
        print("Testing connection with new user...")
        test_config = {
            'host': db_config['host'],
            'port': db_config['port'],
            'user': target_user,
            'password': target_password,
            'database': target_db
        }
        
        test_connection = mysql.connector.connect(**test_config)
        test_cursor = test_connection.cursor()
        test_cursor.execute("SELECT 1")
        result = test_cursor.fetchone()
        
        if result[0] == 1:
            print("✅ Database setup completed successfully!")
            print(f"\nDatabase Details:")
            print(f"  Host: {db_config['host']}")
            print(f"  Port: {db_config['port']}")
            print(f"  Database: {target_db}")
            print(f"  User: {target_user}")
            print(f"\nYou can now run 'python init_db.py' to initialize the database schema.")
        
        test_cursor.close()
        test_connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")
        if "Access denied" in str(e):
            print("\nTroubleshooting:")
            print("1. Make sure MySQL server is running")
            print("2. Check if the root password is correct")
            print("3. Ensure MySQL is accessible from localhost")
        return False
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
    return True

def check_mysql_connection():
    """
    Check if MySQL server is accessible
    """
    try:
        root_password = input("Enter MySQL root password to test connection: ")
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 3306)),
            user='root',
            password=root_password
        )
        connection.close()
        print("✅ MySQL connection successful!")
        return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("EduAccess MySQL Database Setup")
    print("=" * 50)
    print()
    
    print("This script will:")
    print("1. Create a MySQL database for EduAccess")
    print("2. Create a database user with appropriate privileges")
    print("3. Test the database connection")
    print()
    
    # Check if MySQL is accessible
    if not check_mysql_connection():
        print("\nPlease ensure MySQL server is running and try again.")
        exit(1)
    
    # Create database
    if create_database():
        print("\n🎉 MySQL database setup completed successfully!")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")
        exit(1)
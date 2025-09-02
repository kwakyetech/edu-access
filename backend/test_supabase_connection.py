#!/usr/bin/env python3
"""
Supabase Connection Test Script

This script tests the database connection to Supabase PostgreSQL.
Run this after setting up your Supabase credentials to verify the connection.

Usage:
    python test_supabase_connection.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test the database connection to Supabase."""
    
    print("🔍 Testing Supabase PostgreSQL connection...")
    print("=" * 50)
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Try to construct from individual components
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT', '5432')
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD')
        db_name = os.environ.get('DB_NAME', 'postgres')
        
        if not all([db_host, db_password]):
            print("❌ Error: Missing database configuration!")
            print("\nPlease set either:")
            print("1. DATABASE_URL environment variable, or")
            print("2. DB_HOST, DB_PASSWORD (and optionally DB_PORT, DB_USER, DB_NAME)")
            print("\nExample .env file:")
            print("DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres")
            print("\nOr:")
            print("DB_HOST=db.xxx.supabase.co")
            print("DB_PASSWORD=your-password")
            return False
        
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"📡 Connecting to: {database_url.replace(database_url.split(':')[2].split('@')[0], '***')}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            # Test basic connection
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            
            # Test database info
            result = connection.execute(text("SELECT current_database(), current_user;"))
            db_info = result.fetchone()
            print(f"🗄️  Database: {db_info[0]}")
            print(f"👤 User: {db_info[1]}")
            
            # Test table creation (and cleanup)
            print("\n🧪 Testing table operations...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id SERIAL PRIMARY KEY,
                    test_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            connection.commit()
            
            # Insert test data
            connection.execute(text("""
                INSERT INTO connection_test (test_message) 
                VALUES ('Supabase connection test successful!');
            """))
            connection.commit()
            
            # Read test data
            result = connection.execute(text("""
                SELECT test_message, created_at FROM connection_test 
                ORDER BY created_at DESC LIMIT 1;
            """))
            test_data = result.fetchone()
            print(f"✅ Table operations successful!")
            print(f"📝 Test message: {test_data[0]}")
            print(f"⏰ Created at: {test_data[1]}")
            
            # Cleanup
            connection.execute(text("DROP TABLE connection_test;"))
            connection.commit()
            print("🧹 Cleanup completed")
            
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Supabase connection is working correctly.")
        print("\n📋 Next steps:")
        print("1. Run: python init_db.py (to create application tables)")
        print("2. Run: python seed_data.py (to add sample data)")
        print("3. Start the application: python run.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your Supabase project is active")
        print("2. Verify your database password")
        print("3. Ensure your IP is allowed (Supabase allows all by default)")
        print("4. Check your .env file configuration")
        print("\n📖 See SUPABASE_MIGRATION.md for detailed setup instructions")
        
        return False

def main():
    """Main function."""
    print("🚀 EduAccess Supabase Connection Tester")
    print("\nThis script will test your Supabase PostgreSQL connection.")
    print("Make sure you have configured your .env file first.\n")
    
    success = test_connection()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
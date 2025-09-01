# MySQL Database Setup Guide for EduAccess

This guide will help you set up a separate MySQL database for the EduAccess backend application.

## Prerequisites

### 1. Install MySQL Server

#### Option A: MySQL Community Server (Recommended)
1. Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
2. Run the installer and follow the setup wizard
3. During installation:
   - Choose "Server only" or "Developer Default"
   - Set a strong root password (remember this!)
   - Configure MySQL to start as a Windows service
   - Use default port 3306

#### Option B: XAMPP (Easier for beginners)
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP and start the MySQL service from the control panel
3. Default root password is empty (no password)

#### Option C: MySQL with Docker
```bash
docker run --name mysql-eduaccess -e MYSQL_ROOT_PASSWORD=your_root_password -p 3306:3306 -d mysql:8.0
```

### 2. Verify MySQL Installation

Open Command Prompt or PowerShell and test the connection:
```bash
mysql -u root -p
```
Enter your root password when prompted. If successful, you'll see the MySQL prompt.

## Database Setup

### Step 1: Run the MySQL Setup Script

Navigate to the backend directory and run:
```bash
cd edu-access/backend
python setup_mysql.py
```

This script will:
- Create the `eduaccess` database
- Create a dedicated user `eduaccess_user` with appropriate privileges
- Test the database connection

### Step 2: Initialize Database Schema

After the MySQL setup is complete, initialize the database tables:
```bash
python init_db.py
```

This will create all the necessary tables and populate them with sample data.

### Step 3: Start the Flask Application

Restart the Flask server to use the new MySQL database:
```bash
python run.py
```

## Configuration Details

The application is configured to use the following MySQL settings:

- **Host**: localhost
- **Port**: 3306
- **Database**: eduaccess
- **Username**: eduaccess_user
- **Password**: eduaccess_password

These settings are defined in the `.env` file and can be modified if needed.

## Troubleshooting

### Common Issues

#### 1. "Access denied for user 'root'@'localhost'"
- Verify your MySQL root password
- Ensure MySQL server is running
- Try resetting the root password

#### 2. "Can't connect to MySQL server"
- Check if MySQL service is running:
  - Windows: Services → MySQL80 (or similar)
  - XAMPP: Start MySQL from control panel
- Verify the port (default: 3306) is not blocked

#### 3. "Unknown database 'eduaccess'"
- Run the `setup_mysql.py` script first
- Manually create the database:
  ```sql
  CREATE DATABASE eduaccess CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

#### 4. "Table doesn't exist" errors
- Run `python init_db.py` to create the database schema
- Check if the database connection is working

### Manual Database Setup (Alternative)

If the automated script doesn't work, you can set up the database manually:

1. Connect to MySQL as root:
   ```bash
   mysql -u root -p
   ```

2. Create the database:
   ```sql
   CREATE DATABASE eduaccess CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Create the user:
   ```sql
   CREATE USER 'eduaccess_user'@'localhost' IDENTIFIED BY 'eduaccess_password';
   GRANT ALL PRIVILEGES ON eduaccess.* TO 'eduaccess_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Test the connection:
   ```bash
   mysql -u eduaccess_user -p eduaccess
   ```

## Security Considerations

### For Production

1. **Change default passwords**: Update the database password in `.env`
2. **Use environment variables**: Don't commit sensitive data to version control
3. **Limit user privileges**: Create users with minimal required permissions
4. **Enable SSL**: Configure MySQL to use SSL connections
5. **Regular backups**: Set up automated database backups

### Database Backup

Create a backup of your database:
```bash
mysqldump -u eduaccess_user -p eduaccess > eduaccess_backup.sql
```

Restore from backup:
```bash
mysql -u eduaccess_user -p eduaccess < eduaccess_backup.sql
```

## Database Schema Overview

The EduAccess database includes the following tables:

- **users**: User accounts and profiles
- **notes**: Study notes and materials
- **quizzes**: Quiz definitions and questions
- **quiz_attempts**: User quiz attempts and scores
- **past_questions**: Past examination papers
- **leaderboard**: User rankings and statistics

## Next Steps

After setting up MySQL:

1. ✅ MySQL server installed and running
2. ✅ Database and user created
3. ✅ Database schema initialized
4. ✅ Flask application connected to MySQL
5. 🔄 Test the authentication endpoints
6. 🔄 Implement remaining API features

## Support

If you encounter issues:

1. Check the Flask application logs
2. Verify MySQL server status
3. Test database connectivity
4. Review the configuration in `.env` file

For additional help, refer to the main README.md file or check the MySQL documentation.
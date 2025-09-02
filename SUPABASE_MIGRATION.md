# Supabase Migration Guide

This guide will help you migrate from MySQL to Supabase PostgreSQL for the EduAccess application.

## Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in to your account
3. Click "New Project"
4. Choose your organization
5. Fill in project details:
   - **Name**: EduAccess
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to your users
6. Click "Create new project"
7. Wait for project initialization (2-3 minutes)

## Step 2: Get Database Connection Details

1. In your Supabase dashboard, go to **Settings** > **Database**
2. Scroll down to **Connection info**
3. Copy the following details:
   - **Host**: `db.[your-project-ref].supabase.co`
   - **Database name**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: The password you set during project creation

## Step 3: Configure Environment Variables

### Option A: Using .env file (Recommended for local development)

Create a `.env` file in the root directory:

```bash
# Supabase Database Configuration
SUPABASE_DB_HOST=db.[YOUR-PROJECT-REF].supabase.co
SUPABASE_DB_PASSWORD=[YOUR-DATABASE-PASSWORD]

# Flask Security Keys (Generate strong random keys)
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Hugging Face API Token (Optional)
HUGGINGFACE_API_TOKEN=your-huggingface-token-here
```

### Option B: Using backend .env file

Create a `.env` file in the `backend` directory:

```bash
# Supabase Database Configuration
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# Alternative format
DB_HOST=db.[YOUR-PROJECT-REF].supabase.co
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=[YOUR-PASSWORD]
DB_NAME=postgres

# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=pdf,doc,docx,txt,png,jpg,jpeg

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Hugging Face Configuration (optional)
HUGGINGFACE_API_TOKEN=your-huggingface-token-here
```

## Step 4: Install PostgreSQL Dependencies

The dependencies have already been updated in `requirements.txt`. If running locally:

```bash
cd backend
pip install -r requirements.txt
```

## Step 5: Test Database Connection

### Option A: Using Docker (Recommended)

```bash
# Build and start services
docker-compose up --build -d

# Check if backend is healthy
docker-compose ps

# View backend logs
docker-compose logs backend
```

### Option B: Local Development

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test connection
python -c "from app import create_app; app = create_app(); print('Database connection successful!')"
```

## Step 6: Initialize Database Schema

```bash
# Using Docker
docker-compose exec backend python init_db.py

# Or locally
cd backend
python init_db.py
```

## Step 7: Seed Database with Sample Data

```bash
# Using Docker
docker-compose exec backend python seed_data.py

# Or locally
cd backend
python seed_data.py
```

## Step 8: Verify Migration

1. Check that the application starts without errors
2. Visit http://localhost:3000 (frontend)
3. Visit http://localhost:5000/api/health (backend health check)
4. Try logging in with sample credentials:
   - Email: `john@example.com`
   - Password: `Password123!`

## Troubleshooting

### Connection Issues

1. **"Connection refused"**: Check your Supabase project is active and connection details are correct
2. **"Authentication failed"**: Verify your database password
3. **"SSL required"**: Supabase requires SSL connections (handled automatically by psycopg2)

### Environment Variable Issues

1. Make sure `.env` file is in the correct location
2. Restart Docker containers after changing environment variables:
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

### Database Schema Issues

1. If tables don't exist, run:
   ```bash
   docker-compose exec backend python init_db.py
   ```

2. If you get "relation does not exist" errors, the schema wasn't created properly

## Supabase Dashboard Features

Once connected, you can use Supabase dashboard to:

1. **Table Editor**: View and edit data directly
2. **SQL Editor**: Run custom queries
3. **Database**: Monitor connections and performance
4. **Auth**: Manage user authentication (if using Supabase Auth)
5. **Storage**: File storage (alternative to local uploads)

## Next Steps

1. **Production Deployment**: Update production environment variables
2. **Backup Strategy**: Set up automated backups in Supabase
3. **Monitoring**: Use Supabase monitoring tools
4. **Scaling**: Configure connection pooling if needed

## Benefits of Supabase Migration

- ✅ No local database setup required
- ✅ Automatic backups and point-in-time recovery
- ✅ Built-in monitoring and analytics
- ✅ Scalable PostgreSQL database
- ✅ Real-time subscriptions (if needed)
- ✅ Built-in authentication system (optional)
- ✅ File storage capabilities
- ✅ Free tier available for development

## Support

If you encounter issues:
1. Check Supabase documentation: https://supabase.com/docs
2. Review application logs: `docker-compose logs backend`
3. Test database connection in Supabase dashboard
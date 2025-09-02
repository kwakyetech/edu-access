# EduAccess Deployment Guide

This guide provides instructions for deploying the EduAccess application using Docker and Docker Compose with Supabase PostgreSQL database.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Git
- Supabase account and project (https://supabase.com)
- At least 2GB of available RAM
- At least 5GB of available disk space

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd edu-access
```

### 2. Supabase Setup

1. Go to [Supabase](https://supabase.com) and create a new project
2. Wait for the project to be fully initialized
3. Go to Settings > Database
4. Copy your database connection details

### 3. Environment Configuration

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

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

#### Frontend Environment (.env.frontend)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api

# App Configuration
VITE_APP_NAME=EduAccess
VITE_APP_VERSION=1.0.0
```

### 4. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Initialize Database and Seed Data

```bash
# Wait for services to be healthy (about 1-2 minutes)
docker-compose exec backend python init_db.py

# Seed the database with sample data
docker-compose exec backend python seed_data.py
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Health Check**: http://localhost:5000/api/health
- **Supabase Dashboard**: https://supabase.com/dashboard/projects

## Sample Login Credentials

After seeding the database, you can use these credentials:

- **Admin**: admin@eduaccess.com / Admin123!
- **User**: john@example.com / Password123!
- **Student**: student1@example.com / Student123!

## Production Deployment

### 1. Security Considerations

**Important**: Before deploying to production, make sure to:

1. Change all default passwords and secret keys
2. Use strong, randomly generated secrets
3. Enable HTTPS with SSL certificates
4. Configure proper firewall rules
5. Set up regular database backups
6. Enable logging and monitoring

### 2. Environment Variables for Production

Update the environment variables in `docker-compose.yml` or use separate `.env` files:

```bash
# Generate strong secrets
openssl rand -hex 32  # For JWT_SECRET_KEY
openssl rand -hex 32  # For SECRET_KEY
```

### 3. SSL/HTTPS Configuration

For production, configure SSL certificates:

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update nginx configuration
3. Redirect HTTP to HTTPS

### 4. Database Backup

Set up automated database backups:

```bash
# Manual backup
docker-compose exec mysql mysqldump -u root -p eduaccess > backup.sql

# Restore from backup
docker-compose exec -i mysql mysql -u root -p eduaccess < backup.sql
```

## Development Setup

For development without Docker:

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
export FLASK_ENV=development
export DATABASE_URL=mysql+pymysql://user:password@localhost:3306/eduaccess

# Initialize database
python init_db.py
python seed_data.py

# Run development server
python run.py
```

### Frontend Development

```bash
npm install
npm run dev
```

## Troubleshooting

### Common Issues

1. **Services not starting**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

2. **Database connection issues**:
   - Check if MySQL container is healthy
   - Verify database credentials
   - Wait for MySQL to fully initialize (2-3 minutes)

3. **Port conflicts**:
   - Change ports in `docker-compose.yml` if needed
   - Check for other services using ports 3000, 5000, or 3306

4. **Permission issues**:
   ```bash
   sudo chown -R $USER:$USER uploads/
   ```

### Useful Commands

```bash
# View service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql

# Restart specific service
docker-compose restart backend

# Access container shell
docker-compose exec backend bash
docker-compose exec mysql mysql -u root -p

# Clean up
docker-compose down -v  # Removes volumes (data will be lost)
docker system prune     # Clean up unused Docker resources
```

## Monitoring and Maintenance

### Health Checks

All services include health checks. Monitor them with:

```bash
docker-compose ps
```

### Log Management

Configure log rotation to prevent disk space issues:

```bash
# View log sizes
docker-compose logs --tail=0 backend | wc -l

# Rotate logs
docker-compose restart
```

### Performance Monitoring

Monitor resource usage:

```bash
docker stats
```

## Scaling

For high-traffic scenarios:

1. **Database**: Use MySQL replication or clustering
2. **Backend**: Scale horizontally with load balancer
3. **Frontend**: Use CDN for static assets
4. **Caching**: Add Redis for session storage and caching

```bash
# Scale backend service
docker-compose up --scale backend=3
```

## Support

For issues and questions:

1. Check the logs first
2. Review this deployment guide
3. Check the application documentation
4. Create an issue in the repository

## Security Checklist

- [ ] Changed all default passwords
- [ ] Generated strong secret keys
- [ ] Configured HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Enabled security headers
- [ ] Configured rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configured automated backups
- [ ] Reviewed and updated dependencies
- [ ] Implemented proper logging
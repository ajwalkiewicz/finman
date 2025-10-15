# Data

Directory for default environmental variables and database

## Database

Sqlite `finance_manager.db`

## Environmental variables

### Security - CHANGE THESE IN PRODUCTION
SECRET_KEY=<your-secret-key>
FIXER_API_KEY=<fixer-api-key>

### Database settings
DATABASE_URL=sqlite:////app/data/finance_manager.db

### JWT settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

### Redis settings  
REDIS_HOST=redis
REDIS_PORT=6379

### Environment
ENVIRONMENT=production|development
USER_REGISTRATION=true|false
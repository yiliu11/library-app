export const env = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  PORT: process.env.PORT || 3001,
  DB_HOST: process.env.DB_HOST || 'localhost',
  DB_PORT: parseInt(process.env.DB_PORT || '5432'),
  DB_USERNAME: process.env.DB_USERNAME || 'postgres',
  DB_PASSWORD: process.env.DB_PASSWORD || 'postgres',
  DB_NAME: process.env.DB_NAME || 'library_book_service',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
  USER_SERVICE_URL: process.env.USER_SERVICE_URL || 'http://localhost:3000',
};

export const env = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  PORT: process.env.PORT || 3004,
  DB_HOST: process.env.DB_HOST || 'localhost',
  DB_PORT: parseInt(process.env.DB_PORT || '5432'),
  DB_USERNAME: process.env.DB_USERNAME || 'postgres',
  DB_PASSWORD: process.env.DB_PASSWORD || 'postgres',
  DB_NAME: process.env.DB_NAME || 'library_notification_service',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',

  // Email configuration
  SMTP_HOST: process.env.SMTP_HOST || 'smtp.example.com',
  SMTP_PORT: parseInt(process.env.SMTP_PORT || '587'),
  SMTP_USER: process.env.SMTP_USER || 'user@example.com',
  SMTP_PASSWORD: process.env.SMTP_PASSWORD || 'password',
  EMAIL_FROM: process.env.EMAIL_FROM || 'noreply@library.com',

  // Retry policy
  MAX_RETRIES: parseInt(process.env.MAX_RETRIES || '3'),
  RETRY_DELAY_MS: parseInt(process.env.RETRY_DELAY_MS || '5000'),
};

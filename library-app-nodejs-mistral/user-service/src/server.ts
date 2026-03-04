import { pool } from './config/db';
import { createUsersTable } from './models/user.model';
import app from './app';
import { logger } from './utils/logger';

const initializeDatabase = async () => {
  try {
    await pool.query(createUsersTable);
    logger.info('Database initialized');
  } catch (err) {
    logger.error(`Database initialization failed: ${err}`);
    process.exit(1);
  }
};

initializeDatabase();

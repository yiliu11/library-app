// Export all models and database utilities
export * from './user.model';

// Export database initialization function
import { query } from '../config/db';
import { createUsersTable } from './user.model';
import { logger } from '../utils/logger';

/**
 * Initializes the database by creating tables if they don't exist.
 */
export const initializeDatabase = async (): Promise<void> => {
  try {
    // Create users table
    await query(createUsersTable);
    logger.info('Database tables initialized successfully');
  } catch (err) {
    logger.error(`Failed to initialize database tables: ${err}`);
    throw err;
  }
};

/**
 * Drops all tables in the database (for testing purposes only).
 * WARNING: This will delete all data!
 */
export const dropAllTables = async (): Promise<void> => {
  try {
    await query('DROP TABLE IF EXISTS users CASCADE');
    logger.info('All tables dropped successfully');
  } catch (err) {
    logger.error(`Failed to drop tables: ${err}`);
    throw err;
  }
};

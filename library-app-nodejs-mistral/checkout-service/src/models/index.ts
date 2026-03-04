export * from './checkout.model';
import { query } from '../config/db';
import { createCheckoutsTable, createUserRecordsView } from './checkout.model';
import { logger } from '../utils/logger';

/**
 * Initializes the database by creating tables if they don't exist.
 */
export const initializeDatabase = async (): Promise<void> => {
  try {
    await query(createCheckoutsTable);
    await query(createUserRecordsView);
    logger.info('Database tables and views initialized successfully');
  } catch (err) {
    logger.error(`Failed to initialize database: ${err}`);
    throw err;
  }
};

/**
 * Drops all tables in the database (for testing purposes only).
 * WARNING: This will delete all data!
 */
export const dropAllTables = async (): Promise<void> => {
  try {
    await query('DROP TABLE IF EXISTS checkouts CASCADE');
    logger.info('All tables dropped successfully');
  } catch (err) {
    logger.error(`Failed to drop tables: ${err}`);
    throw err;
  }
};

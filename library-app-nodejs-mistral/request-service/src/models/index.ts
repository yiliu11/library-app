export * from './request.model';
import { query } from '../config/db';
import { createRequestsTable } from './request.model';
import { logger } from '../utils/logger';

/**
 * Initializes the database by creating tables if they don't exist.
 */
export const initializeDatabase = async (): Promise<void> => {
  try {
    await query(createRequestsTable);
    logger.info('Requests table initialized successfully');
  } catch (err) {
    logger.error(`Failed to initialize requests table: ${err}`);
    throw err;
  }
};

/**
 * Drops the requests table (for testing purposes only).
 * WARNING: This will delete all request data!
 */
export const dropRequestsTable = async (): Promise<void> => {
  try {
    await query('DROP TABLE IF EXISTS requests CASCADE');
    logger.info('Requests table dropped successfully');
  } catch (err) {
    logger.error(`Failed to drop requests table: ${err}`);
    throw err;
  }
};

export * from './book.model';
import { query } from '../config/db';
import { createBooksTable } from './book.model';
import { logger } from '../utils/logger';

/**
 * Initializes the database by creating tables if they don't exist.
 */
export const initializeDatabase = async (): Promise<void> => {
  try {
    await query(createBooksTable);
    logger.info('Books table initialized successfully');
  } catch (err) {
    logger.error(`Failed to initialize books table: ${err}`);
    throw err;
  }
};

/**
 * Drops the books table (for testing purposes only).
 * WARNING: This will delete all book data!
 */
export const dropBooksTable = async (): Promise<void> => {
  try {
    await query('DROP TABLE IF EXISTS books CASCADE');
    logger.info('Books table dropped successfully');
  } catch (err) {
    logger.error(`Failed to drop books table: ${err}`);
    throw err;
  }
};

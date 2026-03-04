export * from './notification.model';
import { query } from '../config/db';
import { createNotificationsTable } from './notification.model';
import { logger } from '../utils/logger';

/**
 * Initializes the database by creating tables if they don't exist.
 */
export const initializeDatabase = async (): Promise<void> => {
  try {
    await query(createNotificationsTable);
    logger.info('Notifications table initialized successfully');
  } catch (err) {
    logger.error(`Failed to initialize notifications table: ${err}`);
    throw err;
  }
};

/**
 * Drops the notifications table (for testing purposes only).
 * WARNING: This will delete all notification data!
 */
export const dropNotificationsTable = async (): Promise<void> => {
  try {
    await query('DROP TABLE IF EXISTS notifications CASCADE');
    logger.info('Notifications table dropped successfully');
  } catch (err) {
    logger.error(`Failed to drop notifications table: ${err}`);
    throw err;
  }
};

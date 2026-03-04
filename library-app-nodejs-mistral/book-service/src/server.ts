import app from './app';
import { initializeDatabase } from './models';
import { logger } from './utils/logger';
import { env } from './config/env';

const startServer = async () => {
  try {
    await initializeDatabase();
    app.listen(env.PORT, () => {
      logger.info(`Book Service running on port ${env.PORT}`);
    });
  } catch (err) {
    logger.error(`Failed to start server: ${err}`);
    process.exit(1);
  }
};

startServer();

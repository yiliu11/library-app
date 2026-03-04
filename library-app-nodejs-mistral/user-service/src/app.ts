import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import routes from './routes';
import { errorHandler } from './middlewares/error.middleware';
import { logger } from './utils/logger';
import { env } from './config/env';

const app = express();

// Middlewares
app.use(cors());
app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api', routes);

// Error handling
app.use(errorHandler);

app.listen(env.PORT, () => {
  logger.info(`User Service running on port ${env.PORT}`);
});

export default app;

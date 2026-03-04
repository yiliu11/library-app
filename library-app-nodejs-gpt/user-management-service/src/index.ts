// src/index.ts

import express from 'express';
import cors from 'cors';
import { env } from './config/env';
import userRoutes from './routes/user.routes';
import errorHandler from './middlewares/error.middleware';
import { prisma } from './config/prisma';

const app = express();

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/users', userRoutes);

// Healthcheck
app.get('/api/health', (_req, res) => res.json({ status: 'User Management Service healthy' }));

// Error handler
app.use(errorHandler);

// Start
const port = env.PORT;
app.listen(port, () => {
  console.log(`User Management Service running on port ${port}`);
});

// Graceful shutdown hook (optional)
process.on('SIGINT', async () => {
  console.log('Shutting down gracefully...');
  await prisma.$disconnect();
  process.exit(0);
});

// src/middlewares/error.middleware.ts

import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';
import { AppError } from '../utils/errors';
import { env } from '../config/env';

export default function errorHandler(err: any, _req: Request, res: Response, _next: NextFunction) {
  console.error('ERROR:', err);

  if (err instanceof ZodError) {
    const errors = err.errors.map(e => ({ path: e.path.join('.'), message: e.message }));
    return res.status(400).json({ message: 'Validation error', errors });
  }

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ message: err.message, details: err.details || undefined });
  }

  // Fallback
  const status = err?.statusCode || 500;
  const message = err?.message || 'Internal Server Error';

  const payload: any = { message };
  if (env.NODE_ENV !== 'production') payload.stack = err?.stack;
  res.status(status).json(payload);
}

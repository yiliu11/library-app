// src/middlewares/error.middleware.ts

import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

export const errorHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error('🔥 Error:', err);

  // Handle Zod validation errors
  if (err instanceof ZodError) {
    return res.status(400).json({
      message: 'Validation error',
      errors: err.errors.map(e => ({
        field: e.path.join('.'),
        message: e.message
      }))
    });
  }

  // Handle known errors with statusCode and message
  if (err.statusCode && err.message) {
    return res.status(err.statusCode).json({ message: err.message });
  }

  // Fallback for unexpected errors
  return res.status(500).json({ message: 'Internal Server Error' });
};

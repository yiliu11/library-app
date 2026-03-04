// src/utils/errors.ts

export class AppError extends Error {
  statusCode: number;
  details?: any;
  constructor(message: string, statusCode = 500, details?: any) {
    super(message);
    this.statusCode = statusCode;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }
}

export const BadRequest = (msg = 'Bad Request', details?: any) => new AppError(msg, 400, details);
export const Unauthorized = (msg = 'Unauthorized', details?: any) => new AppError(msg, 401, details);
export const Forbidden = (msg = 'Forbidden', details?: any) => new AppError(msg, 403, details);
export const NotFound = (msg = 'Not Found', details?: any) => new AppError(msg, 404, details);

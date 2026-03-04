import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';
import { env } from '../config/env';

/**
 * Custom error class for application-specific errors
 */
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational: boolean = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

/**
 * Error for bad client requests
 */
export class BadRequestError extends AppError {
  constructor(message: string = 'Bad Request') {
    super(400, message);
  }
}

/**
 * Error for unauthorized access
 */
export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(401, message);
  }
}

/**
 * Error for forbidden access
 */
export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(403, message);
  }
}

/**
 * Error for not found resources
 */
export class NotFoundError extends AppError {
  constructor(message: string = 'Not Found') {
    super(404, message);
  }
}

/**
 * Error for conflicts (e.g., duplicate resources)
 */
export class ConflictError extends AppError {
  constructor(message: string = 'Conflict') {
    super(409, message);
  }
}

/**
 * Error for internal server errors
 */
export class InternalServerError extends AppError {
  constructor(message: string = 'Internal Server Error') {
    super(500, message, false);
  }
}

/**
 * Error for service unavailable
 */
export class ServiceUnavailableError extends AppError {
  constructor(message: string = 'Service Unavailable') {
    super(503, message, false);
  }
}

/**
 * Global error handling middleware
 */
export const errorHandler = (
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // If the error is an instance of AppError, use its status code and message
  if (err instanceof AppError) {
    const { statusCode, message, isOperational } = err;

    // Log operational errors differently from programming errors
    if (isOperational) {
      logger.warn(`[${statusCode}] ${message}`);
    } else {
      logger.error(`[${statusCode}] ${message}`);
      if (env.NODE_ENV === 'development') {
        logger.error(err.stack);
      }
    }

    return res.status(statusCode).json({
      error: {
        message,
        statusCode,
        timestamp: new Date().toISOString(),
        path: req.path,
      },
    });
  }

  // For non-AppError instances (programming errors, etc.)
  logger.error(`[500] ${err.message}`);
  if (env.NODE_ENV === 'development') {
    logger.error(err.stack);
  }

  res.status(500).json({
    error: {
      message: 'Internal Server Error',
      statusCode: 500,
      timestamp: new Date().toISOString(),
      path: req.path,
    },
  });
};

/**
 * Middleware to catch async errors and pass them to the error handler
 */
export const catchAsync =
  (fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) =>
  (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch((err) => {
      next(err);
    });
  };

/**
 * Middleware to check if a resource exists
 */
export const checkResourceExists =
  (resourceName: string) =>
  (req: Request, res: Response, next: NextFunction) => {
    if (!req[resourceName]) {
      throw new NotFoundError(`${resourceName} not found`);
    }
    next();
  };

import { Request, Response, NextFunction } from 'express';
import axios from 'axios';
import { env } from '../config/env';
import { UnauthorizedError } from './error.middleware';

declare global {
  namespace Express {
    interface Request {
      user?: {
        userId: number;
        username: string;
        role: string;
      };
    }
  }
}

export const authenticate = async (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new UnauthorizedError('No token provided');
  }

  const token = authHeader.split(' ')[1];

  try {
    // Verify token with User Service
    const response = await axios.post(`${env.USER_SERVICE_URL}/api/auth/verify`, { token });
    req.user = response.data;
    next();
  } catch (err) {
    throw new UnauthorizedError('Invalid or expired token');
  }
};

export const authorize = (roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      throw new UnauthorizedError('Insufficient permissions');
    }
    next();
  };
};

// src/middlewares/auth.middleware.ts

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { env } from '../config/env';
import { Unauthorized, Forbidden } from '../utils/errors';

/**
 * Expected JWT payload: { userId: string, role: 'patron'|'staff'|'librarian' }
 */
type JwtPayload = {
  userId: string;
  role: 'patron' | 'staff' | 'librarian';
  iat?: number;
  exp?: number;
};

declare global {
  namespace Express {
    interface Request {
      auth?: JwtPayload;
    }
  }
}

export const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return next(Unauthorized('Authorization header missing'));
  }
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, env.JWT_SECRET) as JwtPayload;
    req.auth = decoded;
    next();
  } catch (err) {
    return next(Unauthorized('Invalid or expired token'));
  }
};

export const authorize = (...allowedRoles: JwtPayload['role'][]) => {
  return (req: Request, _res: Response, next: NextFunction) => {
    const auth = req.auth;
    if (!auth) return next(Unauthorized('Not authenticated'));
    if (!allowedRoles.includes(auth.role)) return next(Forbidden('Insufficient permissions'));
    next();
  };
};

/**
 * Owner-or-role guard: allows access if requester is the resource owner (userId param matches token userId)
 * or has one of the allowed roles.
 */
export const ownerOrRole = (...allowedRoles: JwtPayload['role'][]) => {
  return (req: Request, _res: Response, next: NextFunction) => {
    const auth = req.auth;
    if (!auth) return next(Unauthorized('Not authenticated'));
    const targetUserId = req.params.id || req.params.userId;
    if (auth.userId === targetUserId) return next();
    if (allowedRoles.includes(auth.role)) return next();
    return next(Forbidden('Insufficient permissions'));
  };
};

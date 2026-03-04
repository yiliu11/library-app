// src/controllers/user.controller.ts

import { Request, Response, NextFunction } from 'express';
import * as userService from '../services/user.service';
import { sendSuccess } from '../utils/response';

export const createUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.createUser(req.body);
    return sendSuccess(res, user, 'User created', 201);
  } catch (err) {
    next(err);
  }
};

export const getUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.getUserById(req.params.id);
    return sendSuccess(res, user, 'User retrieved');
  } catch (err) {
    next(err);
  }
};

export const listUsers = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const page = req.query.page ? Number(req.query.page) : undefined;
    const size = req.query.size ? Number(req.query.size) : undefined;
    const role = req.query.role as string | undefined;
    const search = req.query.search as string | undefined;
    const result = await userService.listUsers({ page, size, role, search });
    return sendSuccess(res, result, 'Users listed');
  } catch (err) {
    next(err);
  }
};

export const updateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const updated = await userService.updateUser(req.params.id, req.body);
    return sendSuccess(res, updated, 'User updated');
  } catch (err) {
    next(err);
  }
};

export const deleteUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const result = await userService.deleteUser(req.params.id);
    return sendSuccess(res, result, 'User deleted');
  } catch (err) {
    next(err);
  }
};

/**
 * Optional endpoint: get current user profile
 */
export const me = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const auth = req.auth!;
    const user = await userService.getUserById(auth.userId);
    return sendSuccess(res, user, 'My profile');
  } catch (err) {
    next(err);
  }
};

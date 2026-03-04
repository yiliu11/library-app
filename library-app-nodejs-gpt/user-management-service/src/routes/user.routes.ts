// src/routes/user.routes.ts

import { Router } from 'express';
import * as userController from '../controllers/user.controller';
import validate from '../middlewares/validate';
import { createUserSchema, updateUserSchema, getUserParams, listUsersQuery } from '../validators/user.validator';
import { authenticate, authorize, ownerOrRole } from '../middlewares/auth.middleware';

const router = Router();

// Librarian registers new users
router.post('/', authenticate, authorize('librarian'), validate(createUserSchema), userController.createUser);

// Librarian can list users
router.get('/', authenticate, authorize('librarian'), validate(listUsersQuery), userController.listUsers);

// Get user by id - owner or librarian
router.get('/:id', authenticate, ownerOrRole('librarian'), validate(getUserParams), userController.getUser);

// Update user - owner or librarian
router.put('/:id', authenticate, ownerOrRole('librarian'), validate(updateUserSchema), userController.updateUser);

// Delete user - librarian only
router.delete('/:id', authenticate, authorize('librarian'), validate(getUserParams), userController.deleteUser);

// Get current profile
router.get('/me/profile', authenticate, userController.me);

export default router;

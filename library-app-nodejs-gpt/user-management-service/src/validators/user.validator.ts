// src/validators/user.validator.ts

import { z } from 'zod';

/**
 * For registration by librarian: provide username, email, password, role (patron|staff|librarian) optionally fullName.
 * Password policy: min 6 chars, at least one digit and one letter.
 */

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    username: z.string().min(3),
    password: z
      .string()
      .min(6, 'Password must be at least 6 characters')
      .regex(/[A-Za-z]/, 'Password must include letters')
      .regex(/[0-9]/, 'Password must include numbers'),
    role: z.enum(['patron', 'staff', 'librarian']).optional().default('patron'),
    fullName: z.string().optional()
  })
});

export const updateUserSchema = z.object({
  body: z.object({
    email: z.string().email().optional(),
    username: z.string().min(3).optional(),
    password: z
      .string()
      .min(6)
      .regex(/[A-Za-z]/)
      .regex(/[0-9]/)
      .optional(),
    fullName: z.string().optional(),
    isActive: z.boolean().optional(),
    role: z.enum(['patron', 'staff', 'librarian']).optional()
  })
});

export const getUserParams = z.object({
  params: z.object({
    id: z.string().uuid()
  })
});

export const listUsersQuery = z.object({
  query: z.object({
    page: z.string().optional(),
    size: z.string().optional(),
    role: z.string().optional(),
    search: z.string().optional()
  })
});

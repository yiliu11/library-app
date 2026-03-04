import { z } from 'zod';

export const checkoutSchema = z.object({
  body: z.object({
    userId: z.string().uuid({ message: 'Invalid user ID' }),
    bookId: z.string().uuid({ message: 'Invalid book ID' }),
  }),
});

export const renewSchema = z.object({
  body: z.object({
    userId: z.string().uuid({ message: 'Invalid user ID' }),
    bookId: z.string().uuid({ message: 'Invalid book ID' }),
  }),
});

export const returnSchema = z.object({
  body: z.object({
    userId: z.string().uuid({ message: 'Invalid user ID' }),
    bookId: z.string().uuid({ message: 'Invalid book ID' }),
  }),
});

export const userLoanParamSchema = z.object({
  params: z.object({
    userId: z.string().uuid({ message: 'Invalid user ID' }),
  }),
});

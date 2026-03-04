import { Router } from 'express';
import {
  getAllBooks,
  getBookById,
  createBook,
  updateBook,
  deleteBook,
  searchBooks,
} from '../controllers/book.controller';
import { validateBookCreation, validateBookUpdate } from '../validators/book.validator';
import { authenticate, authorizeLibrarian } from '../middlewares/auth.middleware';

const router = Router();

// Public
router.get('/', getAllBooks);
router.get('/search', searchBooks);
router.get('/:id', getBookById);

// Protected
router.post('/', authenticate, authorizeLibrarian, validateBookCreation, createBook);
router.put('/:id', authenticate, authorizeLibrarian, validateBookUpdate, updateBook);
router.delete('/:id', authenticate, authorizeLibrarian, deleteBook);

export default router;
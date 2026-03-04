import { Router } from 'express';
import { BookController } from '../controllers/book.controller';
import { BookRepository } from '../repositories/book.repository';
import { BookService } from '../services/book.service';
import { authenticate, authorize } from '../middlewares/auth.middleware';
import { validateDTO } from '../middlewares/validation.middleware';
import { BookRequestDTO, BookUpdateDTO } from '../dtos/book.dto';
import { BookSearchDTO } from '../dtos/search.dto';

const router = Router();
const bookRepository = new BookRepository();
const bookService = new BookService(bookRepository);
const bookController = new BookController(bookService);

// Public routes
router.get('/:id', bookController.getBookById);
router.post('/search', validateDTO(BookSearchDTO), bookController.searchBooks);

// Protected routes (require authentication)
router.use(authenticate);

// Librarian-only routes
router.post(
  '/',
  authorize(['LIBRARIAN']),
  validateDTO(BookRequestDTO),
  bookController.createBook
);

router.put(
  '/:id',
  authorize(['LIBRARIAN']),
  validateDTO(BookUpdateDTO),
  bookController.updateBook
);

router.delete(
  '/:id',
  authorize(['LIBRARIAN']),
  bookController.deleteBook
);

export default router;

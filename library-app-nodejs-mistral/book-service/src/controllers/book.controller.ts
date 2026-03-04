import { Request, Response } from 'express';
import { BookService } from '../services/book.service';
import { BookRequestDTO, BookResponseDTO, BookUpdateDTO } from '../dtos/book.dto';
import { BookSearchDTO } from '../dtos/search.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class BookController {
  constructor(private bookService: BookService) {}

  createBook = async (req: Request, res: Response) => {
    const bookDTO: BookRequestDTO = req.body;
    const book = await this.bookService.createBook(bookDTO, req.user.role);
    res.status(201).json(book);
  };

  getBookById = async (req: Request, res: Response) => {
    const bookId = parseInt(req.params.id);
    const book = await this.bookService.getBookById(bookId);
    res.json(book);
  };

  searchBooks = async (req: Request, res: Response) => {
    const searchDTO: BookSearchDTO = req.body;
    const books = await this.bookService.searchBooks(searchDTO);
    res.json(books);
  };

  updateBook = async (req: Request, res: Response) => {
    const bookId = parseInt(req.params.id);
    const bookDTO: BookUpdateDTO = req.body;
    const updatedBook = await this.bookService.updateBook(bookId, bookDTO, req.user.role);
    res.json(updatedBook);
  };

  deleteBook = async (req: Request, res: Response) => {
    const bookId = parseInt(req.params.id);
    await this.bookService.deleteBook(bookId, req.user.role);
    res.status(204).send();
  };
}

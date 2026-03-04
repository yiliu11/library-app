import { BookRepository } from '../repositories/book.repository';
import { BookRequestDTO, BookResponseDTO, BookUpdateDTO, AvailabilityStatus } from '../dtos/book.dto';
import { BookSearchDTO } from '../dtos/search.dto';
import { BadRequestError, ForbiddenError, NotFoundError } from '../middlewares/error.middleware';
import { logger } from '../utils/logger';
import axios from 'axios';
import { env } from '../config/env';

export class BookService {
  constructor(
    private bookRepository: BookRepository
  ) {}

  async createBook(bookDTO: BookRequestDTO, userRole: string): Promise<BookResponseDTO> {
    if (userRole !== 'LIBRARIAN') {
      throw new ForbiddenError('Only librarians can add books');
    }

    // Check if ISBN already exists
    const existingBook = await this.bookRepository.findByIsbn(bookDTO.isbn);
    if (existingBook) {
      throw new BadRequestError('A book with this ISBN already exists');
    }

    const book = {
      title: bookDTO.title,
      author: bookDTO.author,
      isbn: bookDTO.isbn,
      publication_date: bookDTO.publicationDate ? new Date(bookDTO.publicationDate) : null,
      availability_status: AvailabilityStatus.AVAILABLE as const,
    };

    const createdBook = await this.bookRepository.createBook(book);
    return new BookResponseDTO(createdBook);
  }

  async getBookById(id: number): Promise<BookResponseDTO> {
    const book = await this.bookRepository.findById(id);
    if (!book) {
      throw new NotFoundError('Book not found');
    }
    return new BookResponseDTO(book);
  }

  async searchBooks(searchDTO: BookSearchDTO): Promise<BookResponseDTO[]> {
    const books = await this.bookRepository.searchBooks(searchDTO);
    return books.map(book => new BookResponseDTO(book));
  }

  async updateBook(id: number, bookDTO: BookUpdateDTO, userRole: string): Promise<BookResponseDTO> {
    if (userRole !== 'LIBRARIAN') {
      throw new ForbiddenError('Only librarians can update books');
    }

    const existingBook = await this.bookRepository.findById(id);
    if (!existingBook) {
      throw new NotFoundError('Book not found');
    }

    // If ISBN is being updated, check if the new ISBN already exists
    if (bookDTO.isbn && bookDTO.isbn !== existingBook.isbn) {
      const bookWithIsbn = await this.bookRepository.findByIsbn(bookDTO.isbn);
      if (bookWithIsbn) {
        throw new BadRequestError('A book with this ISBN already exists');
      }
    }

    const updatedBook = await this.bookRepository.updateBook(id, bookDTO);
    if (!updatedBook) {
      throw new NotFoundError('Book not found');
    }
    return new BookResponseDTO(updatedBook);
  }

  async deleteBook(id: number, userRole: string): Promise<void> {
    if (userRole !== 'LIBRARIAN') {
      throw new ForbiddenError('Only librarians can delete books');
    }

    const book = await this.bookRepository.findById(id);
    if (!book) {
      throw new NotFoundError('Book not found');
    }

    // Check if the book is currently checked out
    try {
      const response = await axios.get(`${env.USER_SERVICE_URL}/api/checkouts/book/${id}/status`);
      if (response.data.isCheckedOut) {
        throw new BadRequestError('Cannot delete a book that is currently checked out');
      }
    } catch (err) {
      logger.error(`Failed to check book status: ${err}`);
      throw new BadRequestError('Failed to verify book status');
    }

    await this.bookRepository.deleteBook(id);
  }

  async updateAvailabilityStatus(id: number, status: AvailabilityStatus): Promise<BookResponseDTO> {
    const updatedBook = await this.bookRepository.updateAvailabilityStatus(id, status);
    if (!updatedBook) {
      throw new NotFoundError('Book not found');
    }
    return new BookResponseDTO(updatedBook);
  }
}

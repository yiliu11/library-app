import { query } from '../config/db';
import { Book, AvailabilityStatus } from '../models/book.model';
import { BookSearchDTO, SearchCriteria } from '../dtos/search.dto';
import { logger } from '../utils/logger';
import { inputSanitizer } from '../utils/input-sanitizer';

export class BookRepository {
  async createBook(book: Book): Promise<Book> {
    const sanitizedBook = inputSanitizer.sanitizeObject(book);
    const result = await query(
      `INSERT INTO books (
        title, author, isbn, publication_date, availability_status
      ) VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [
        sanitizedBook.title,
        sanitizedBook.author,
        sanitizedBook.isbn,
        sanitizedBook.publication_date,
        sanitizedBook.availability_status,
      ]
    );
    return result.rows[0];
  }

  async findById(id: number): Promise<Book | null> {
    const result = await query('SELECT * FROM books WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async findByIsbn(isbn: string): Promise<Book | null> {
    const result = await query('SELECT * FROM books WHERE isbn = $1', [isbn]);
    return result.rows[0] || null;
  }

  async updateBook(id: number, book: Partial<Book>): Promise<Book | null> {
    const sanitizedBook = inputSanitizer.sanitizeObject(book);
    const fields = Object.keys(sanitizedBook)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');

    const values = Object.values(sanitizedBook);

    const result = await query(
      `UPDATE books SET ${fields}, updated_at = CURRENT_TIMESTAMP WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    return result.rows[0] || null;
  }

  async deleteBook(id: number): Promise<void> {
    await query('DELETE FROM books WHERE id = $1', [id]);
  }

  async searchBooks(searchDTO: BookSearchDTO): Promise<Book[]> {
    const { searchTerm, searchBy = SearchCriteria.TITLE } = searchDTO;
    const sanitizedTerm = inputSanitizer.sanitize(searchTerm);

    let queryText = '';
    let params: any[] = [];

    switch (searchBy) {
      case SearchCriteria.TITLE:
        queryText = 'SELECT * FROM books WHERE LOWER(title) LIKE LOWER($1)';
        params = [`%${sanitizedTerm}%`];
        break;
      case SearchCriteria.AUTHOR:
        queryText = 'SELECT * FROM books WHERE LOWER(author) LIKE LOWER($1)';
        params = [`%${sanitizedTerm}%`];
        break;
      case SearchCriteria.ISBN:
        queryText = 'SELECT * FROM books WHERE isbn = $1';
        params = [sanitizedTerm];
        break;
      default:
        queryText = 'SELECT * FROM books WHERE LOWER(title) LIKE LOWER($1)';
        params = [`%${sanitizedTerm}%`];
    }

    const result = await query(queryText, params);
    return result.rows;
  }

  async updateAvailabilityStatus(id: number, status: AvailabilityStatus): Promise<Book | null> {
    const result = await query(
      'UPDATE books SET availability_status = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2 RETURNING *',
      [status, id]
    );
    return result.rows[0] || null;
  }
}

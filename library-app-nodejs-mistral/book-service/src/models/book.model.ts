import { AvailabilityStatus } from '../dtos/book.dto';

export interface Book {
  id?: number;
  title: string;
  author: string;
  isbn: string;
  publication_date?: Date;
  availability_status: AvailabilityStatus;
  created_at?: Date;
  updated_at?: Date;
}

export const createBooksTable = `
  CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publication_date DATE,
    availability_status VARCHAR(20) NOT NULL CHECK (
      availability_status IN ('AVAILABLE', 'CHECKED_OUT', 'RESERVED', 'LOST')
    ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
`;

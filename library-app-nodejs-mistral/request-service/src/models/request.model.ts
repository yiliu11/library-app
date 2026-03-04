import { RequestStatus } from '../dtos/request.dto';

export interface BookRequest {
  id?: number;
  book_title: string;
  book_author: string;
  book_isbn?: string;
  requester_id: number;
  request_date?: Date;
  status: RequestStatus;
  decision_date?: Date;
  decided_by?: number;
  notes?: string;
}

export const createRequestsTable = `
  CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    book_author VARCHAR(100) NOT NULL,
    book_isbn VARCHAR(20),
    requester_id INTEGER NOT NULL,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (
      status IN ('PENDING', 'APPROVED', 'REJECTED', 'ARCHIVED')
    ),
    decision_date TIMESTAMP,
    decided_by INTEGER,
    notes TEXT,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (decided_by) REFERENCES users(id) ON DELETE SET NULL
  );
`;

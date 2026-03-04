import { query } from '../config/db';
import { BookRequest, RequestStatus } from '../models/request.model';
import { logger } from '../utils/logger';

export class RequestRepository {
  async createRequest(request: BookRequest): Promise<BookRequest> {
    const result = await query(
      `INSERT INTO requests (
        book_title, book_author, book_isbn, requester_id, status, notes
      ) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [
        request.book_title,
        request.book_author,
        request.book_isbn,
        request.requester_id,
        request.status,
        request.notes,
      ]
    );
    return result.rows[0];
  }

  async findById(id: number): Promise<BookRequest | null> {
    const result = await query('SELECT * FROM requests WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async findPendingRequests(): Promise<BookRequest[]> {
    const result = await query(
      'SELECT * FROM requests WHERE status = \'PENDING\' ORDER BY request_date DESC'
    );
    return result.rows;
  }

  async findByRequester(requesterId: number): Promise<BookRequest[]> {
    const result = await query(
      'SELECT * FROM requests WHERE requester_id = $1 ORDER BY request_date DESC',
      [requesterId]
    );
    return result.rows;
  }

  async updateRequest(id: number, request: Partial<BookRequest>): Promise<BookRequest | null> {
    const fields = Object.keys(request)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');

    const values = Object.values(request);

    const result = await query(
      `UPDATE requests SET ${fields} WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    return result.rows[0] || null;
  }

  async updateStatus(id: number, status: RequestStatus, decidedBy?: number): Promise<BookRequest | null> {
    const result = await query(
      `UPDATE requests
       SET status = $1,
           decision_date = CURRENT_TIMESTAMP,
           decided_by = $2
       WHERE id = $3 RETURNING *`,
      [status, decidedBy, id]
    );
    return result.rows[0] || null;
  }
}

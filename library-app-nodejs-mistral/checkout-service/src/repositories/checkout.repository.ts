import { query } from '../config/db';
import { Checkout, CheckoutStatus } from '../models/checkout.model';
import { logger } from '../utils/logger';
import { DateUtils } from '../utils/date-utils';

export class CheckoutRepository {
  async createCheckout(checkout: Checkout): Promise<Checkout> {
    const result = await query(
      `INSERT INTO checkouts (
        user_id, book_id, due_date, status
      ) VALUES ($1, $2, $3, $4) RETURNING *`,
      [
        checkout.user_id,
        checkout.book_id,
        checkout.due_date,
        checkout.status,
      ]
    );
    return result.rows[0];
  }

  async findById(id: number): Promise<Checkout | null> {
    const result = await query('SELECT * FROM checkouts WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async findByUserAndBook(userId: number, bookId: number): Promise<Checkout | null> {
    const result = await query(
      'SELECT * FROM checkouts WHERE user_id = $1 AND book_id = $2 AND status IN (\'ACTIVE\', \'OVERDUE\')',
      [userId, bookId]
    );
    return result.rows[0] || null;
  }

  async findActiveByUser(userId: number): Promise<Checkout[]> {
    const result = await query(
      'SELECT * FROM checkouts WHERE user_id = $1 AND status IN (\'ACTIVE\', \'OVERDUE\')',
      [userId]
    );
    return result.rows;
  }

  async findActiveByBook(bookId: number): Promise<Checkout | null> {
    const result = await query(
      'SELECT * FROM checkouts WHERE book_id = $1 AND status IN (\'ACTIVE\', \'OVERDUE\')',
      [bookId]
    );
    return result.rows[0] || null;
  }

  async updateCheckout(id: number, checkout: Partial<Checkout>): Promise<Checkout | null> {
    const fields = Object.keys(checkout)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');

    const values = Object.values(checkout);

    const result = await query(
      `UPDATE checkouts SET ${fields} WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    return result.rows[0] || null;
  }

  async updateStatus(id: number, status: CheckoutStatus): Promise<Checkout | null> {
    const result = await query(
      'UPDATE checkouts SET status = $1 WHERE id = $2 RETURNING *',
      [status, id]
    );
    return result.rows[0] || null;
  }

  async getUserRecords(userId: number): Promise<any> {
    const result = await query(
      `SELECT * FROM user_records WHERE user_id = $1`,
      [userId]
    );
    return result.rows[0] || null;
  }

  async updateFineAmount(id: number, amount: number): Promise<Checkout | null> {
    const result = await query(
      'UPDATE checkouts SET fine_amount = $1 WHERE id = $2 RETURNING *',
      [amount, id]
    );
    return result.rows[0] || null;
  }

  async checkUserCheckoutLimit(userId: number): Promise<boolean> {
    const result = await query(
      'SELECT COUNT(*) FROM checkouts WHERE user_id = $1 AND status IN (\'ACTIVE\', \'OVERDUE\')',
      [userId]
    );
    return parseInt(result.rows[0].count) < env.MAX_CHECKOUT_LIMIT;
  }

  async checkUserHasOverdueBooks(userId: number): Promise<boolean> {
    const result = await query(
      'SELECT COUNT(*) FROM checkouts WHERE user_id = $1 AND status = \'OVERDUE\'',
      [userId]
    );
    return parseInt(result.rows[0].count) > 0;
  }
}

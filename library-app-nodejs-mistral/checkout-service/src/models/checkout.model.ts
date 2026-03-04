import { CheckoutStatus } from '../dtos/checkout.dto';

export interface Checkout {
  id?: number;
  user_id: number;
  book_id: number;
  checkout_date?: Date;
  due_date: Date;
  return_date?: Date;
  status: CheckoutStatus;
  fine_amount?: number;
}

export const createCheckoutsTable = `
  CREATE TABLE IF NOT EXISTS checkouts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    checkout_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (
      status IN ('ACTIVE', 'OVERDUE', 'RETURNED', 'RENEWED')
    ),
    fine_amount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
  );
`;

export const createUserRecordsView = `
  CREATE OR REPLACE VIEW user_records AS
  SELECT
    c.user_id,
    json_agg(
      json_build_object(
        'book_id', c.book_id,
        'book_title', b.title,
        'due_date', c.due_date,
        'status', c.status,
        'fine_amount', c.fine_amount
      )
    ) AS checked_out_items,
    COALESCE(SUM(c.fine_amount), 0) AS total_fines
  FROM checkouts c
  JOIN books b ON c.book_id = b.id
  WHERE c.status IN ('ACTIVE', 'OVERDUE')
  GROUP BY c.user_id;
`;

CREATE TABLE IF NOT EXISTS loans (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  book_id UUID NOT NULL,
  checkout_date DATE NOT NULL,
  due_date DATE NOT NULL,
  return_date DATE,
  renewal_count INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(30) NOT NULL,
  created_at TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_loans_user ON loans(user_id);
CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id);

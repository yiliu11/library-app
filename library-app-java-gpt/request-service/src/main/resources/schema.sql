CREATE TABLE IF NOT EXISTS book_requests (
  id UUID PRIMARY KEY,
  requested_by UUID NOT NULL,
  title VARCHAR(500) NOT NULL,
  author VARCHAR(300),
  reason TEXT,
  status VARCHAR(50) NOT NULL,
  comments TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_requests_requested_by ON book_requests(requested_by);
CREATE INDEX IF NOT EXISTS idx_requests_status ON book_requests(status);

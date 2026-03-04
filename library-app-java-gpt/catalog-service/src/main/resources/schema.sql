CREATE TABLE IF NOT EXISTS books (
  id UUID PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  author VARCHAR(300) NOT NULL,
  isbn VARCHAR(20),
  published_date DATE,
  genre VARCHAR(100),
  copies_available INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);

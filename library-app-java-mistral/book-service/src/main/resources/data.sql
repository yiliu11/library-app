-- Disable foreign key checks temporarily
SET session_replication_role = 'replica';

-- Insert sample books
INSERT INTO books (id, title, author, isbn, publication_date, availability_status, created_at, updated_at)
VALUES
    (1, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', '1925-04-10', 'AVAILABLE', NOW(), NOW()),
    (2, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', '1960-07-11', 'AVAILABLE', NOW(), NOW()),
    (3, '1984', 'George Orwell', '9780451524935', '1949-06-08', 'CHECKED_OUT', NOW(), NOW()),
    (4, 'Pride and Prejudice', 'Jane Austen', '9780141439518', '1813-01-28', 'AVAILABLE', NOW(), NOW()),
    (5, 'The Hobbit', 'J.R.R. Tolkien', '9780547928227', '1937-09-21', 'RESERVED', NOW(), NOW());

-- Re-enable foreign key checks
SET session_replication_role = 'default';

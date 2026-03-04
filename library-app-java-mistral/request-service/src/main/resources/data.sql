-- Disable foreign key checks temporarily
SET session_replication_role = 'replica';

-- Insert sample book requests
INSERT INTO book_requests (id, book_title, book_author, book_isbn, requester_id, request_date, status, decision_date, decided_by, notes, updated_at)
VALUES
    (1, 'Clean Code', 'Robert C. Martin', '9780132350884', 2, NOW() - INTERVAL '5 days', 'PENDING', NULL, NULL, NULL, NOW()),
    (2, 'Designing Data-Intensive Applications', 'Martin Kleppmann', '9781449373320', 2, NOW() - INTERVAL '3 days', 'APPROVED', NOW() - INTERVAL '1 day', 1, 'Approved for acquisition', NOW()),
    (3, 'The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', 2, NOW() - INTERVAL '7 days', 'REJECTED', NOW() - INTERVAL '2 days', 1, 'Already in collection', NOW()),
    (4, 'Refactoring', 'Martin Fowler', '9780134757599', 3, NOW() - INTERVAL '1 day', 'PENDING', NULL, NULL, NULL, NOW());

-- Re-enable foreign key checks
SET session_replication_role = 'default';

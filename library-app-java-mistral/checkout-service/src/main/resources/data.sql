-- Disable foreign key checks temporarily
SET session_replication_role = 'replica';

-- Insert sample checkout records
INSERT INTO checkout_records (id, user_id, book_id, checkout_date, due_date, return_date, status, fine_amount, created_at, updated_at)
VALUES
    (1, 3, 3, NOW() - INTERVAL '7 days', NOW() + INTERVAL '7 days', NULL, 'ACTIVE', 0.00, NOW(), NOW()),
    (2, 3, 1, NOW() - INTERVAL '14 days', NOW() - INTERVAL '1 day', NULL, 'OVERDUE', 2.50, NOW(), NOW()),
    (3, 4, 2, NOW() - INTERVAL '21 days', NOW() - INTERVAL '7 days', NOW() - INTERVAL '5 days', 'RETURNED', 3.50, NOW(), NOW()),
    (4, 3, 5, NOW() - INTERVAL '3 days', NOW() + INTERVAL '11 days', NULL, 'RENEWED', 0.00, NOW(), NOW());

-- Re-enable foreign key checks
SET session_replication_role = 'default';

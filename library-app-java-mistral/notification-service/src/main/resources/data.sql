-- Disable foreign key checks temporarily
SET session_replication_role = 'replica';

-- Insert sample notifications
INSERT INTO notifications (id, recipient_id, recipient_email, recipient_phone, subject, message, notification_type, status, created_at, sent_at, metadata, updated_at)
VALUES
    (1, 3, 'patron1@library.com', '5551234567', 'Overdue Book Reminder', 'The book "The Great Gatsby" is overdue.', 'OVERDUE_BOOK', 'SENT', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days', '{"bookTitle": "The Great Gatsby", "dueDate": "2023-10-15", "fineAmount": "2.50"}', NOW()),
    (2, 2, 'staff1@library.com', '5559876543', 'Request Approved', 'Your request for "Clean Code" has been approved.', 'REQUEST_APPROVED', 'SENT', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', '{"bookTitle": "Clean Code", "reason": "Approved for acquisition"}', NOW()),
    (3, 3, 'patron1@library.com', '5551234567', 'Due Date Reminder', 'Reminder: "1984" is due on 2023-10-20.', 'DUE_DATE_REMINDER', 'PENDING', NOW() - INTERVAL '1 hour', NULL, '{"bookTitle": "1984", "dueDate": "2023-10-20"}', NOW()),
    (4, 4, 'patron2@library.com', '5555555555', 'Checkout Confirmation', 'You checked out "Pride and Prejudice". Due: 2023-10-25.', 'CHECKOUT_CONFIRMATION', 'FAILED', NOW() - INTERVAL '3 days', NULL, '{"bookTitle": "Pride and Prejudice", "dueDate": "2023-10-25"}', NOW());

-- Re-enable foreign key checks
SET session_replication_role = 'default';

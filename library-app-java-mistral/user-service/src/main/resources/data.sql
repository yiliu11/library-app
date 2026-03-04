-- Disable foreign key checks temporarily to avoid constraints during insertion
SET session_replication_role = 'replica';

-- Insert sample users
INSERT INTO users (username, email, password, role, is_active, failed_login_attempts, last_login, created_at, updated_at)
VALUES
    -- Librarian (admin)
    (1, 'admin', 'admin@library.com', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrUQYVZ9q1f0T2orYd5HlVYZQ1Q5X7G', 'LIBRARIAN', TRUE, 0, NOW(), NOW(), NOW()),
    -- Staff
    (2, 'staff1', 'staff1@library.com', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrUQYVZ9q1f0T2orYd5HlVYZQ1Q5X7G', 'STAFF', TRUE, 0, NOW(), NOW(), NOW()),
    -- Patron
    (3, 'patron1', 'patron1@library.com', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrUQYVZ9q1f0T2orYd5HlVYZQ1Q5X7G', 'PATRON', TRUE, 0, NOW(), NOW(), NOW()),
    -- Another Patron
    (4, 'patron2', 'patron2@library.com', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrUQYVZ9q1f0T2orYd5HlVYZQ1Q5X7G', 'PATRON', TRUE, 0, NOW(), NOW(), NOW()),
    -- Inactive user (locked)
    (5, 'inactive_user', 'inactive@library.com', '$2a$10$N9qo8uLOickgx2ZMRZoMy.MrUQYVZ9q1f0T2orYd5HlVYZQ1Q5X7G', 'PATRON', FALSE, 5, NOW(), NOW(), NOW());

-- Re-enable foreign key checks
SET session_replication_role = 'default';

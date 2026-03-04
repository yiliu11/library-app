import { UserRole } from '../dtos/user.dto';

export interface User {
  id?: number;
  username: string;
  email: string;
  passwordHash: string;
  role: UserRole;
  isActive: boolean;
  failedLoginAttempts: number;
  lastLogin?: Date;
  createdAt?: Date;
  updatedAt?: Date;
}

export const createUsersTable = `
  CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('PATRON', 'STAFF', 'LIBRARIAN')),
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INT DEFAULT 0,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
`;

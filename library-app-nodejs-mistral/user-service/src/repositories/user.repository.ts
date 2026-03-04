import { query } from '../config/db';
import { User, UserRole } from '../models/user.model';
import { logger } from '../utils/logger';

export class UserRepository {
  async createUser(user: User): Promise<User> {
    const result = await query(
      'INSERT INTO users (username, email, password_hash, role) VALUES ($1, $2, $3, $4) RETURNING *',
      [user.username, user.email, user.passwordHash, user.role]
    );
    return result.rows[0];
  }

  async findByUsername(username: string): Promise<User | null> {
    const result = await query('SELECT * FROM users WHERE username = $1', [username]);
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await query('SELECT * FROM users WHERE email = $1', [email]);
    return result.rows[0] || null;
  }

  async findById(id: number): Promise<User | null> {
    const result = await query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async updateUser(id: number, user: Partial<User>): Promise<User | null> {
    const fields = Object.keys(user)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');
    const values = Object.values(user);

    const result = await query(
      `UPDATE users SET ${fields}, updated_at = CURRENT_TIMESTAMP WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    return result.rows[0] || null;
  }

  async incrementFailedLoginAttempts(id: number): Promise<void> {
    await query(
      'UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE id = $1',
      [id]
    );
  }

  async resetFailedLoginAttempts(id: number): Promise<void> {
    await query(
      'UPDATE users SET failed_login_attempts = 0 WHERE id = $1',
      [id]
    );
  }

  async lockUser(id: number): Promise<void> {
    await query(
      'UPDATE users SET is_active = FALSE WHERE id = $1',
      [id]
    );
  }

  async updateLastLogin(id: number): Promise<void> {
    await query(
      'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1',
      [id]
    );
  }

  async existsByUsername(username: string): Promise<boolean> {
    const result = await query('SELECT 1 FROM users WHERE username = $1', [username]);
    return result.rowCount > 0;
  }

  async existsByEmail(email: string): Promise<boolean> {
    const result = await query('SELECT 1 FROM users WHERE email = $1', [email]);
    return result.rowCount > 0;
  }
}

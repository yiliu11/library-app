import { query } from '../config/db';
import { Notification, NotificationStatus } from '../models/notification.model';
import { logger } from '../utils/logger';

export class NotificationRepository {
  async createNotification(notification: Notification): Promise<Notification> {
    const result = await query(
      `INSERT INTO notifications (
        recipient_id, recipient_email, recipient_phone, subject, message,
        notification_type, status, metadata
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [
        notification.recipient_id,
        notification.recipient_email,
        notification.recipient_phone,
        notification.subject,
        notification.message,
        notification.notification_type,
        notification.status,
        notification.metadata,
      ]
    );
    return result.rows[0];
  }

  async findById(id: number): Promise<Notification | null> {
    const result = await query('SELECT * FROM notifications WHERE id = $1', [id]);
    return result.rows[0] || null;
  }

  async findPendingNotifications(): Promise<Notification[]> {
    const result = await query(
      'SELECT * FROM notifications WHERE status = \'PENDING\' ORDER BY created_at ASC'
    );
    return result.rows;
  }

  async updateNotificationStatus(id: number, status: NotificationStatus): Promise<Notification | null> {
    const result = await query(
      'UPDATE notifications SET status = $1, sent_at = CURRENT_TIMESTAMP WHERE id = $2 RETURNING *',
      [status, id]
    );
    return result.rows[0] || null;
  }

  async updateNotificationFailure(id: number, error: string): Promise<Notification | null> {
    const result = await query(
      'UPDATE notifications SET status = \'FAILED\', sent_at = CURRENT_TIMESTAMP, metadata = jsonb_set(metadata, \'{error}\', to_jsonb($1::text)) WHERE id = $2 RETURNING *',
      [error, id]
    );
    return result.rows[0] || null;
  }
}

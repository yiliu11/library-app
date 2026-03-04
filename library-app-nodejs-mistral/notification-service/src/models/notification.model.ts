import { NotificationType, NotificationStatus } from '../dtos/notification.dto';

export interface Notification {
  id?: number;
  recipient_id: number;
  recipient_email?: string;
  recipient_phone?: string;
  subject: string;
  message: string;
  notification_type: NotificationType;
  status: NotificationStatus;
  created_at?: Date;
  sent_at?: Date;
  metadata?: Record<string, any>;
}

export const createNotificationsTable = `
  CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER NOT NULL,
    recipient_email VARCHAR(100),
    recipient_phone VARCHAR(20),
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (
      status IN ('PENDING', 'SENT', 'FAILED')
    ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    metadata JSONB,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
  );
`;

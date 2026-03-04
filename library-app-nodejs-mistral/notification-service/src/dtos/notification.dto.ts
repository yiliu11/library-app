import { IsString, IsNotEmpty, IsEnum, IsOptional, IsInt, IsDateString, IsEmail, IsPhoneNumber } from 'class-validator';

export enum NotificationType {
  OVERDUE_BOOK = 'OVERDUE_BOOK',
  REQUEST_APPROVED = 'REQUEST_APPROVED',
  REQUEST_REJECTED = 'REQUEST_REJECTED',
  DUE_DATE_REMINDER = 'DUE_DATE_REMINDER',
  PASSWORD_RESET = 'PASSWORD_RESET',
  CHECKOUT_CONFIRMATION = 'CHECKOUT_CONFIRMATION',
  RENEWAL_CONFIRMATION = 'RENEWAL_CONFIRMATION',
  RETURN_CONFIRMATION = 'RETURN_CONFIRMATION',
  NEW_BOOK_REQUEST = 'NEW_BOOK_REQUEST',
}

export enum NotificationStatus {
  PENDING = 'PENDING',
  SENT = 'SENT',
  FAILED = 'FAILED',
}

export class NotificationRequestDTO {
  @IsInt()
  @IsNotEmpty()
  recipientId: number;

  @IsEmail()
  @IsOptional()
  recipientEmail?: string;

  @IsPhoneNumber()
  @IsOptional()
  recipientPhone?: string;

  @IsString()
  @IsNotEmpty()
  subject: string;

  @IsString()
  @IsNotEmpty()
  message: string;

  @IsEnum(NotificationType)
  @IsNotEmpty()
  notificationType: NotificationType;

  @IsOptional()
  metadata?: Record<string, any>;
}

export class NotificationResponseDTO {
  notificationId: number;
  status: NotificationStatus;
  timestamp: Date;

  constructor(notification: any) {
    this.notificationId = notification.id;
    this.status = notification.status;
    this.timestamp = notification.created_at || new Date();
  }
}

export class NotificationDTO {
  id: number;
  recipientId: number;
  recipientEmail: string;
  recipientPhone: string;
  subject: string;
  message: string;
  notificationType: NotificationType;
  status: NotificationStatus;
  createdAt: Date;
  sentAt: Date;
  metadata: Record<string, any>;

  constructor(notification: any) {
    this.id = notification.id;
    this.recipientId = notification.recipient_id;
    this.recipientEmail = notification.recipient_email;
    this.recipientPhone = notification.recipient_phone;
    this.subject = notification.subject;
    this.message = notification.message;
    this.notificationType = notification.notification_type;
    this.status = notification.status;
    this.createdAt = notification.created_at;
    this.sentAt = notification.sent_at;
    this.metadata = notification.metadata || {};
  }
}

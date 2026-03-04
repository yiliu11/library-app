import { NotificationRepository } from '../repositories/notification.repository';
import { NotificationRequestDTO, NotificationResponseDTO, NotificationDTO, NotificationStatus } from '../dtos/notification.dto';
import { EmailNotificationDTO } from '../dtos/email.dto';
import { IEmailSender } from '../interfaces/email-sender.interface';
import { EmailTemplates } from './template/email.templates';
import { SMSTemplates } from './template/sms.templates';
import { BadRequestError, NotFoundError } from '../middlewares/error.middleware';
import { logger } from '../utils/logger';
import { env } from '../config/env';

export class NotificationService {
  constructor(
    private notificationRepository: NotificationRepository,
    private emailSender: IEmailSender,
  ) {}

  async sendNotification(notificationRequest: NotificationRequestDTO): Promise<NotificationResponseDTO> {
    // Create notification record
    const notification: any = {
      recipient_id: notificationRequest.recipientId,
      recipient_email: notificationRequest.recipientEmail,
      recipient_phone: notificationRequest.recipientPhone,
      subject: notificationRequest.subject,
      message: notificationRequest.message,
      notification_type: notificationRequest.notificationType,
      status: NotificationStatus.PENDING,
      metadata: notificationRequest.metadata,
    };

    const createdNotification = await this.notificationRepository.createNotification(notification);

    // Send notification based on available contact methods
    let success = false;

    if (notificationRequest.recipientEmail) {
      // Send email
      const emailTemplate = EmailTemplates.getTemplate(
        notificationRequest.notificationType,
        {
          ...notificationRequest.metadata,
          subject: notificationRequest.subject,
          message: notificationRequest.message,
        }
      );

      const emailDTO: EmailNotificationDTO = {
        to: notificationRequest.recipientEmail,
        subject: emailTemplate.subject,
        body: emailTemplate.body,
      };

      success = await this.emailSender.send(emailDTO);

      if (success) {
        await this.notificationRepository.updateNotificationStatus(
          createdNotification.id!,
          NotificationStatus.SENT
        );
      } else {
        await this.notificationRepository.updateNotificationFailure(
          createdNotification.id!,
          'Failed to send email'
        );
      }
    }

    // In a real app, you would also send SMS if recipientPhone is provided
    // This is commented out as we don't have an SMS sender implementation
    /*
    if (notificationRequest.recipientPhone && !success) {
      const smsTemplate = SMSTemplates.getTemplate(
        notificationRequest.notificationType,
        notificationRequest.metadata
      );

      success = await this.smsSender.send(
        notificationRequest.recipientPhone,
        smsTemplate
      );

      if (success) {
        await this.notificationRepository.updateNotificationStatus(
          createdNotification.id!,
          NotificationStatus.SENT
        );
      } else {
        await this.notificationRepository.updateNotificationFailure(
          createdNotification.id!,
          'Failed to send SMS'
        );
      }
    }
    */

    if (!success && !notificationRequest.recipientPhone) {
      // If no contact method succeeded, mark as failed
      await this.notificationRepository.updateNotificationFailure(
        createdNotification.id!,
        'No valid contact method provided'
      );
    }

    return new NotificationResponseDTO(createdNotification);
  }

  async retryFailedNotifications(): Promise<number> {
    const failedNotifications = await this.notificationRepository.findPendingNotifications();
    let successfulRetries = 0;

    for (const notification of failedNotifications) {
      try {
        let success = false;

        if (notification.recipient_email) {
          const emailTemplate = EmailTemplates.getTemplate(
            notification.notification_type,
            notification.metadata || {}
          );

          const emailDTO: EmailNotificationDTO = {
            to: notification.recipient_email,
            subject: emailTemplate.subject,
            body: emailTemplate.body,
          };

          success = await this.emailSender.send(emailDTO);
        }

        if (success) {
          await this.notificationRepository.updateNotificationStatus(
            notification.id!,
            NotificationStatus.SENT
          );
          successfulRetries++;
          logger.info(`Successfully retried notification ${notification.id}`);
        }
      } catch (err) {
        logger.error(`Failed to retry notification ${notification.id}: ${err}`);
        await this.notificationRepository.updateNotificationFailure(
          notification.id!,
          `Retry failed: ${err}`
        );
      }
    }

    return successfulRetries;
  }

  async getNotificationById(id: number): Promise<NotificationDTO> {
    const notification = await this.notificationRepository.findById(id);
    if (!notification) {
      throw new NotFoundError('Notification not found');
    }
    return new NotificationDTO(notification);
  }
}

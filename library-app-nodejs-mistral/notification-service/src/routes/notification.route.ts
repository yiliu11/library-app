import { Router } from 'express';
import { NotificationController } from '../controllers/notification.controller';
import { NotificationRepository } from '../repositories/notification.repository';
import { NotificationService } from '../services/notification.service';
import { NodemailerEmailSender } from '../services/email/nodemailer.email-sender';
import { validateDTO } from '../middlewares/validation.middleware';
import { NotificationRequestDTO } from '../dtos/notification.dto';

const router = Router();
const notificationRepository = new NotificationRepository();
const emailSender = new NodemailerEmailSender();
const notificationService = new NotificationService(notificationRepository, emailSender);
const notificationController = new NotificationController(notificationService);

// Public routes (for receiving notifications from other services)
router.post(
  '/',
  validateDTO(NotificationRequestDTO),
  notificationController.sendNotification
);

// Admin routes
router.post('/retry', notificationController.retryFailedNotifications);
router.get('/:id', notificationController.getNotificationById);

export default router;

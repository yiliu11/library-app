import { Request, Response } from 'express';
import { NotificationService } from '../services/notification.service';
import { NotificationRequestDTO } from '../dtos/notification.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class NotificationController {
  constructor(private notificationService: NotificationService) {}

  sendNotification = async (req: Request, res: Response) => {
    const notificationRequest: NotificationRequestDTO = req.body;
    const notificationResponse = await this.notificationService.sendNotification(notificationRequest);
    res.status(201).json(notificationResponse);
  };

  retryFailedNotifications = async (req: Request, res: Response) => {
    const count = await this.notificationService.retryFailedNotifications();
    res.json({ message: `Successfully retried ${count} notifications` });
  };

  getNotificationById = async (req: Request, res: Response) => {
    const notificationId = parseInt(req.params.id);
    const notification = await this.notificationService.getNotificationById(notificationId);
    res.json(notification);
  };
}

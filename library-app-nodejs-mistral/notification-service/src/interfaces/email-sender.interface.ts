import { EmailNotificationDTO } from '../dtos/email.dto';

export interface IEmailSender {
  send(email: EmailNotificationDTO): Promise<boolean>;
}

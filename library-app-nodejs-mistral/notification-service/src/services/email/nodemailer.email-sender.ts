import { createTransport, Transporter } from 'nodemailer';
import { IEmailSender } from '../interfaces/email-sender.interface';
import { EmailNotificationDTO } from '../../dtos/email.dto';
import { env } from '../../config/env';
import { logger } from '../../utils/logger';

export class NodemailerEmailSender implements IEmailSender {
  private transporter: Transporter;

  constructor() {
    this.transporter = createTransport({
      host: env.SMTP_HOST,
      port: env.SMTP_PORT,
      secure: env.SMTP_PORT === 465, // true for 465, false for other ports
      auth: {
        user: env.SMTP_USER,
        pass: env.SMTP_PASSWORD,
      },
    });
  }

  async send(email: EmailNotificationDTO): Promise<boolean> {
    try {
      const info = await this.transporter.sendMail({
        from: env.EMAIL_FROM,
        to: email.to,
        subject: email.subject,
        html: email.body,
      });

      logger.info(`Email sent: ${info.messageId}`);
      return true;
    } catch (err) {
      logger.error(`Failed to send email: ${err}`);
      return false;
    }
  }
}

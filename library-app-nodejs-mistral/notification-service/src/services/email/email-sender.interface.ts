import { EmailNotificationDTO } from '../dtos/email.dto';

/**
 * Interface for email sending services
 */
export interface IEmailSender {
  /**
   * Sends an email
   * @param email The email to send
   * @returns Promise that resolves to true if the email was sent successfully, false otherwise
   */
  send(email: EmailNotificationDTO): Promise<boolean>;

  /**
   * Optional method to verify the email sender configuration
   * @returns Promise that resolves to true if the configuration is valid, false otherwise
   */
  verifyConfiguration?(): Promise<boolean>;
}

/**
 * Interface for email template rendering
 */
export interface IEmailTemplateRenderer {
  /**
   * Renders an email template
   * @param templateName The name of the template to render
   * @param context The context data to use when rendering the template
   * @returns Promise that resolves to the rendered email (subject and body)
   */
  render(templateName: string, context: any): Promise<{ subject: string; body: string }>;
}

/**
 * Interface for email service that combines sending and template rendering
 */
export interface IEmailService extends IEmailSender, IEmailTemplateRenderer {
  /**
   * Sends an email using a template
   * @param templateName The name of the template to use
   * @param to The recipient's email address
   * @param context The context data to use when rendering the template
   * @returns Promise that resolves to true if the email was sent successfully, false otherwise
   */
  sendWithTemplate(templateName: string, to: string, context: any): Promise<boolean>;
}

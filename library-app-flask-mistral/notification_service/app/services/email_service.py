from flask import current_app
from flask_mail import Message
from app.models.notification import Notification, NotificationStatus
from werkzeug.exceptions import InternalServerError
import smtplib
from email.mime.text import MIMEText

class EmailService:
    @staticmethod
    def send_email(notification):
        try:
            msg = Message(
                subject=notification.subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[notification.recipient_email]
            )
            msg.body = notification.message

            # For HTML emails, you can use msg.html instead of msg.body
            # msg.html = "<p>HTML content</p>"

            result = current_app.mail.send(msg)

            if result:
                notification.mark_as_sent()
                current_app.db.session.commit()
                current_app.logger.info(f"Email sent to {notification.recipient_email}")
                return True
            else:
                raise Exception("Email send returned False")
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            notification.mark_as_failed(error_msg)
            current_app.db.session.commit()
            current_app.logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            notification.mark_as_failed(error_msg)
            current_app.db.session.commit()
            current_app.logger.error(error_msg)
            return False

    @staticmethod
    def send_email_direct(to, subject, body):
        try:
            msg = Message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[to]
            )
            msg.body = body

            result = current_app.mail.send(msg)
            return result
        except Exception as e:
            current_app.logger.error(f"Error sending direct email: {str(e)}")
            return False

from flask import current_app
from twilio.rest import Client
from app.models.notification import Notification, NotificationStatus
from werkzeug.exceptions import InternalServerError

class SMSService:
    @staticmethod
    def send_sms(notification):
        try:
            # Initialize Twilio client
            client = Client(
                current_app.config['SMS_ACCOUNT_SID'],
                current_app.config['SMS_AUTH_TOKEN']
            )

            message = client.messages.create(
                body=notification.message,
                from_=current_app.config['SMS_FROM_NUMBER'],
                to=notification.recipient_phone
            )

            if message.sid:
                notification.mark_as_sent()
                current_app.db.session.commit()
                current_app.logger.info(f"SMS sent to {notification.recipient_phone}")
                return True
            else:
                raise Exception("SMS send returned no message SID")
        except Exception as e:
            error_msg = f"Error sending SMS: {str(e)}"
            notification.mark_as_failed(error_msg)
            current_app.db.session.commit()
            current_app.logger.error(error_msg)
            return False

    @staticmethod
    def send_sms_direct(to, message):
        try:
            client = Client(
                current_app.config['SMS_ACCOUNT_SID'],
                current_app.config['SMS_AUTH_TOKEN']
            )

            sms = client.messages.create(
                body=message,
                from_=current_app.config['SMS_FROM_NUMBER'],
                to=to
            )

            return sms.sid is not None
        except Exception as e:
            current_app.logger.error(f"Error sending direct SMS: {str(e)}")
            return False

import { NotificationType } from '../../dtos/notification.dto';

export class SMSTemplates {
  static getTemplate(type: NotificationType, data: any): string {
    switch (type) {
      case NotificationType.OVERDUE_BOOK:
        return `Overdue Book: ${data.bookTitle}. Due: ${new Date(data.dueDate).toDateString()}. Return ASAP to avoid fines.`;

      case NotificationType.REQUEST_APPROVED:
        return `Your request for "${data.bookTitle}" has been approved.${data.notes ? ` Notes: ${data.notes}` : ''}`;

      case NotificationType.REQUEST_REJECTED:
        return `Your request for "${data.bookTitle}" has been rejected.${data.notes ? ` Reason: ${data.notes}` : ''}`;

      case NotificationType.CHECKOUT_CONFIRMATION:
        return `You checked out "${data.bookTitle}". Due: ${new Date(data.dueDate).toDateString()}.`;

      case NotificationType.RENEWAL_CONFIRMATION:
        return `Your checkout for "${data.bookTitle}" has been renewed. New due: ${new Date(data.dueDate).toDateString()}.`;

      case NotificationType.RETURN_CONFIRMATION:
        return `You returned "${data.bookTitle}".${data.fineAmount > 0 ? ` Fine: $${data.fineAmount}.` : ''}`;

      case NotificationType.NEW_BOOK_REQUEST:
        return `New request: "${data.bookTitle}" by ${data.bookAuthor}. Review in system.`;

      default:
        return data.message || 'New library notification. Check your email for details.';
    }
  }
}

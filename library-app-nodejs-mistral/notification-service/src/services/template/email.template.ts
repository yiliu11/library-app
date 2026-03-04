import { NotificationType } from '../../dtos/notification.dto';

export class EmailTemplates {
  static getTemplate(type: NotificationType, data: any): { subject: string; body: string } {
    switch (type) {
      case NotificationType.OVERDUE_BOOK:
        return {
          subject: `Overdue Book: ${data.bookTitle}`,
          body: `
            <h1>Overdue Book Reminder</h1>
            <p>Dear User,</p>
            <p>The book "<strong>${data.bookTitle}</strong>" is overdue.</p>
            <p>Due date: ${new Date(data.dueDate).toDateString()}</p>
            <p>Please return it as soon as possible to avoid additional fines.</p>
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.REQUEST_APPROVED:
        return {
          subject: `Your Book Request Has Been Approved: ${data.bookTitle}`,
          body: `
            <h1>Book Request Approved</h1>
            <p>Dear User,</p>
            <p>Your request for the book "<strong>${data.bookTitle}</strong>" has been approved.</p>
            ${data.notes ? `<p>Notes: ${data.notes}</p>` : ''}
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.REQUEST_REJECTED:
        return {
          subject: `Your Book Request Has Been Rejected: ${data.bookTitle}`,
          body: `
            <h1>Book Request Rejected</h1>
            <p>Dear User,</p>
            <p>Your request for the book "<strong>${data.bookTitle}</strong>" has been rejected.</p>
            ${data.notes ? `<p>Reason: ${data.notes}</p>` : ''}
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.CHECKOUT_CONFIRMATION:
        return {
          subject: `Book Checkout Confirmation: ${data.bookTitle}`,
          body: `
            <h1>Book Checkout Confirmation</h1>
            <p>Dear User,</p>
            <p>You have successfully checked out the book "<strong>${data.bookTitle}</strong>".</p>
            <p>Due date: ${new Date(data.dueDate).toDateString()}</p>
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.RENEWAL_CONFIRMATION:
        return {
          subject: `Book Renewal Confirmation: ${data.bookTitle}`,
          body: `
            <h1>Book Renewal Confirmation</h1>
            <p>Dear User,</p>
            <p>Your checkout for the book "<strong>${data.bookTitle}</strong>" has been renewed.</p>
            <p>New due date: ${new Date(data.dueDate).toDateString()}</p>
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.RETURN_CONFIRMATION:
        return {
          subject: `Book Return Confirmation: ${data.bookTitle}`,
          body: `
            <h1>Book Return Confirmation</h1>
            <p>Dear User,</p>
            <p>You have successfully returned the book "<strong>${data.bookTitle}</strong>".</p>
            ${data.fineAmount > 0 ? `<p>Fine charged: $${data.fineAmount}</p>` : ''}
            <p>Thank you,<br>Library Team</p>
          `,
        };

      case NotificationType.NEW_BOOK_REQUEST:
        return {
          subject: `New Book Request: ${data.bookTitle}`,
          body: `
            <h1>New Book Request</h1>
            <p>Dear Librarian,</p>
            <p>A new book request has been submitted:</p>
            <ul>
              <li>Title: ${data.bookTitle}</li>
              <li>Author: ${data.bookAuthor}</li>
              ${data.bookIsbn ? `<li>ISBN: ${data.bookIsbn}</li>` : ''}
            </ul>
            <p>Please review this request in the system.</p>
            <p>Thank you,<br>Library Team</p>
          `,
        };

      default:
        return {
          subject: data.subject || 'Library Notification',
          body: data.message || 'You have a new notification from the library.',
        };
    }
  }
}

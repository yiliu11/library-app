import { CheckoutRepository } from '../repositories/checkout.repository';
import {
  CheckoutRequestDTO,
  CheckoutResponseDTO,
  RenewalRequestDTO,
  ReturnRequestDTO,
  CheckoutStatus,
} from '../dtos/checkout.dto';
import { UserRecordDTO, UserRecordsRequestDTO } from '../dtos/record.dto';
import { BadRequestError, ForbiddenError, NotFoundError } from '../middlewares/error.middleware';
import { logger } from '../utils/logger';
import { DateUtils } from '../utils/date-utils';
import axios from 'axios';
import { env } from '../config/env';

export class CheckoutService {
  constructor(private checkoutRepository: CheckoutRepository) {}

  async checkoutBook(request: CheckoutRequestDTO, userId: number): Promise<CheckoutResponseDTO> {
    // Check if user has reached checkout limit
    const canCheckout = await this.checkoutRepository.checkUserCheckoutLimit(userId);
    if (!canCheckout) {
      throw new BadRequestError(`You have reached the maximum checkout limit of ${env.MAX_CHECKOUT_LIMIT} books`);
    }

    // Check if user has overdue books
    const hasOverdue = await this.checkoutRepository.checkUserHasOverdueBooks(userId);
    if (hasOverdue) {
      throw new BadRequestError('You have overdue books. Please return them before checking out more');
    }

    // Check if book is available
    try {
      const response = await axios.get(`${env.BOOK_SERVICE_URL}/api/books/${request.bookId}`);
      if (response.data.availabilityStatus !== 'AVAILABLE') {
        throw new BadRequestError('This book is currently unavailable');
      }
    } catch (err) {
      logger.error(`Failed to check book availability: ${err}`);
      throw new BadRequestError('Failed to verify book availability');
    }

    // Check if user already has this book checked out
    const existingCheckout = await this.checkoutRepository.findByUserAndBook(userId, request.bookId);
    if (existingCheckout) {
      throw new BadRequestError('You already have this book checked out');
    }

    // Create checkout record
    const dueDate = DateUtils.calculateDueDate();
    const checkout = {
      user_id: userId,
      book_id: request.bookId,
      due_date: dueDate,
      status: CheckoutStatus.ACTIVE,
    };

    const createdCheckout = await this.checkoutRepository.createCheckout(checkout);

    // Update book availability status
    try {
      await axios.put(`${env.BOOK_SERVICE_URL}/api/books/${request.bookId}/status`, {
        status: 'CHECKED_OUT',
      });
    } catch (err) {
      logger.error(`Failed to update book status: ${err}`);
      // Rollback checkout creation
      await this.checkoutRepository.updateStatus(createdCheckout.id!, CheckoutStatus.RETURNED);
      throw new BadRequestError('Failed to update book status');
    }

    // Get book title for response
    let bookTitle = '';
    try {
      const response = await axios.get(`${env.BOOK_SERVICE_URL}/api/books/${request.bookId}`);
      bookTitle = response.data.title;
    } catch (err) {
      logger.error(`Failed to get book title: ${err}`);
    }

    // Send notification
    try {
      await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
        recipientId: userId,
        notificationType: 'CHECKOUT_CONFIRMATION',
        subject: 'Book Checkout Confirmation',
        message: `You have successfully checked out "${bookTitle}". Due date: ${dueDate.toDateString()}`,
        metadata: {
          bookId: request.bookId,
          bookTitle,
          dueDate: dueDate.toISOString(),
        },
      });
    } catch (err) {
      logger.error(`Failed to send checkout notification: ${err}`);
    }

    return new CheckoutResponseDTO({
      ...createdCheckout,
      book_title: bookTitle,
    });
  }

  async renewCheckout(request: RenewalRequestDTO, userId: number): Promise<CheckoutResponseDTO> {
    const checkout = await this.checkoutRepository.findById(request.checkoutId);
    if (!checkout) {
      throw new NotFoundError('Checkout record not found');
    }

    if (checkout.user_id !== userId) {
      throw new ForbiddenError('You can only renew your own checkouts');
    }

    if (checkout.status !== CheckoutStatus.ACTIVE) {
      throw new BadRequestError('Only active checkouts can be renewed');
    }

    if (DateUtils.isOverdue(checkout.due_date)) {
      throw new BadRequestError('Overdue books cannot be renewed');
    }

    // Calculate new due date (extend by CHECKOUT_DURATION_DAYS)
    const newDueDate = new Date(checkout.due_date);
    newDueDate.setDate(newDueDate.getDate() + env.CHECKOUT_DURATION_DAYS);

    const updatedCheckout = await this.checkoutRepository.updateCheckout(checkout.id!, {
      due_date: newDueDate,
      status: CheckoutStatus.RENEWED,
    });

    if (!updatedCheckout) {
      throw new BadRequestError('Failed to renew checkout');
    }

    // Get book title for response
    let bookTitle = '';
    try {
      const response = await axios.get(`${env.BOOK_SERVICE_URL}/api/books/${checkout.book_id}`);
      bookTitle = response.data.title;
    } catch (err) {
      logger.error(`Failed to get book title: ${err}`);
    }

    // Send notification
    try {
      await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
        recipientId: userId,
        notificationType: 'RENEWAL_CONFIRMATION',
        subject: 'Book Renewal Confirmation',
        message: `Your checkout for "${bookTitle}" has been renewed. New due date: ${newDueDate.toDateString()}`,
        metadata: {
          bookId: checkout.book_id,
          bookTitle,
          dueDate: newDueDate.toISOString(),
        },
      });
    } catch (err) {
      logger.error(`Failed to send renewal notification: ${err}`);
    }

    return new CheckoutResponseDTO({
      ...updatedCheckout,
      book_title: bookTitle,
    });
  }

  async returnBook(request: ReturnRequestDTO, userId: number): Promise<void> {
    const checkout = await this.checkoutRepository.findById(request.checkoutId);
    if (!checkout) {
      throw new NotFoundError('Checkout record not found');
    }

    if (checkout.user_id !== userId) {
      throw new ForbiddenError('You can only return your own checkouts');
    }

    if (checkout.status === CheckoutStatus.RETURNED) {
      throw new BadRequestError('This book has already been returned');
    }

    // Calculate fine if overdue
    let fineAmount = 0;
    if (DateUtils.isOverdue(checkout.due_date)) {
      const overdueDays = DateUtils.calculateOverdueDays(checkout.due_date);
      // Simple fine calculation: $1 per day overdue
      fineAmount = overdueDays * 1;
    }

    const returnDate = new Date();
    const status = fineAmount > 0 ? CheckoutStatus.OVERDUE : CheckoutStatus.RETURNED;

    await this.checkoutRepository.updateCheckout(checkout.id!, {
      return_date: returnDate,
      status,
      fine_amount: fineAmount,
    });

    // Update book availability status
    try {
      await axios.put(`${env.BOOK_SERVICE_URL}/api/books/${checkout.book_id}/status`, {
        status: 'AVAILABLE',
      });
    } catch (err) {
      logger.error(`Failed to update book status: ${err}`);
      throw new BadRequestError('Failed to update book status');
    }

    // Get book title for notification
    let bookTitle = '';
    try {
      const response = await axios.get(`${env.BOOK_SERVICE_URL}/api/books/${checkout.book_id}`);
      bookTitle = response.data.title;
    } catch (err) {
      logger.error(`Failed to get book title: ${err}`);
    }

    // Send return confirmation notification
    try {
      await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
        recipientId: userId,
        notificationType: 'RETURN_CONFIRMATION',
        subject: 'Book Return Confirmation',
        message: `You have successfully returned "${bookTitle}".${fineAmount > 0 ? ` Fine: $${fineAmount}` : ''}`,
        metadata: {
          bookId: checkout.book_id,
          bookTitle,
          fineAmount,
        },
      });
    } catch (err) {
      logger.error(`Failed to send return notification: ${err}`);
    }

    // If there's a fine, send overdue notification
    if (fineAmount > 0) {
      try {
        await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
          recipientId: userId,
          notificationType: 'OVERDUE_BOOK',
          subject: 'Overdue Book Fine',
          message: `You have been charged a fine of $${fineAmount} for returning "${bookTitle}" late.`,
          metadata: {
            bookId: checkout.book_id,
            bookTitle,
            fineAmount,
          },
        });
      } catch (err) {
        logger.error(`Failed to send fine notification: ${err}`);
      }
    }
  }

  async getUserRecords(request: UserRecordsRequestDTO, requestingUserId: number, requestingUserRole: string): Promise<UserRecordDTO> {
    // Librarians can access any user's records, others can only access their own
    if (request.userId !== requestingUserId && requestingUserRole !== 'LIBRARIAN') {
      throw new ForbiddenError('You can only access your own records');
    }

    const record = await this.checkoutRepository.getUserRecords(request.userId);
    if (!record) {
      return new UserRecordDTO({
        user_id: request.userId,
        checked_out_items: [],
        total_fines: 0,
      });
    }

    return new UserRecordDTO(record);
  }

  async checkBookAvailability(bookId: number): Promise<boolean> {
    const activeCheckout = await this.checkoutRepository.findActiveByBook(bookId);
    return !activeCheckout;
  }
}

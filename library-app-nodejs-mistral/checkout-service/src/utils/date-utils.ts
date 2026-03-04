import { env } from '../config/env';

export class DateUtils {
  /**
   * Calculate the due date for a checkout.
   * @returns Date object representing the due date.
   */
  static calculateDueDate(): Date {
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + env.CHECKOUT_DURATION_DAYS);
    return dueDate;
  }

  /**
   * Check if a date is overdue.
   * @param dueDate The due date to check.
   * @returns True if the date is overdue, false otherwise.
   */
  static isOverdue(dueDate: Date): boolean {
    return new Date() > new Date(dueDate);
  }

  /**
   * Calculate the number of days a book is overdue.
   * @param dueDate The due date of the book.
   * @returns Number of days overdue, or 0 if not overdue.
   */
  static calculateOverdueDays(dueDate: Date): number {
    const today = new Date();
    const overdueDate = new Date(dueDate);
    const diffTime = today.getTime() - overdueDate.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  }
}

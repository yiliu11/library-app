import { IsInt } from 'class-validator';
import { CheckoutStatus } from './checkout.dto';

export class CheckedOutItemDTO {
  bookId: number;
  bookTitle: string;
  dueDate: Date;
  status: CheckoutStatus;
  fineAmount: number;

  constructor(item: any) {
    this.bookId = item.book_id;
    this.bookTitle = item.book_title;
    this.dueDate = item.due_date;
    this.status = item.status;
    this.fineAmount = item.fine_amount || 0;
  }
}

export class UserRecordDTO {
  userId: number;
  checkedOutItems: CheckedOutItemDTO[];
  totalFines: number;

  constructor(record: any) {
    this.userId = record.user_id;
    this.checkedOutItems = record.checked_out_items?.map((item: any) => new CheckedOutItemDTO(item)) || [];
    this.totalFines = record.total_fines || 0;
  }
}

export class UserRecordsRequestDTO {
  @IsInt()
  userId: number;
}

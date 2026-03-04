import { IsInt, IsNotEmpty, IsDateString, IsEnum } from 'class-validator';

export enum CheckoutStatus {
  ACTIVE = 'ACTIVE',
  OVERDUE = 'OVERDUE',
  RETURNED = 'RETURNED',
  RENEWED = 'RENEWED',
}

export class CheckoutRequestDTO {
  @IsInt()
  @IsNotEmpty()
  userId: number;

  @IsInt()
  @IsNotEmpty()
  bookId: number;
}

export class CheckoutResponseDTO {
  checkoutId: number;
  bookId: number;
  bookTitle: string;
  dueDate: Date;
  status: CheckoutStatus;

  constructor(checkout: any) {
    this.checkoutId = checkout.id;
    this.bookId = checkout.book_id;
    this.bookTitle = checkout.book_title;
    this.dueDate = checkout.due_date;
    this.status = checkout.status;
  }
}

export class RenewalRequestDTO {
  @IsInt()
  @IsNotEmpty()
  checkoutId: number;
}

export class ReturnRequestDTO {
  @IsInt()
  @IsNotEmpty()
  checkoutId: number;
}

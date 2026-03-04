import { IsString, IsNotEmpty, IsOptional, IsEnum, IsISBN } from 'class-validator';

export enum RequestStatus {
  PENDING = 'PENDING',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
  ARCHIVED = 'ARCHIVED',
}

export class BookRequestDTO {
  @IsString()
  @IsNotEmpty()
  bookTitle: string;

  @IsString()
  @IsNotEmpty()
  bookAuthor: string;

  @IsISBN()
  @IsOptional()
  bookIsbn?: string;

  @IsString()
  @IsOptional()
  notes?: string;
}

export class BookRequestResponseDTO {
  requestId: number;
  bookTitle: string;
  bookAuthor: string;
  bookIsbn?: string;
  requesterId: number;
  requestDate: Date;
  status: RequestStatus;
  notes?: string;

  constructor(request: any) {
    this.requestId = request.id;
    this.bookTitle = request.book_title;
    this.bookAuthor = request.book_author;
    this.bookIsbn = request.book_isbn;
    this.requesterId = request.requester_id;
    this.requestDate = request.request_date;
    this.status = request.status;
    this.notes = request.notes;
  }
}

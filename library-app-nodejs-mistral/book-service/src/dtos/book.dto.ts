import { IsString, IsNotEmpty, IsOptional, IsEnum, IsISBN, IsDateString } from 'class-validator';

export enum AvailabilityStatus {
  AVAILABLE = 'AVAILABLE',
  CHECKED_OUT = 'CHECKED_OUT',
  RESERVED = 'RESERVED',
  LOST = 'LOST',
}

export class BookRequestDTO {
  @IsString()
  @IsNotEmpty()
  title: string;

  @IsString()
  @IsNotEmpty()
  author: string;

  @IsISBN()
  @IsNotEmpty()
  isbn: string;

  @IsDateString()
  @IsOptional()
  publicationDate?: string;
}

export class BookResponseDTO {
  id: number;
  title: string;
  author: string;
  isbn: string;
  publicationDate: Date;
  availabilityStatus: AvailabilityStatus;
  createdAt: Date;
  updatedAt: Date;

  constructor(book: any) {
    this.id = book.id;
    this.title = book.title;
    this.author = book.author;
    this.isbn = book.isbn;
    this.publicationDate = book.publication_date;
    this.availabilityStatus = book.availability_status;
    this.createdAt = book.created_at;
    this.updatedAt = book.updated_at;
  }
}

export class BookUpdateDTO {
  @IsString()
  @IsOptional()
  title?: string;

  @IsString()
  @IsOptional()
  author?: string;

  @IsISBN()
  @IsOptional()
  isbn?: string;

  @IsDateString()
  @IsOptional()
  publicationDate?: string;

  @IsEnum(AvailabilityStatus)
  @IsOptional()
  availabilityStatus?: AvailabilityStatus;
}

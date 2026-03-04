import { IsString, IsNotEmpty, IsOptional, IsEnum } from 'class-validator';

export enum SearchCriteria {
  TITLE = 'TITLE',
  AUTHOR = 'AUTHOR',
  ISBN = 'ISBN',
}

export class BookSearchDTO {
  @IsString()
  @IsNotEmpty()
  searchTerm: string;

  @IsEnum(SearchCriteria)
  @IsOptional()
  searchBy?: SearchCriteria = SearchCriteria.TITLE;
}

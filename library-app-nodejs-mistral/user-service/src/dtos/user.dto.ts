import { IsEmail, IsEnum, IsNotEmpty, IsString } from 'class-validator';

export enum UserRole {
  PATRON = 'PATRON',
  STAFF = 'STAFF',
  LIBRARIAN = 'LIBRARIAN',
}

export class UserRegistrationDTO {
  @IsString()
  @IsNotEmpty()
  username: string;

  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsEnum(UserRole)
  @IsNotEmpty()
  role: UserRole;
}

export class UserDTO {
  id: number;
  username: string;
  email: string;
  role: UserRole;
}

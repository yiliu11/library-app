import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';

export class LoginRequestDTO {
  @IsString()
  @IsNotEmpty()
  username: string;

  @IsString()
  @IsNotEmpty()
  @MinLength(6)
  password: string;
}

export class LoginResponseDTO {
  token: string;
  role: string;
}

export class PasswordResetRequestDTO {
  @IsEmail()
  @IsNotEmpty()
  email: string;
}

import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';
import { LoginRequestDTO, LoginResponseDTO, PasswordResetRequestDTO } from '../dtos/auth.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class AuthController {
  constructor(private authService: AuthService) {}

  login = async (req: Request, res: Response) => {
    const loginResponse: LoginResponseDTO = await this.authService.login(req.body);
    res.json(loginResponse);
  };

  requestPasswordReset = async (req: Request, res: Response) => {
    await this.authService.requestPasswordReset(req.body.email);
    res.json({ message: 'Password reset email sent' });
  };
}

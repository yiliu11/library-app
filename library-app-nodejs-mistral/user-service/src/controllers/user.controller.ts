import { Request, Response } from 'express';
import { UserService } from '../services/user.service';
import { UserRegistrationDTO } from '../dtos/user.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class UserController {
  constructor(private userService: UserService) {}

  registerUser = async (req: Request, res: Response) => {
    const userDTO = await this.userService.registerUser(
      req.body,
      req.user.role
    );
    res.status(201).json(userDTO);
  };
}

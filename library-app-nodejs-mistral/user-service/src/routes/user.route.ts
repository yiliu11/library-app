import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { authenticate, authorize } from '../middlewares/auth.middleware';
import { validateDTO } from '../middlewares/validation.middleware';
import { UserRegistrationDTO } from '../dtos/user.dto';
import { UserRole } from '../models/user.model';

const router = Router();
const userController = new UserController(new UserService(new UserRepository()));

router.post(
  '/register',
  authenticate,
  authorize([UserRole.LIBRARIAN]),
  validateDTO(UserRegistrationDTO),
  userController.registerUser
);

export default router;

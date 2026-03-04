import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { validateDTO } from '../middlewares/validation.middleware';
import { LoginRequestDTO, PasswordResetRequestDTO } from '../dtos/auth.dto';

const router = Router();
const authController = new AuthController(new AuthService(new UserRepository()));

router.post('/login', validateDTO(LoginRequestDTO), authController.login);
router.post('/request-reset', validateDTO(PasswordResetRequestDTO), authController.requestPasswordReset);

export default router;

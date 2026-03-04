import { Router } from 'express';
import { CheckoutController } from '../controllers/checkout.controller';
import { CheckoutRepository } from '../repositories/checkout.repository';
import { CheckoutService } from '../services/checkout.service';
import { authenticate } from '../middlewares/auth.middleware';
import { validateDTO } from '../middlewares/validation.middleware';
import {
  CheckoutRequestDTO,
  RenewalRequestDTO,
  ReturnRequestDTO,
} from '../dtos/checkout.dto';
import { UserRecordsRequestDTO } from '../dtos/record.dto';

const router = Router();
const checkoutRepository = new CheckoutRepository();
const checkoutService = new CheckoutService(checkoutRepository);
const checkoutController = new CheckoutController(checkoutService);

// Protected routes (require authentication)
router.use(authenticate);

// Checkout routes
router.post(
  '/checkout',
  validateDTO(CheckoutRequestDTO),
  checkoutController.checkoutBook
);

router.post(
  '/renew',
  validateDTO(RenewalRequestDTO),
  checkoutController.renewCheckout
);

router.post(
  '/return',
  validateDTO(ReturnRequestDTO),
  checkoutController.returnBook
);

// User records route
router.get(
  '/records/:userId',
  validateDTO(UserRecordsRequestDTO, 'params'),
  checkoutController.getUserRecords
);

export default router;

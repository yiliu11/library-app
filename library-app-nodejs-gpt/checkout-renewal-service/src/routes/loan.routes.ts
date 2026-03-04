import { Router } from 'express';
import * as loanController from '../controllers/loan.controller';
import validate from '../middlewares/validate';
import {
  checkoutSchema,
  renewSchema,
  returnSchema,
  viewUserLoansSchema
} from '../validators/loan.validator';

const router = Router();

// POST /api/loans/checkout
router.post('/checkout', validate(checkoutSchema), loanController.checkoutBook);

// POST /api/loans/renew
router.post('/renew', validate(renewSchema), loanController.renewLoan);

// POST /api/loans/return
router.post('/return', validate(returnSchema), loanController.returnBook);

// GET /api/loans/user/:userId
router.get('/user/:userId', validate(viewUserLoansSchema), loanController.viewUserLoans);

export default router;

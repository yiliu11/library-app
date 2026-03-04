import { Request, Response } from 'express';
import { CheckoutService } from '../services/checkout.service';
import {
  CheckoutRequestDTO,
  CheckoutResponseDTO,
  RenewalRequestDTO,
  ReturnRequestDTO,
} from '../dtos/checkout.dto';
import { UserRecordsRequestDTO, UserRecordDTO } from '../dtos/record.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class CheckoutController {
  constructor(private checkoutService: CheckoutService) {}

  checkoutBook = async (req: Request, res: Response) => {
    const checkoutRequest: CheckoutRequestDTO = req.body;
    const checkoutResponse = await this.checkoutService.checkoutBook(checkoutRequest, req.user.userId);
    res.status(201).json(checkoutResponse);
  };

  renewCheckout = async (req: Request, res: Response) => {
    const renewalRequest: RenewalRequestDTO = req.body;
    const checkoutResponse = await this.checkoutService.renewCheckout(renewalRequest, req.user.userId);
    res.json(checkoutResponse);
  };

  returnBook = async (req: Request, res: Response) => {
    const returnRequest: ReturnRequestDTO = req.body;
    await this.checkoutService.returnBook(returnRequest, req.user.userId);
    res.status(204).send();
  };

  getUserRecords = async (req: Request, res: Response) => {
    const recordsRequest: UserRecordsRequestDTO = req.params;
    const userRecords = await this.checkoutService.getUserRecords(
      recordsRequest,
      req.user.userId,
      req.user.role
    );
    res.json(userRecords);
  };
}

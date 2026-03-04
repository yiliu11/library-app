import { Request, Response } from 'express';
import { RequestService } from '../services/request.service';
import { BookRequestDTO, BookRequestResponseDTO } from '../dtos/request.dto';
import { RequestDecisionDTO } from '../dtos/decision.dto';
import { validateDTO } from '../middlewares/validation.middleware';

export class RequestController {
  constructor(private requestService: RequestService) {}

  submitRequest = async (req: Request, res: Response) => {
    const requestDTO: BookRequestDTO = req.body;
    const requestResponse = await this.requestService.submitRequest(
      requestDTO,
      req.user.userId,
      req.user.role
    );
    res.status(201).json(requestResponse);
  };

  processDecision = async (req: Request, res: Response) => {
    const decisionDTO: RequestDecisionDTO = req.body;
    const requestResponse = await this.requestService.processDecision(
      decisionDTO,
      req.user.userId
    );
    res.json(requestResponse);
  };

  getPendingRequests = async (req: Request, res: Response) => {
    const requests = await this.requestService.getPendingRequests();
    res.json(requests);
  };

  getMyRequests = async (req: Request, res: Response) => {
    const requests = await this.requestService.getRequestsByRequester(req.user.userId);
    res.json(requests);
  };
}

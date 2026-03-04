import { Request, Response, NextFunction } from "express";
import { validationResult } from "express-validator";
import { RequestService } from "../services/request.service";
import { BadRequestError } from "../utils/errors";

const requestService = new RequestService();

export class RequestController {
  // Create a new request
  async createRequest(req: Request, res: Response, next: NextFunction) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        throw new BadRequestError("Validation failed", errors.array());
      }

      const { title, author, description, requestedBy } = req.body;
      const request = await requestService.createRequest({
        title,
        author,
        description,
        requestedBy,
      });

      res.status(201).json({ success: true, data: request });
    } catch (error) {
      next(error);
    }
  }

  // Get all requests (optionally filter by status)
  async getRequests(req: Request, res: Response, next: NextFunction) {
    try {
      const { status } = req.query;
      const requests = await requestService.getRequests(
        status ? (status as any) : undefined
      );
      res.json({ success: true, data: requests });
    } catch (error) {
      next(error);
    }
  }

  // Get request by ID
  async getRequestById(req: Request, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id);
      const request = await requestService.getRequestById(id);
      res.json({ success: true, data: request });
    } catch (error) {
      next(error);
    }
  }

  // Update request status (approve/reject)
  async updateRequestStatus(req: Request, res: Response, next: NextFunction) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        throw new BadRequestError("Validation failed", errors.array());
      }

      const id = parseInt(req.params.id);
      const { status, reviewedBy } = req.body;
      const updated = await requestService.updateRequestStatus(
        id,
        status,
        reviewedBy
      );
      res.json({ success: true, data: updated });
    } catch (error) {
      next(error);
    }
  }

  // Delete a request
  async deleteRequest(req: Request, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id);
      const deleted = await requestService.deleteRequest(id);
      res.json({ success: true, data: deleted });
    } catch (error) {
      next(error);
    }
  }
}

import { Router } from 'express';
import { RequestController } from '../controllers/request.controller';
import { RequestRepository } from '../repositories/request.repository';
import { RequestService } from '../services/request.service';
import { authenticate, authorize } from '../middlewares/auth.middleware';
import { validateDTO } from '../middlewares/validation.middleware';
import { BookRequestDTO } from '../dtos/request.dto';
import { RequestDecisionDTO } from '../dtos/decision.dto';

const router = Router();
const requestRepository = new RequestRepository();
const requestService = new RequestService(requestRepository);
const requestController = new RequestController(requestService);

// Protected routes (require authentication)
router.use(authenticate);

// Staff routes
router.post(
  '/requests',
  authorize(['STAFF']),
  validateDTO(BookRequestDTO),
  requestController.submitRequest
);

router.get(
  '/my-requests',
  authorize(['STAFF', 'PATRON', 'LIBRARIAN']),
  requestController.getMyRequests
);

// Librarian routes
router.post(
  '/requests/decide',
  authorize(['LIBRARIAN']),
  validateDTO(RequestDecisionDTO),
  requestController.processDecision
);

router.get(
  '/requests/pending',
  authorize(['LIBRARIAN']),
  requestController.getPendingRequests
);

export default router;

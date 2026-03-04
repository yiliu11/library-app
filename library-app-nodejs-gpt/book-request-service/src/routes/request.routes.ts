import { Router } from "express";
import { RequestController } from "../controllers/request.controller";
import {
  createRequestValidator,
  updateRequestStatusValidator,
} from "../validators/request.validator";

const router = Router();
const controller = new RequestController();

// Create a new book request (staff only, but role-check handled via auth service middleware)
router.post("/", createRequestValidator, (req, res, next) =>
  controller.createRequest(req, res, next)
);

// Get all book requests (librarians can filter by status)
router.get("/", (req, res, next) =>
  controller.getRequests(req, res, next)
);

// Get single request by ID
router.get("/:id", (req, res, next) =>
  controller.getRequestById(req, res, next)
);

// Update request status (approve/reject by librarian)
router.patch("/:id/status", updateRequestStatusValidator, (req, res, next) =>
  controller.updateRequestStatus(req, res, next)
);

// Delete a request (cleanup, optional)
router.delete("/:id", (req, res, next) =>
  controller.deleteRequest(req, res, next)
);

export default router;

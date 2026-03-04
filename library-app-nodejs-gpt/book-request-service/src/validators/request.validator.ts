import { body, param } from "express-validator";

export const createRequestValidator = [
  body("title")
    .isString()
    .notEmpty()
    .withMessage("Title is required and must be a string"),
  body("author")
    .isString()
    .notEmpty()
    .withMessage("Author is required and must be a string"),
  body("description")
    .optional()
    .isString()
    .withMessage("Description must be a string if provided"),
  body("requestedBy")
    .isInt({ gt: 0 })
    .withMessage("RequestedBy must be a valid user ID"),
];

export const updateRequestStatusValidator = [
  param("id")
    .isInt({ gt: 0 })
    .withMessage("Request ID must be a positive integer"),
  body("status")
    .isIn(["APPROVED", "REJECTED"])
    .withMessage("Status must be either APPROVED or REJECTED"),
  body("reviewedBy")
    .isInt({ gt: 0 })
    .withMessage("ReviewedBy must be a valid librarian user ID"),
];

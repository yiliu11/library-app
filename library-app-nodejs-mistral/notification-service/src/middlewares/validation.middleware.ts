import { plainToClass } from 'class-transformer';
import { validate, ValidationError } from 'class-validator';
import { Request, Response, NextFunction } from 'express';
import { BadRequestError } from './error.middleware';

/**
 * Middleware to validate DTOs (Data Transfer Objects)
 * @param dtoClass The DTO class to validate against
 * @param source The source of the data to validate (body, params, or query)
 * @returns Express middleware function
 */
export const validateDTO = (
  dtoClass: any,
  source: 'body' | 'params' | 'query' = 'body'
) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Convert the request data to the DTO class instance
      const dto = plainToClass(dtoClass, req[source]);

      // Validate the DTO
      const errors: ValidationError[] = await validate(dto);

      // If there are validation errors, throw a BadRequestError
      if (errors.length > 0) {
        const errorMessages = errors.map((error) => {
          return Object.values(error.constraints || {});
        }).flat();

        throw new BadRequestError(errorMessages.join(', '));
      }

      // If validation passes, update the request object with the validated DTO
      req[source] = dto;
      next();
    } catch (error) {
      // Pass any errors to the error handling middleware
      next(error);
    }
  };
};

/**
 * Middleware to validate query parameters
 * @param dtoClass The DTO class to validate against
 * @returns Express middleware function
 */
export const validateQuery = (dtoClass: any) => {
  return validateDTO(dtoClass, 'query');
};

/**
 * Middleware to validate URL parameters
 * @param dtoClass The DTO class to validate against
 * @returns Express middleware function
 */
export const validateParams = (dtoClass: any) => {
  return validateDTO(dtoClass, 'params');
};

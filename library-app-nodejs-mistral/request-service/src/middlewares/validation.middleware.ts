import { plainToClass } from 'class-transformer';
import { validate, ValidationError } from 'class-validator';
import { Request, Response, NextFunction } from 'express';
import { BadRequestError } from './error.middleware';

export const validateDTO = (dtoClass: any, source: 'body' | 'params' | 'query' = 'body') => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const dto = plainToClass(dtoClass, req[source]);
    const errors: ValidationError[] = await validate(dto);

    if (errors.length > 0) {
      const errorMessages = errors.map((error) => {
        return Object.values(error.constraints || {});
      }).flat();
      throw new BadRequestError(errorMessages.join(', '));
    }

    req[source] = dto;
    next();
  };
};

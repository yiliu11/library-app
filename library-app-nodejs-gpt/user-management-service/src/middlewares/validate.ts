// src/middlewares/validate.ts

import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';

const validate = (schema: ZodSchema<any>) => async (req: Request, res: Response, next: NextFunction) => {
  try {
    await schema.parseAsync({
      body: req.body,
      query: req.query,
      params: req.params
    });
    next();
  } catch (err: any) {
    // Zod will throw a ZodError; let error middleware format it
    next(err);
  }
};

export default validate;

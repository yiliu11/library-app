// src/utils/response.ts

import { Response } from 'express';

export const sendSuccess = (res: Response, data: any = null, message = 'OK', status = 200) => {
  return res.status(status).json({ message, data });
};

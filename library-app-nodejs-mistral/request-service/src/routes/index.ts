import { Router } from 'express';
import requestRouter from './request.route';

const router = Router();

router.use('/api', requestRouter);

export default router;
